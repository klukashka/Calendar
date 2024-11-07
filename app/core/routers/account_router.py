from typing import List
from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession
from fastapi import APIRouter, Depends
from fastapi_users import FastAPIUsers
from app.schemas.note import NoteCreate, NoteRead
from app.schemas.user import UserRead
from app.db.repositories.note import NoteRepo
from app.db.repositories.user import UserRepo
from app.db.cache_storage.cache_repo import CacheRepo


async def get_account_router(
        users: FastAPIUsers,
        async_session_maker: async_sessionmaker[AsyncSession],
        cache_pool: CacheRepo,
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
        ):
            """Set a new note to cache and database"""
            note = await note_repo.add_note(note_to_create, user.id)
            cached_notes = await cache_pool.get_cached_user_notes(user.id)
            if not cached_notes:
                async for note in note_repo.get_notes_by_user_id(user.id, 0):
                    await cache_pool.set_cached_user_note(user.id, note)
            else:
                await cache_pool.set_cached_user_note(user.id, note)
            return note

        @router.get("/account/notes_get")
        async def notes_get(
                user: UserRead = Depends(users.current_user(active=True)),
        ) -> List[NoteRead]:
            """Retrieve notes from cache or database if the cache is empty"""
            cached_notes = await cache_pool.get_cached_user_notes(user.id)
            if cached_notes:
                return cached_notes
            notes = [note async for note in note_repo.get_notes_by_user_id(user.id, 0)]
            for note in notes:
                await cache_pool.set_cached_user_note(user.id, note)
            return notes

        @router.get("/account/user_info")
        async def get_user_info(user: UserRead = Depends(users.current_user(active=True))) -> UserRead:
            """Retrieve user info from cache or database if cache is empty"""
            cached_user_info = await cache_pool.get_cached_user_info(user.id)
            if cached_user_info:
                return cached_user_info
            user = await user_repo.get_user(user.id)
            await cache_pool.set_cached_user_info(user.id, user)
            return user

        return router
