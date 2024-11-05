import logging
from typing import List
from app.schemas.note import NoteRead
from app.schemas.user import UserRead
from abc import ABC, abstractmethod


class AbstractCacheStorage(ABC):
    """General implementation of cache storage"""
    _log = logging.getLogger()

    @abstractmethod
    async def connect(self) -> None:
        self._log.debug("Cache storage was connected successfully")

    @abstractmethod
    async def close(self) -> None:
        self._log.debug("Cache storage was closed successfully")

    @abstractmethod
    async def clear_cache(self) -> None:
        self._log.debug("Cache database was cleared successfully")

    @abstractmethod
    async def get_cached_user_info(self, user_id: int) -> None:
        self._log.debug(f"Got cached user info of user {user_id}")

    @abstractmethod
    async def set_cached_user_info(self, user_id: int, user_info: UserRead) -> None:
        self._log.debug(f"Set cached user info {user_info.id} of user {user_id}")

    @abstractmethod
    async def get_cached_user_notes(self, user_id: int) -> None:
        self._log.debug(f"Got cached user notes of user {user_id}")

    @abstractmethod
    async def set_cached_user_note(self, user_id: int, note: NoteRead) -> None:
        self._log.debug(f"Set cached user note {note.id} of user {user_id}")


class CacheRepo(AbstractCacheStorage):
    """Repository pattern for cache storage"""

    def __init__(self, cache_storage: AbstractCacheStorage):
        self._cache_storage = cache_storage

    async def get_cached_user_info(self, user_id: int) -> UserRead | None:
        return await self._cache_storage.get_cached_user_info(user_id)

    async def set_cached_user_info(self, user_id: int, user_info: UserRead) -> None:
        return await self._cache_storage.set_cached_user_info(user_id, user_info)

    async def get_cached_user_notes(self, user_id: int) -> List[NoteRead] | None:
        return await self._cache_storage.get_cached_user_notes(user_id)

    async def set_cached_user_note(self, user_id: int, note: NoteRead) -> None:
        return await self._cache_storage.set_cached_user_note(user_id, note)

    async def clear_cache(self) -> None:
        await self._cache_storage.clear_cache()

    async def connect(self) -> None:
        await self._cache_storage.connect()

    async def close(self) -> None:
        await self._cache_storage.close()
