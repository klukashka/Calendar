from typing import Optional
from datetime import datetime
from pydantic import BaseModel


class NoteCreate(BaseModel):
    remind_time: str
    message: str
    important: Optional[bool] = True


class NoteRead(BaseModel):
    id: int
    user_id: int
    remind_time: datetime
    message: str
    important: bool
    is_completed: bool
