import asyncio
import uvicorn
from fastapi.middleware.cors import CORSMiddleware

from app.schemas.user import UserRead, UserCreate
from app.db.connector import setup_get_pool
from fastapi import FastAPI
from fastapi_users import FastAPIUsers
from app.models.User import User
from app.config import TITLE, DB_URL, BACK_HOST, BACK_PORT, FRONT_HOST, FRONT_PORT
from app.core.routers import account_router
from app.auth.auth import auth_backend
from app.auth.manager import providing_user_manager


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

    _users = FastAPIUsers[User, int](
        await providing_user_manager(session_pool),
        [auth_backend],
    )

    app.include_router(
        _users.get_auth_router(auth_backend),
        prefix="/auth/jwt",
        tags=["auth"],
    )

    app.include_router(
        _users.get_register_router(UserRead, UserCreate),
        prefix="/auth",
        tags=["auth"],
    )

    app.include_router(
        await account_router.get_account_router(_users, session_pool),
        tags=["account"]
    )

    config = uvicorn.Config(app, log_level="info", host=BACK_HOST, port=int(BACK_PORT), reload=True)
    server = uvicorn.Server(config)
    await server.serve()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        pass

# attach a scheduler
# add config file to use variables for ports

# make register page send fetch
# send user data to /account