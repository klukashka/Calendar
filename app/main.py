import asyncio
import uvicorn
from fastapi.middleware.cors import CORSMiddleware
from app.db.connector import setup_get_pool
from fastapi import FastAPI
from fastapi_users import FastAPIUsers
from app.models.User import User
from app.config import *
from app.auth.auth import auth_backend
from app.auth.manager import providing_user_manager
from app.core.email_sender import EmailSender
from app.core.routers_includer import include_routers
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.interval import IntervalTrigger
import tzlocal


async def main() -> None:
    """Main function to run app"""
    app = FastAPI(title=TITLE)

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

    await include_routers(app, users, session_pool) # includes all the routers

    email_sender = EmailSender(session_pool, ADMIN_EMAIL, ADMIN_EMAIL_PASSWORD, SMTP_PORT, SMTP_SERVER)
    await email_sender.start()

    scheduler = _init_scheduler()

    scheduler.add_job(
        email_sender.super_send,
        IntervalTrigger(seconds=60),
    )

    try:
        config = uvicorn.Config(app, log_level="info", host=BACK_HOST, port=int(BACK_PORT), reload=True)
        server = uvicorn.Server(config)
        await server.serve()
    finally:
       await email_sender.close()

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


# why are some folders empty?
# why is there an _ everywhere at the beginnings of the names
# how to catch errors properly?
# why are all the queries yellow in repos?
# clear config
# should I batch in update queries?
# should do converting in notes

# parametrize ports and hosts on frontend
# add timezone logic everywhere (especially frontend)
# add batching
# convert iterable objects
# how to typify semi-models?
# clear up with timezones. make comparisons work properly
# cannot understand how to select only specific fields from a table
