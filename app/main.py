import logging
import asyncio
from datetime import datetime
import uvicorn
import tzlocal
from fastapi.middleware.cors import CORSMiddleware
from app.db.connector import setup_get_pool
from fastapi import FastAPI
from fastapi_users import FastAPIUsers
from app.email_broker.email_broker import SMTPBroker
from app.models.user import User
from app.config import *
from app.auth.auth import auth_backend
from app.auth.manager import providing_user_manager
from app.email_broker.email_broker_repo import EmailBrokerRepo
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
        level=LOG_LEVEL,
        filename=LOG_FILE,
    )

    app = FastAPI()

    session_pool = await setup_get_pool(DB_URL)

    origins = [
        f"http://{FRONT_HOST}:{FRONT_PORT}",
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
        host=REDIS_HOST,
        port=int(REDIS_PORT),
        db=int(REDIS_DB),
        password=REDIS_PASS,
    )
    redis_storage = RedisStorage(redis)
    cache_pool = CacheRepo(redis_storage)
    await cache_pool.connect()
    # -----------------------------------
    # -------- Email broker -------------
    mail = SMTP(port=EMAIL_PORT, hostname=EMAIL_SERVER)
    smtp_broker = SMTPBroker(
        mail,
        session_pool,
        ADMIN_EMAIL,
        ADMIN_EMAIL_PASSWORD
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
        config = uvicorn.Config(app, log_level="info", host=BACK_HOST, port=int(BACK_PORT))
        server = uvicorn.Server(config)
        await server.serve()
    finally:
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
