import logging
import asyncio
from datetime import datetime
import uvicorn
import tzlocal
from fastapi.middleware.cors import CORSMiddleware
from app.db.connector import setup_get_pool
from fastapi import FastAPI
from fastapi_users import FastAPIUsers
from app.services.email.smtp_broker import SMTPBroker
from app.models.user import User
from app.config import conf
from app.auth.auth import auth_backend
from app.auth.manager import providing_user_manager
from app.services.email.email_broker_repo import EmailBrokerRepo
from aiosmtplib.smtp import SMTP
from app.core.routers_includer import include_routers
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.interval import IntervalTrigger
from app.db.cache_storage.cache_repo import CacheRepo
from app.db.cache_storage.cache_redis import RedisStorage
from redis.asyncio import Redis


async def main() -> None:
    """Main function to run app"""

    logging.basicConfig(
        format='%(asctime)s : %(levelname)s : %(message)s',
        level=conf.LOG_LEVEL,
        filename=conf.LOG_FILE,
    )

    app = FastAPI()

    session_pool = await setup_get_pool(conf.DB_URL)

    origins = [
        f"http://{conf.FRONT_HOST}:{conf.FRONT_PORT}",
    ]
    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    users = FastAPIUsers[User, int](
        await providing_user_manager(session_pool),
        [auth_backend],
    )

    # ----------- Redis -----------------
    redis = Redis(
        host=conf.REDIS_HOST,
        port=conf.REDIS_PORT,
        db=conf.REDIS_DB,
        password=conf.REDIS_PASS,
    )
    redis_storage = RedisStorage(redis)
    cache_pool = CacheRepo(redis_storage)
    await cache_pool.connect()
    # -----------------------------------
    # -------- Email broker -------------
    mail = SMTP(port=conf.EMAIL_PORT, hostname=conf.EMAIL_SERVER)
    smtp_broker = SMTPBroker(
        mail,
        session_pool,
        conf.ADMIN_EMAIL,
        conf.ADMIN_EMAIL_PASSWORD
    )
    email_broker = EmailBrokerRepo(smtp_broker)
    await email_broker.connect()
    # ------------------------------------

    await include_routers(app, users, session_pool, cache_pool)

    scheduler = _init_scheduler()
    scheduler.add_job(
        cache_pool.clear_cache,
        IntervalTrigger(seconds=30),
        next_run_time=datetime.now(),
    )
    scheduler.add_job(
        email_broker.distribute_emails,
        IntervalTrigger(seconds=30),
        next_run_time=datetime.now(),
    )

    try:
        config = uvicorn.Config(app, log_level="info", host=conf.BACK_HOST, port=conf.BACK_PORT)
        server = uvicorn.Server(config)
        await server.serve()
    finally:
        scheduler.remove_all_jobs()
        scheduler.shutdown()
        await email_broker.close()
        await cache_pool.close()


def _init_scheduler() -> AsyncIOScheduler:
    """
    Initializes and starts a scheduler.
    """
    scheduler = AsyncIOScheduler(timezone=str(tzlocal.get_localzone()))
    scheduler.start()
    return scheduler


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        pass
