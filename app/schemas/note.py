from datetime import datetime
from pydantic import BaseModel



class NoteCreate(BaseModel):
    remind_time: str
    message: str
    important: bool


class NoteRead(BaseModel):
    id: int
    user_id: int
    remind_time: datetime
    message: str
    important: bool
    is_completed: bool
