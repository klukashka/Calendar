from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession
from fastapi import APIRouter, Depends
from fastapi_users import FastAPIUsers
from app.schemas.note import NoteCreate
from app.schemas.user import UserRead
from app.db.repositories.note import NoteRepo
from app.db.repositories.user import UserRepo
from app.db.redis_storage import *


async def get_account_router(
        users: FastAPIUsers,
        async_session_maker: async_sessionmaker[AsyncSession],
        redis_pool: RedisStorage,
) -> APIRouter:
    """Generate a router with an account route"""

    router = APIRouter()

    async with async_session_maker() as _session:
        note_repo = NoteRepo(_session)
        user_repo = UserRepo(_session)

        @router.post("/account/note_create", status_code=201)
        async def note_create(
                note_to_create: NoteCreate,
                user: UserRead = Depends(users.current_user(active=True)),
                batch_size: int = 10,
        ):
            """Set a new note to cache and database"""
            note = await note_repo.add_note(note_to_create, user.id)
            cached_notes = await redis_pool.get_cached_user_notes(user.id)
            if cached_notes is None:
                async for note in note_repo.get_notes_by_user_id(user.id, 0, batch_size):
                    await redis_pool.set_cached_user_note(user.id, note)
            else:
                await redis_pool.set_cached_user_note(user.id, note)
            return note

        @router.get("/account/notes_get")
        async def notes_get(
                user: UserRead = Depends(users.current_user(active=True)),
                batch_size: int = 10,
        ) -> List[NoteRead]:
            """Retrieve notes from cache or database if the cache is empty"""
            cached_notes = await redis_pool.get_cached_user_notes(user.id)
            if cached_notes is not None:
                return cached_notes
            notes = []  # yet not the best one
            async for note in note_repo.get_notes_by_user_id(user.id, 0, batch_size):
                notes.append(note)
                await redis_pool.set_cached_user_note(user.id, note)
            return notes

        @router.get("/account/user_info")
        async def get_user_info(user: UserRead = Depends(users.current_user(active=True))) -> UserRead:
            """Retrieve user info from cache or database if cache is empty"""
            cached_user_info = await redis_pool.get_cached_user_info(user.id)
            if cached_user_info is not None:
                return cached_user_info
            user = await user_repo.get_user(user.id)
            await redis_pool.set_cached_user_info(user.id, user)
            return user

        return router
