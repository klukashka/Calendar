from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends
from fastapi_users import BaseUserManager, IntegerIDMixin
from models.models import User
from fastapi_users.db import SQLAlchemyUserDatabase
from config import SECRET_KEY



class UserManager(IntegerIDMixin, BaseUserManager[User, int]):
    """User info manager (concerning registration and authentication)"""
    reset_password_token_secret = SECRET_KEY
    verification_token_secret = SECRET_KEY


async def get_async_session(async_session_maker) -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        yield session


async def get_user_db(session: AsyncSession = Depends(get_async_session)):
    yield SQLAlchemyUserDatabase(session, User)


async def get_user_manager(user_db=Depends(get_user_db)):
    yield UserManager(user_db)
