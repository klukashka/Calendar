from typing import AsyncGenerator
from sqlalchemy import select, update
from app.models.Note import Note as DBNote
from app.models.User import User as DBUser
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import SQLAlchemyError
from app.exceptions.repository import DBError
from datetime import datetime as datetime, timedelta, timezone
from app.schemas.email import EmailRead


class EmailRepo:
    """Repository for database operations concerning emails"""

    def __init__(self, session: AsyncSession):
        self._session = session

    async def get_notes_to_send(self, low: int, high: int) -> AsyncGenerator[EmailRead, None]:
        """Get notes which should be sent (time to remind)"""
        try:
            current_time = datetime.now()
            query = (
                select(DBNote.message, DBUser.email, DBUser.nickname)
                .join(DBNote, (DBUser.id == DBNote.user_id))  # type: ignore
                .where((DBNote.remind_time <= current_time) &
                       (DBNote.is_completed == False) &
                       (DBNote.important == True))
                .limit(high)
                .offset(low)
            )
            for row in await self._session.execute(query):
                yield self._convert_db_email_to_read_email(row)

            # ------- mark as completed -------
            await self.update_expired_notes(low, high)
            # ---------------------------------

        except SQLAlchemyError:
            raise DBError("Failed to get notes from the database") from SQLAlchemyError

    async def update_expired_notes(self, low: int, high: int):
        """Mark all the expired notes as completed"""
        current_time = datetime.now()
        sub_query = (
            select(DBNote.id)
            .where((DBNote.is_completed == False) & (DBNote.remind_time <= current_time))
            .limit(high)
            .offset(low)
        )
        update_query = (
            update(DBNote)
            .filter(DBNote.id.in_(sub_query))
            .values(is_completed=True)
        )
        await self._session.execute(update_query)
        await self._session.commit()

    @staticmethod
    def _convert_db_email_to_read_email(db_email) -> EmailRead:
        return EmailRead(
            message=str(db_email.message) if db_email.message else None,
            email=str(db_email.email) if db_email.email else None,
            nickname=str(db_email.nickname) if db_email.nickname else None,
        )
