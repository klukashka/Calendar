from dataclasses import dataclass
from typing import Optional
from datetime import datetime
from pydantic import BaseModel
from app.config import DATE_TIME_FORMAT


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

    def to_dict(self):
        return {
            'id': str(self.id),
            'user_id': str(self.user_id),
            'remind_time': str(datetime.strftime(self.remind_time, DATE_TIME_FORMAT)),
            'message': str(self.message),
            'important': str(self.important),
            'is_completed': str(self.is_completed),
        }
