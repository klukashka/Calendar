from fastapi import APIRouter, Depends
from fastapi_users import FastAPIUsers
from schemas.note import NoteCreate
from schemas.user import UserRead
from db.repositories.user import UserRepo
from db.repositories.note import NoteRepo, convert_db_note_to_read_note


def get_account_router(users: FastAPIUsers, user_repo: UserRepo, note_repo: NoteRepo) -> APIRouter:
    """Generate a router with an account route"""
    router = APIRouter()

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