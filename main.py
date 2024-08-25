import asyncio
import uvicorn
import core.routers.account_router
from db.connector import setup_get_pool
from fastapi import FastAPI, Depends, Request, Form, Body, HTTPException
from fastapi_users import FastAPIUsers
from auth.auth import auth_backend
from models.models import User
from auth.manager import get_user_manager, get_async_session
from schemas.auth import *
from config import DATABASE_URL

async def main() -> None:
    """Main function to run app"""
    app = FastAPI(title="Calendar")

    fastapi_users = FastAPIUsers[User, int](
        get_user_manager,
        [auth_backend],
    )

    app.include_router(
        fastapi_users.get_auth_router(auth_backend),
        prefix="/auth/jwt",
        tags=["auth"],
    )

    app.include_router(
        fastapi_users.get_register_router(UserRead, UserCreate),
        prefix="/auth",
        tags=["auth"],
    )

    app.include_router(
        core.routers.account_router.get_account_router(),
        prefix="/account",
        tags=["account"]
    )

    # connect db
    session_pool = await setup_get_pool(DATABASE_URL)

    #

    config = uvicorn.Config("main:app", port=5000, log_level="info")
    server = uvicorn.Server(config)
    await server.serve()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        pass

# https://github.com/fastapi-users/fastapi-users/blob/master/fastapi_users/router/register.py
# https://github.com/fastapi-users/fastapi-users/blob/master/fastapi_users/router/auth.py


# make one more router for account handler to keep there those ^ functions
# understand how to throw db_session to a function without throwing it
# make a good main func
# understand how to deal with a database and orm
# do smth with a scheduler
# git: how to move file to another folder without losing its history of changing and commits?
# add logging
# how to get rid of those table-classes
# what is metadata?
# what is __call__ method? makes an object behave like a func
# why there was db_urI????????? not urL
# what is "future" parameter in create_async_engine
# what is engine.begin()
# what is context manager
# why to use __repr__ in database classes
# how to select files for .gitignore
# about config in .env and python logging
# what to do with get_async_session
# what are logs written to?
# what is MIT license
# if I rearrange files, all the imports get wrong. What should I do?
# what is model_db_mixin
# learn how to Makefile
# how make correct .env file
# where to store secret_key generator for password hashing (or how to generate it)
# __main__
# where is fastapi.db SQLAlchemyUserDatabase in docs?
# Don't forget to ask about server
