from typing import AsyncGenerator
from datetime import datetime
from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from app.models.note import Note as DBNote
from app.schemas.note import NoteCreate, NoteRead
from app.config import DATE_TIME_FORMAT
from app.utils.time_manager import utc_cur_time, convert_to_utc, localize


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
                .where((DBNote.user_id == user_id) & (~DBNote.is_completed))  # type: ignore
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
        converted_remind_time = convert_to_utc(note.remind_time, note.time_zone)
        current_time = utc_cur_time()
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
            remind_time_to_return = localize(db_note.remind_time, db_note.time_zone)
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
