from typing import Optional
from datetime import datetime
from pydantic import BaseModel
from app.config import DATE_TIME_FORMAT


class NoteCreate(BaseModel):
    remind_time: str
    message: str
    important: Optional[bool] = True
    time_zone: str


class NoteRead(BaseModel):
    id: int
    user_id: int
    remind_time: datetime
    time_zone: str
    message: str
    important: bool
    is_completed: bool

    def to_dict(self):
        return {
            'id': str(self.id),
            'user_id': str(self.user_id),
            'remind_time': str(datetime.strftime(self.remind_time, DATE_TIME_FORMAT)),
            'time_zone': str(self.time_zone),
            'message': str(self.message),
            'important': str(self.important),
            'is_completed': str(self.is_completed),
        }
