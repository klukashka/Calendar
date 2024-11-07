from typing import List
from datetime import datetime

from pydantic import BaseModel


class NoteRead(BaseModel):
    id: int
    user_id: int
    remind_time: datetime
    time_zone: str
    message: str
    important: bool
    is_completed: bool


class UserRead(BaseModel):
    id: int
    email: str
    nickname: str
    is_active: bool = True
    is_superuser: bool = False
    is_verified: bool = False


class MockCacheStorage:
    def __init__(self):
        self.cache = {}

    def connect(self) -> None:
        pass

    def close(self) -> None:
        del self.cache

    def clear_cache(self) -> None:
        self.cache.clear()

    def get_cached_user_info(self, user_id: int) -> UserRead | None:
        key = self._get_user_info_key(user_id)
        try:
            return self.cache[key]
        except KeyError:
            return None

    def set_cached_user_info(self, user_id: int, user_info: UserRead) -> UserRead:
        key = self._get_user_info_key(user_id)
        self.cache[key] = user_info
        return user_info

    def get_cached_user_notes(self, user_id: int) -> List[NoteRead]:
        key = self._get_user_notes_key(user_id)
        if self.cache[key]:
            return self.cache[key]
        else:
            return []

    def set_cached_user_note(self, user_id: int, note: NoteRead) -> NoteRead:
        key = self._get_user_notes_key(user_id)
        if self.cache[key]:
            self.cache[key].append(note)
        else:
            self.cache[key] = [note]
        return note

    @staticmethod
    def _get_user_info_key(user_id: int) -> str:
        return f"user_info:{user_id}"

    @staticmethod
    def _get_user_notes_key(user_id: int) -> str:
        return f"user_notes:{user_id}"


def test_cache_00():
    user1 = UserRead(
        id=1,
        email='user1@mail.com',
        is_active=True,
        is_superuser=False,
        is_verified=False,
        nickname='user1',
    )
    store = MockCacheStorage()
    store.set_cached_user_info(user1.id, user1)
    assert store.get_cached_user_info(user1.id) == user1
    store.clear_cache()
    assert store.get_cached_user_info(user1.id) is None
    store.close()
