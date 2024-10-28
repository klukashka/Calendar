from sqlalchemy import Column, String, Boolean, BigInteger, DateTime, ForeignKey
from app.db.base import Base


class Note(Base):
    """Notes info"""

    __tablename__ = "note"
    id = Column(BigInteger, primary_key=True, unique=True, autoincrement=True)
    user_id = Column(BigInteger, ForeignKey("user.id"))
    remind_time = Column(DateTime(timezone=False), nullable=False) # time when to send a notification
    message = Column(String, nullable=True) # what should be written in a notification
    important = Column(Boolean, nullable=False) # if it is an important one (to send notifications or not)
    is_completed = Column(Boolean, nullable=False, default=False) # to mark a task completed

    def __repr__(self) -> str:
        return (
            f"<Note(id='{self.id}', user_id='{self.user_id}', remind_time='{self.remind_time}', \n"
            f"important='{self.important}', is_completed='{self.is_completed}')>"
        )
