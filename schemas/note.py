from datetime import datetime
from typing import Optional
from fastapi_users import schemas
from pydantic import BaseModel


class UserBase(BaseModel):
    email: int
    username: int
    class Config:
        from_attributes = True


class NoteBase(BaseModel):
    remind_time: str
    message: str
    important: bool
    class Config:
        from_attributes = True


class UserCreate(UserBase, schemas.BaseUserCreate):
    email: str
    username: str
    password: str
    is_active: Optional[bool] = True # what's the use of None (Optional) for this field?
    is_superuser: Optional[bool] = False
    is_verified: Optional[bool] = False


class UserRead(UserBase, schemas.BaseUser[int]):
    id: int
    email: str
    username: str
    is_active: bool = True
    is_superuser: bool = False
    is_verified: bool = False


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
