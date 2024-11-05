from typing import AsyncGenerator
from sqlalchemy import select, update
from app.models.note import Note as DBNote
from app.models.user import User as DBUser
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import SQLAlchemyError
from datetime import datetime as datetime, timezone
from app.schemas.email import EmailRead
import pytz


class EmailRepo:
    """Repository for database operations concerning emails"""

    def __init__(self, session: AsyncSession):
        self._session = session

    async def get_notes_to_send(self, low: int, high: int) -> AsyncGenerator[EmailRead, None]:
        """Get notes which should be sent (time to remind)"""
        current_time = EmailRepo._utc_cur_time()
        try:
            query = (
                select(DBNote.message, DBUser.email, DBUser.nickname)
                .join(DBNote, (DBUser.id == DBNote.user_id))  # type: ignore
                .where(
                    (DBNote.remind_time <= current_time) &
                    (DBNote.is_completed is False) &
                    (DBNote.important is True)
                )
                .limit(high)
                .offset(low)
            )
            query_result = await self._session.execute(query)
            for row in query_result:
                yield self._convert_db_email_to_read_email(row)
        except SQLAlchemyError as e:
            raise SQLAlchemyError("Failed to get notes from the database") from e

        # ------- mark as completed -------
        await self.update_expired_notes(low, high)
        # ---------------------------------

    async def update_expired_notes(self, low: int, high: int) -> None:
        """Mark all the expired notes as completed"""
        current_time = EmailRepo._utc_cur_time()
        try:
            sub_query = (
                select(DBNote.id)
                .where((DBNote.is_completed is False) & (DBNote.remind_time <= current_time))
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
        except SQLAlchemyError as e:
            raise SQLAlchemyError(f"Failed to update expired notes from {low} to {high}") from e

    async def roll_back(self) -> None:
        await self._session.rollback()

    @staticmethod
    def _convert_db_email_to_read_email(db_email) -> EmailRead:
        return EmailRead(
            message=str(db_email.message) if db_email.message else None,
            email=str(db_email.email) if db_email.email else None,
            nickname=str(db_email.nickname) if db_email.nickname else None,
        )

    @staticmethod
    def _utc_cur_time() -> datetime:
        """Return current time in UTC"""
        local_time = datetime.now(pytz.utc.localize(datetime.now()).tzinfo)
        # Convert to UTC and remove microseconds
        utc_time = local_time.astimezone(timezone.utc).replace(microsecond=0, tzinfo=None)  # to naive
        return utc_time
