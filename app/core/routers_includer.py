from fastapi import FastAPI
from fastapi_users import FastAPIUsers
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from app.auth.auth import auth_backend
from app.core.routers import account_router
from app.db.cache_storage.cache_repo import CacheRepo
from app.models.user import User
from app.schemas.user import UserCreate, UserRead


async def include_routers(
    app: FastAPI,
    users: FastAPIUsers[User, int],
    session_pool: async_sessionmaker[AsyncSession],
    redis_pool: CacheRepo,
):
    app.include_router(
        users.get_auth_router(auth_backend),
        prefix="/auth/jwt",
        tags=["auth"],
    )

    app.include_router(
        users.get_register_router(UserRead, UserCreate),
        prefix="/auth",
        tags=["auth"],
    )

    app.include_router(
        await account_router.get_account_router(users, session_pool, redis_pool),
        tags=["account"],
    )
