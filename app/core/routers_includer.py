from app.db.redis_storage import RedisStorage
from app.schemas.user import UserRead, UserCreate
from app.core.routers import account_router
from app.auth.auth import auth_backend
from fastapi import FastAPI
from fastapi_users import FastAPIUsers
from app.models.User import User
from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession


async def include_routers(
        app: FastAPI,
        users: FastAPIUsers[User, int],
        session_pool: async_sessionmaker[AsyncSession],
        redis_pool: RedisStorage,
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
        tags=["account"]
    )
