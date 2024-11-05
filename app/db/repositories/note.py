from typing import AsyncGenerator
from datetime import datetime as datetime
from datetime import timezone
from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from app.models.note import Note as DBNote
from app.schemas.note import NoteCreate, NoteRead
from app.config import DATE_TIME_FORMAT
import pytz


class NoteRepo:
    """Repository for database operations concerning notes"""

    def __init__(self, session: AsyncSession):
        self._session = session
        self._read_batch_size = 10

    async def add_note(self, note: NoteCreate, user_id: int) -> NoteRead:
        """Add a new note to the database"""
        try:
            db_note = self._convert_create_note_to_db_note(note, user_id)
            self._session.add(db_note)
            await self._session.commit()
            return self._convert_db_note_to_read_note(db_note)
        except SQLAlchemyError as e:
            raise SQLAlchemyError("Failed to add a note to the database") from e

    async def get_note(self, note_id: int) -> NoteRead:
        """Return a note by its id"""
        try:
            result = await self._session.execute(select(DBNote).where(DBNote.id == note_id))  # type: ignore
            db_note = result.scalar_one_or_none()
            return self._convert_db_note_to_read_note(db_note)
        except SQLAlchemyError as e:
            raise SQLAlchemyError(f"Failed to get the note:{note_id} from the database") from e

    async def get_notes_by_user_id(
            self,
            user_id: int,
            cursor: int,
    ) -> AsyncGenerator[NoteRead, None]:
        """Get all user notes by user id"""
        try:
            query = (
                select(DBNote)
                .where((DBNote.user_id == user_id) & (DBNote.is_completed == False))  # type: ignore
                .limit(cursor + self._read_batch_size)
                .offset(cursor)
                .order_by(DBNote.remind_time.asc())
            )
            for row in await self._session.execute(query):
                yield self._convert_db_note_to_read_note(row[0])
        except SQLAlchemyError as e:
            raise SQLAlchemyError(f"Failed to get the notes of user:{user_id} from the database") from e

    @staticmethod
    def _convert_read_note_to_db_note(note: NoteRead) -> DBNote:
        return DBNote(
            id=note.id,
            user_id=note.user_id,
            remind_time=note.remind_time,
            time_zone=note.time_zone,
            message=note.message,
            important=note.important,
            is_completed=note.is_completed,
        )

    @staticmethod
    def _convert_create_note_to_db_note(note: NoteCreate, user_id: int) -> DBNote:
        if not datetime.strptime(note.remind_time, DATE_TIME_FORMAT):
            raise HTTPException(status_code=406, detail="Wrong date-time data format")
        converted_remind_time = NoteRepo._convert_to_utc(note.remind_time)
        current_time = NoteRepo._utc_cur_time()
        # print(repr(current_time), "- cur", "||||", repr(converted_remind_time), "- conv")
        if converted_remind_time < current_time:
            raise HTTPException(status_code=406, detail="Inappropriate time value")
        return DBNote(
            user_id=user_id,
            remind_time=converted_remind_time,
            time_zone=note.time_zone,
            message=note.message,
            important=note.important,
            is_completed=False,
        )

    @staticmethod
    def _convert_db_note_to_read_note(db_note: DBNote) -> NoteRead:
        if db_note.remind_time:
            # print(db_note.time_zone, " time zone")
            remind_time_to_return = NoteRepo._localize(db_note.remind_time, db_note.time_zone)
        else:
            remind_time_to_return = None
        return NoteRead(
            id=int(str(db_note.id)) if db_note.id else None,
            user_id=int(str(db_note.user_id)) if db_note.user_id else None,
            remind_time=remind_time_to_return,
            time_zone=str(db_note.time_zone) if db_note.time_zone else None,
            message=str(db_note.message) if db_note.message else None,
            important=bool(db_note.important),
            is_completed=bool(db_note.is_completed),
        )

    @staticmethod
    def _utc_cur_time() -> datetime:
        """Return current time in UTC"""
        local_time = datetime.now(pytz.utc.localize(datetime.now()).tzinfo)
        # Convert to UTC and remove microseconds
        utc_time = local_time.astimezone(timezone.utc).replace(microsecond=0, tzinfo=None)  # to naive
        return utc_time

    @staticmethod
    def _localize(dt: datetime, tz: str) -> datetime:
        """Convert aware datetime to necessary time zone"""
        local_tz = pytz.timezone(tz)
        try:
            in_utc_time = pytz.utc.localize(dt)
            local_time = in_utc_time.astimezone(local_tz)
            return local_time
        except ValueError as e:
            raise ValueError(f"Failed to convert {dt}. Expected aware datetime") from e

    @staticmethod
    def _convert_to_utc(dt: str) -> datetime:
        formatted_datetime = datetime.strptime(dt, DATE_TIME_FORMAT)
        converted_datetime = formatted_datetime.astimezone(pytz.utc)
        converted_datetime = converted_datetime.replace(tzinfo=None)  # convert to naive
        return converted_datetime
