from datetime import datetime

from utils.EmailSender import EmailSender

from fastapi import FastAPI, Depends, Request, Form, Body, HTTPException
from fastapi_users import FastAPIUsers

from auth.auth import auth_backend
from db.database import User, Note, get_async_session
from auth.manager import get_user_manager

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from schemas.schemas import *


app = FastAPI(title="Calendar")

email_sender = EmailSender()
email_sender.start()
# email_sender.send("klukin0202@yandex.ru", "mailcheck", "it's me")

fastapi_users = FastAPIUsers[User, int](
    get_user_manager,
    [auth_backend],
)

# https://github.com/fastapi-users/fastapi-users/blob/master/fastapi_users/router/auth.py
app.include_router(
    fastapi_users.get_auth_router(auth_backend),
    prefix="/auth/jwt",
    tags=["auth"],
)
# https://github.com/fastapi-users/fastapi-users/blob/master/fastapi_users/router/register.py
app.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="/auth",
    tags=["auth"],
)

current_active_user = fastapi_users.current_user(active=True)


@app.post("/account", status_code=201, response_model=NoteCreate)
async def note_create(note_to_create: NoteCreate,
                      db_session: AsyncSession = Depends(get_async_session),
                      user: User = Depends(current_active_user)
                      ) -> NoteCreate:
    date_time_format = "%H:%M %d.%m.%Y"
    if not datetime.strptime(note_to_create.remind_time, date_time_format):
        raise HTTPException(status_code=406, detail="Wrong date-time data format")
    converted_remind_time = datetime.strptime(note_to_create.remind_time, "%H:%M %d.%m.%Y")
    if converted_remind_time < datetime.now():
        raise HTTPException(status_code=406, detail="Inappropriate time value")
    new_note = Note(user_id=user.id,
                    remind_time=converted_remind_time,
                    message=note_to_create.message,
                    important=note_to_create.important,
                    is_completed=False)
    db_session.add(new_note)
    await db_session.commit()
    return note_to_create


# 20:30 20.12.2024
# 20:40 20.12.2024

@app.get("/account")
async def get_notes(db_session: AsyncSession = Depends(get_async_session),
                    user: User = Depends(current_active_user)
                    ):
    rows = await db_session.execute(select(Note).where(Note.user_id == user.id))
    rows = list(rows.scalars())
    print(type(rows))
    return rows
