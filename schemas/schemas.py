from typing import Optional

from fastapi_users import schemas

from pydantic import BaseModel


class UserRead(schemas.BaseUser[int]):
    id: int
    email: str
    username: str
    is_active: bool = True
    is_superuser: bool = False
    is_verified: bool = False

    class Config:
        from_attributes = True


class UserCreate(schemas.BaseUserCreate):
    email: str
    username: str
    password: str
    is_active: Optional[bool] = True
    is_superuser: Optional[bool] = False
    is_verified: Optional[bool] = False


class NoteRead(BaseModel):
    id: int
    user_id: int
    remind_time: str
    message: str
    important: bool
    is_completed: bool

    class Config:
        from_attributes = True


class NoteCreate(BaseModel):
    remind_time: str
    message: str
    important: bool
