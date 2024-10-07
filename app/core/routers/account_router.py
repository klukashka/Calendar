from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession
from fastapi import APIRouter, Depends
from fastapi_users import FastAPIUsers
from app.schemas.note import NoteCreate
from app.schemas.user import UserRead
from app.db.repositories.note import NoteRepo, _convert_db_note_to_read_note
from app.db.repositories.user import UserRepo


async def get_account_router(users: FastAPIUsers, async_session_maker: async_sessionmaker[AsyncSession]) -> APIRouter:
    """Generate a router with an account route"""
    router = APIRouter()
    async with async_session_maker() as _session:

        note_repo = NoteRepo(_session)
        user_repo = UserRepo(_session)

        @router.post("/account/note_create", status_code=201)
        async def note_create(
                note_to_create: NoteCreate,
                user: UserRead = Depends(users.current_user(active=True))
        ):
            note = await note_repo.add_note(note_to_create, user.id)
            note_to_read = _convert_db_note_to_read_note(note)
            return note_to_read

        @router.get("/account/notes_get")
        async def notes_get(user: UserRead = Depends(users.current_user(active=True))):
            notes = await note_repo.get_notes_by_user_id(user.id)
            return notes

        @router.get("/account/user_info")
        async def get_user_info(user: UserRead = Depends(users.current_user(active=True))):
            user = await user_repo.get_user(user.id)
            return user

        return router
