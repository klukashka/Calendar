from typing import Any, AsyncGenerator, Callable

from fastapi import Depends
from fastapi_users import BaseUserManager, IntegerIDMixin
from fastapi_users.db import BaseUserDatabase, SQLAlchemyUserDatabase
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from app.config import conf
from app.models.user import User


class UserManager(IntegerIDMixin, BaseUserManager[User, int]):
    """User info manager (concerning registration and authentication)"""

    reset_password_token_secret = conf.SECRET_KEY
    verification_token_secret = conf.SECRET_KEY

    # def __init__(self, user_db: BaseUserDatabase[User, int], secret_key: str):
    #     super().__init__(user_db)
    #     self.reset_password_token_secret = secret_key
    #     self.verification_token_secret = secret_key


async def providing_user_manager(
    session_maker: async_sessionmaker[AsyncSession], secret_key: str
) -> Callable[[BaseUserDatabase[User, int]], AsyncGenerator[UserManager, Any]]:
    """
    Function to inject the user manager class instance into FastAPIUsers.
    :param session_maker: async_session_maker to standardize how sessions are configured
    :param secret_key: credential that is used by authentication endpoints to generate additional credentials
    :return get_user_manager: Returns a function to insert a generator into FastAPIUsers.
    """

    async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
        async with session_maker() as session:
            yield session

    async def get_user_db(
        session: AsyncSession = Depends(get_async_session),
    ) -> SQLAlchemyUserDatabase[AsyncSession, User]:
        yield SQLAlchemyUserDatabase(session, User)

    async def get_user_manager(
        user_db: BaseUserDatabase[User, int] = Depends(get_user_db),
    ) -> (AsyncGenerator)[UserManager, Any]:
        yield UserManager(user_db)

    return get_user_manager
