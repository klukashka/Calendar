from fastapi_users.db import SQLAlchemyBaseUserTable
from sqlalchemy import Column, String, Boolean, BigInteger, func, DateTime

from app.db.base import Base


class User(SQLAlchemyBaseUserTable[int], Base):
    """Table of registered users"""

    __tablename__ = "user"
    id = Column(BigInteger, primary_key=True)
    email = Column(String, nullable=False)
    nickname = Column(String, nullable=False)
    registered_at = Column(DateTime(timezone=True), default=func.now())
    hashed_password: str = Column(String(length=1024), nullable=False)
    is_active: bool = Column(Boolean, default=True, nullable=False)
    is_superuser: bool = Column(Boolean, default=False, nullable=False)
    is_verified: bool = Column(Boolean, default=False, nullable=False)

    def __repr__(self) -> str:
        return (
            f"<User(id='{self.id}', email='{self.email}', \n"
            f"nickname='{self.nickname}', registered_at='{self.registered_at}')>"
        )
