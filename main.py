import asyncio
import uvicorn
from db.connector import setup_get_pool
from fastapi import FastAPI
from fastapi_users import FastAPIUsers
from auth.auth import auth_backend
from models.User import User
from config import TITLE, DB_URL
from schemas.user import UserRead, UserCreate
from core.routers import account_router
from db.repositories.note import NoteRepo
from db.repositories.user import UserRepo

from auth.manager import providing_user_manager


async def main() -> None:
    """Main function to run app"""
    app = FastAPI(title=TITLE)

    session_pool = await setup_get_pool(DB_URL)

    async with session_pool() as _session:
        user_repo = UserRepo(session=_session)
        note_repo = NoteRepo(session=_session)

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
        account_router.get_account_router(_users, user_repo, note_repo),
        prefix="/account",
        tags=["account"]
    )

    config = uvicorn.Config(app, log_level="info", reload=True)
    server = uvicorn.Server(config)
    await server.serve()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        pass
