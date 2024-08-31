from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from exceptions.repository import ModelExists
from models.Note import Note as DBNote
from schemas.note import NoteCreate, NoteRead
from exceptions.repository import DBError
from config import DATE_TIME_FORMAT
from datetime import datetime as datetime


"""There is a user repository to separate database and SQL syntax from functions themselves"""

class NoteRepo:
    """Repository for database operations concerning notes"""
    def __init__(self, session: AsyncSession):
        self.session = session

    async def add_note(self, note: NoteCreate, user_id: int) -> DBNote:
        """This function adds a new note to the database"""
        try:
            db_note = convert_create_note_to_db_note(note, user_id)
            self.session.add(db_note)
            await self.session.commit()
            return db_note
        except IntegrityError as e:
            raise ModelExists("Failed to add note to the database") from e
        except SQLAlchemyError as e:
            raise DBError("Failed to add note to the database") from e

    async def get_note(self, note_id: int) -> NoteRead:
        """This function returns a note by its id"""
        try:
            result = await self.session.execute(select(DBNote).where(DBNote.id == note_id))
            db_note = result.scalar_one_or_none()  # what is a scalar type?
            return convert_db_note_to_read_note(db_note)
        except SQLAlchemyError:
            raise DBError("Failed to get the note from the database") from SQLAlchemyError

    async def get_notes_by_user_id(self, _user_id: int):
        try:
            query = select(DBNote).where(DBNote.user_id==_user_id and DBNote.is_completed==False)
            result = await self.session.execute(query)
            return result.mappings().all()
        except SQLAlchemyError:
            raise DBError("Failed to get the note from the database") from SQLAlchemyError
        # memory limit exceeded


def convert_read_note_to_db_note(note: NoteRead) -> DBNote:
    return DBNote(id=note.id,
                  user_id=note.user_id,
                  remind_time=note.remind_time,
                  message=note.message,
                  important=note.important,
                  is_completed=note.is_completed
    )

def convert_create_note_to_db_note(note: NoteCreate, user_id: int) -> DBNote:
    if not datetime.strptime(note.remind_time, DATE_TIME_FORMAT):
        raise HTTPException(status_code=406, detail="Wrong date-time data format")
    converted_remind_time = datetime.strptime(note.remind_time, DATE_TIME_FORMAT)
    if converted_remind_time < datetime.now():
        raise HTTPException(status_code=406, detail="Inappropriate time value")
    # temporary solution
    # I should get rid of these exceptions and use buttons
    return DBNote(user_id=user_id,
                  remind_time=converted_remind_time,
                  message=note.message,
                  important=note.important,
                  is_completed=False
    )

def convert_db_note_to_read_note(db_note: DBNote) -> NoteRead:
    return NoteRead(
        id=int(str(db_note.id)) if db_note.id else None,
        user_id=int(str(db_note.user_id)) if db_note.user_id else None,
        remind_time=db_note.remind_time if db_note.remind_time else None,
        message=str(db_note.message) if db_note.message else None,
        important=bool(db_note.important),
        is_completed=bool(db_note.is_completed)
    )