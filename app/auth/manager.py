from typing import AsyncGenerator, Any
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker
from fastapi import Depends
from fastapi_users import BaseUserManager, IntegerIDMixin
from models.User import User
from fastapi_users.db import SQLAlchemyUserDatabase
from config import SECRET_KEY


class UserManager(IntegerIDMixin, BaseUserManager[User, int]):
    """User info manager (concerning registration and authentication)"""
    reset_password_token_secret = SECRET_KEY
    verification_token_secret = SECRET_KEY

async def providing_user_manager(session_maker: async_sessionmaker[AsyncSession]):
    """
    Function to inject the user manager class instance into FastAPIUsers.
    :param session_maker: async_session_maker to standardize how sessions are configured
    :return get_user_manager: Returns a function to insert a generator into FastAPIUsers.
    """
    async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
        async with session_maker() as session:
            yield session

    async def get_user_db(session: AsyncSession = Depends(get_async_session)):
        yield SQLAlchemyUserDatabase(session, User)

    async def get_user_manager(user_db = Depends(get_user_db)) -> AsyncGenerator[UserManager, Any]:
        yield UserManager(user_db)

    return get_user_manager
