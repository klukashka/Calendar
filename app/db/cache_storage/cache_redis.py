import json
from typing import List
from redis import RedisError
from redis.asyncio import Redis
from app.schemas.note import NoteRead
from app.schemas.user import UserRead
from app.db.cache_storage.cache_repo import AbstractCacheStorage


class RedisStorage(AbstractCacheStorage):
    """Redis storage to cache data"""

    def __init__(self, pool: Redis) -> None:
        self._pool = pool

    async def get_cached_user_info(self, user_id: int) -> UserRead | None:
        """Retrieve user info if available else None"""
        key = self._get_user_info_key(user_id)
        try:
            async with self._pool:
                user_info = await self._pool.hgetall(key)
                if not user_info:
                    return None
                user_info = {k.decode(): v.decode() for k, v in user_info.items()}
                return UserRead(**user_info)
        except RedisError as e:
            raise RedisError(f"Failed to get user:{user_id} info by key") from e

    async def set_cached_user_info(self, user_id: int, user_info: UserRead) -> UserRead:
        """Set user info to cache"""
        key = self._get_user_info_key(user_id)
        try:
            async with self._pool:
                await self._pool.hset(key, mapping=user_info.to_dict())
                return user_info
        except RedisError as e:
            raise RedisError(f"Failed to push user:{user_id} info by key") from e

    async def get_cached_user_notes(self, user_id: int) -> List[NoteRead] | None:
        """Retrieve user notes if available else None"""
        key = self._get_user_notes_key(user_id)
        try:
            async with self._pool:
                notes = await self._pool.lrange(key, 0, -1)  # list
                if not notes:
                    return None
                return list(NoteRead(**json.loads(note)) for note in notes)
        except RedisError as e:
            raise RedisError(f"Failed to get user:{user_id} notes by key") from e

    async def set_cached_user_note(self, user_id: int, note: NoteRead) -> NoteRead:
        """Set user notes to cache"""
        key = self._get_user_notes_key(user_id)
        try:
            async with self._pool:
                await self._pool.rpush(key, json.dumps(note.to_dict()))
                return note
        except RedisError as e:
            raise RedisError(f"Failed to set user:{user_id} note{note.id} by key") from e

    async def clear_cache(self) -> None:
        """Remove all cached data"""
        try:
            await self._pool.flushdb()
        except RedisError:
            raise RedisError("Failed to update the cache")

    async def connect(self) -> None:
        if not await self._pool.ping():
            raise RuntimeError("Redis server is not available")

    async def close(self) -> None:
        await self._pool.close()

    @staticmethod
    def _get_user_info_key(user_id: int) -> str:
        return f"user_info:{user_id}"

    @staticmethod
    def _get_user_notes_key(user_id: int) -> str:
        return f"user_notes:{user_id}"
