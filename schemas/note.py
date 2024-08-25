from datetime import datetime
from typing import Optional
from fastapi_users import schemas
from pydantic import BaseModel


class NoteBase(BaseModel):
    remind_time: str
    message: str
    important: bool
    class Config:
        from_attributes = True


class NoteCreate(NoteBase):
    remind_time: str
    message: str
    important: bool


class NoteRead(NoteBase):
    id: int
    user_id: int
    remind_time: datetime
    message: str
    important: bool
    is_completed: bool
