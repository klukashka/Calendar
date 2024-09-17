from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession
from fastapi import APIRouter, Depends
from fastapi_users import FastAPIUsers
from app.schemas.note import NoteCreate
from app.schemas.user import UserRead
from app.db.repositories.note import NoteRepo, convert_db_note_to_read_note


async def get_account_router(users: FastAPIUsers, async_session_maker: async_sessionmaker[AsyncSession]) -> APIRouter:
    """Generate a router with an account route"""
    router = APIRouter()
    async with async_session_maker() as _session:

        note_repo = NoteRepo(_session)

        @router.post("/account", status_code=201)
        async def note_create(note_to_create: NoteCreate,
                              user: UserRead = Depends(users.current_user(active=True))
                              ):
            note = await note_repo.add_note(note_to_create, user.id)
            note_to_read = convert_db_note_to_read_note(note)
            return note_to_read

        @router.get("/account")
        async def get_notes(user: UserRead = Depends(users.current_user(active=True))):
            notes = await note_repo.get_notes_by_user_id(user.id)
            return notes

        return router