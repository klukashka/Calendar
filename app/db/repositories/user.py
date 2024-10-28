from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import select
from app.models.User import User as DBUser
from app.schemas.user import UserRead
from app.exceptions.repository import DBError


class UserRepo:
    """Repository for database operations concerning user"""

    def __init__(self, session: AsyncSession):
        self._session = session

    async def get_user(self, user_id: int) -> Optional[UserRead]:
        """Get user info by id"""
        try:
            result = await self._session.execute(select(DBUser).where(DBUser.id == user_id))  # type: ignore
            db_user = result.scalar_one_or_none()
            return self._convert_db_user_to_user(db_user)
        except SQLAlchemyError:
            raise DBError("Failed to get the user from the database") from SQLAlchemyError

    @staticmethod
    def _convert_db_user_to_user(db_user: DBUser) -> UserRead:
        return UserRead(
            id=int(str(db_user.id)) if db_user.id else None,
            email=str(db_user.email) if db_user.email else None,
            nickname=str(db_user.nickname) if db_user.nickname else None,
            is_active=bool(db_user.is_active),
            registered_at=db_user.registered_at if db_user.registered_at else None,
            is_superuser=bool(db_user.is_superuser),
            is_verified=bool(db_user.is_verified),
        )
