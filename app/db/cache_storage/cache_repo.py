import logging
from typing import List
from app.schemas.note import NoteRead
from app.schemas.user import UserRead
from abc import ABC, abstractmethod


class AbstractCacheStorage(ABC):
    """General implementation of cache storage"""

    @abstractmethod
    async def connect(self) -> None:
        raise NotImplementedError

    @abstractmethod
    async def close(self) -> None:
        raise NotImplementedError

    @abstractmethod
    async def clear_cache(self) -> None:
        raise NotImplementedError

    @abstractmethod
    async def get_cached_user_info(self, user_id: int) -> None:
        raise NotImplementedError

    @abstractmethod
    async def set_cached_user_info(self, user_id: int, user_info: UserRead) -> None:
        raise NotImplementedError

    @abstractmethod
    async def get_cached_user_notes(self, user_id: int) -> None:
        raise NotImplementedError

    @abstractmethod
    async def set_cached_user_note(self, user_id: int, note: NoteRead) -> None:
        raise NotImplementedError


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
