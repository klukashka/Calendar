from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from models.models import Note as DBNote
from schemas.note import NoteBase
from sqlalchemy.exc import SQLAlchemyError
from exceptions.repository import DBError


"""There is a user repository to separate database and SQL syntax from functions themselves"""

class NoteRepo:
    """Repository for database operations concerning notes"""
    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session

    async def add_note(self, note: NoteCreate) -> None:
        """This function adds a new note to the database"""
        try:
            db_note = convert_note_to_db_note(note)


    async def get_note(self, note_id: int) -> NoteBase:
        """This function returns a note by its id"""
        try:
            result = await self.db_session.execute(select(DBNote).where(DBNote.id == note_id))
            db_note = result.scalar_one_or_none()  # what is a scalar type?
            return convert_db_note_to_note(db_note)
        except SQLAlchemyError:
            raise DBError("Failed to get the user from the database") from SQLAlchemyError

    async def get_notes_by_user_id(self, user_id: int):

def convert_note_to_db_note(note: NoteRead) -> DBNote:
    return DBNote(id=note.id,
                  user_id=note.user_id,
                  remind_time=note.remind_time,
                  message=note.message,
                  important=note.important,
                  is_completed=note.is_completed
    )

def convert_db_note_to_note(db_note: DBNote) -> NoteRead:
    return NoteBase(
        id=int(db_note.id) if db_note.id else None,
        user_id=int(db_note.user_id) if db_note.user_id else None,
        remind_time=db_note.remind_time if db_note.remind_time else None,
        message=str(db_note.message) if db_note.message else None,
        important=bool(db_note.important) if db_note.important else None,
        is_completed=bool(db_note.is_completed) if db_note.is_completed else None
    )