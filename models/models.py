from datetime import datetime
from fastapi_users.db import SQLAlchemyBaseUserTable, SQLAlchemyUserDatabase
from sqlalchemy import Column, String, Boolean, BigInteger, TIMESTAMP
from db.connector import Base


class User(SQLAlchemyBaseUserTable[int], Base):
    """This class describes a table of registered users"""

    __tablename__ = "user"
    id = Column(BigInteger, primary_key=True)
    email = Column(String, nullable=False)
    username = Column(String, nullable=False)
    registered_at = Column(TIMESTAMP, default=datetime.utcnow)
    hashed_password: str = Column(String(length=1024), nullable=False)
    is_active: bool = Column(Boolean, default=True, nullable=False)
    is_superuser: bool = Column(Boolean, default=False, nullable=False)
    is_verified: bool = Column(Boolean, default=False, nullable=False)


class Note(Base):
    """This class describes a table of notes of all time"""

    __tablename__ = "note"
    id = Column(BigInteger, primary_key=True, unique=True, autoincrement=True)
    user_id = Column(BigInteger, nullable=False) # attaches a user
    remind_time = Column(TIMESTAMP, default=datetime.utcnow()) # time when to send a notification
    message = Column(String, nullable=True) # what should be written in a notification
    important = Column(Boolean, nullable=True) # if it is an important one (still unaware of how to use this feature)
    is_completed = Column(Boolean, nullable=False) # to mark a task completed
