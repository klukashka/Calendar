from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import select
from models.models import User as DBUser
from schemas.note import UserRead
from exceptions.repository import DBError

"""There is a user repository to separate database and SQL syntax from functions themselves"""

class UserRepo:
    """Repository for database operations concerning user"""
    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session # why do you use _session not session

    async def yield_user_db():

    async def get_user(self, user_id: int) -> Optional[UserRead]:
        try:
            result = await self.db_session.execute(select(DBUser).where(DBUser.id==user_id)) # is there any difference between filter and where
            db_user = result.scalar_one_or_none() # what is a scalar type?
            return convert_db_user_to_user(db_user)
        except SQLAlchemyError:
            raise DBError("Failed to get the user from the database") from SQLAlchemyError # what does this "from" do
                                                                                           # to see the root of the error?


def convert_db_user_to_user(db_user: DBUser) -> UserRead:
    return UserRead(
        id=int(str(db_user.id)), # why to convert it?
        email=str(db_user.email) if db_user.email else None,
        username=str(db_user.username) if db_user.username else None,
        is_active=bool(db_user.is_active) if db_user.is_active else None,
        registered_at=db_user.registered_at if db_user.registered_at else None,
        is_superuser=bool(db_user.is_superuser) if db_user.is_superuser else None,
        is_verified=bool(db_user.is_verified) if db_user.is_verified else None
       )
