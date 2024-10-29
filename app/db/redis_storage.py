import json
from typing import List, Any
from redis import RedisError
from redis.asyncio import Redis
from app.schemas.note import NoteRead
from app.schemas.user import UserRead


class RedisStorage:
    """Storage to cache data"""

    def __init__(self, host: str, port: int, db: int, password: str | None = None) -> None:
        self._host = host
        self._port = port
        self._db = db
        self._password = password
        self._pool: Redis = Redis(
            host=host,
            port=port,
            db=db,
            password=password,
            decode_responses=True,
        )

    async def get_cached_user_info(self, user_id: int) -> UserRead | None:
        """Retrieve user info if available else None"""
        try:
            async with self._pool:
                key = self._key("user_info", user_id)
                user_info = await self._pool.hgetall(key)
                if len(user_info) == 0:
                    return None
                return UserRead(**user_info)
        except RedisError:
            raise RedisError("Failed to get user info by key")

    async def set_cached_user_info(self, user_id: int, user_info: UserRead) -> UserRead:
        """Set user info to cache"""
        try:
            async with self._pool:
                key = self._key("user_info", user_id)
                await self._pool.hset(key, mapping=user_info.to_dict())
                return user_info
        except RedisError:
            raise RedisError("Failed to push user info by key")

    async def get_cached_user_notes(self, user_id: int) -> List[NoteRead] | None:
        """Retrieve user notes if available else None"""
        try:
            async with self._pool:
                key = self._key("user_notes", user_id)
                notes = await self._pool.hgetall(key)  # dict
                if len(notes) == 0:
                    return None
                return sorted(
                    list((NoteRead(**json.loads(note)) for note in notes.values())),  # not the best one
                    key=lambda note: note.remind_time
                )
        except RedisError:
            raise RedisError("Failed to get user notes by key")

    async def set_cached_user_note(self, user_id: int, note: NoteRead) -> NoteRead:
        """Set user notes to cache"""
        try:
            async with self._pool:
                key = self._key("user_notes", user_id)
                retrieved_data = await self._pool.hgetall(key)
                notes = {k: json.loads(v) for k, v in retrieved_data.items()}
                notes[str(note.id)] = note.to_dict()
                for note_id, notes_item in notes.items():
                    await self._pool.hset(key, note_id, json.dumps(notes_item))
                return note
        except RedisError:
            raise RedisError("Failed to set user note by key")

    async def clear_cache(self):
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
    def _key(*key: Any) -> str:
        return ":".join(map(str, key))
