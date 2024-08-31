from sqlalchemy import Column, String, Boolean, BigInteger, DateTime, ForeignKey

from db.base import Base

class Note(Base):
    """This class describes a table of notes of all time"""

    __tablename__ = "note"
    id = Column(BigInteger, primary_key=True, unique=True, autoincrement=True)
    user_id = Column(BigInteger, ForeignKey("user.id"))
    remind_time = Column(DateTime(timezone=True), nullable=False) # time when to send a notification
    message = Column(String, nullable=True) # what should be written in a notification
    important = Column(Boolean, nullable=True) # if it is an important one (still unaware of how to use this feature)
    is_completed = Column(Boolean, nullable=False, default=False) # to mark a task completed

    def __repr__(self) -> str:
        return f"Note: {self.id} | {self.user_id}, {self.remind_time}, {self.important}, {self.is_completed}"