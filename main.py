from typing import Annotated

from datetime import datetime

from fastapi.templating import Jinja2Templates

from fastapi import FastAPI, Depends, Request, Form, Body, HTTPException
from fastapi_users import FastAPIUsers

from auth.auth import auth_backend
from db.database import User, Note, get_async_session
from auth.manager import get_user_manager
from schemas.schemas import *

from sqlalchemy.ext.asyncio import AsyncSession

from models.models import note


templates = Jinja2Templates(directory="templates")

app = FastAPI(title="Calendar")

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


@app.get("/account")
async def account(user: User = Depends(current_active_user)):
    return f"Hello, {user.username}"


# @app.post("/account/create", response_model=NoteRead)
# async def note_create(db_session: Session, note_to_create: NoteCreate, user: User = Depends(current_active_user)):
#     date_time_format = "%H:%M %d.%m.%Y"
#     if datetime.strptime(note_create.remind_time, date_time_format):
#         raise HTTPException(status_code=406, detail="Wrong date-time data format")
#     new_note = Note(user_id=user.id,
#                     remind_time=note_to_create.remind_time,
#                     message=note_to_create.message,
#                     important=note_to_create.important,
#                     is_complited=False)
#     db_session.add(new_note)
#     db_session.commit()
#     db_session.refresh(new_note)
#     return new_note


@app.post("/account/note_create")
async def note_create(note_to_create: NoteCreate,
                      db_session: AsyncSession = Depends(get_async_session),
                      user: User = Depends(current_active_user)
                      ) -> None:
    date_time_format = "%H:%M %d.%m.%Y"
    if not datetime.strptime(note_to_create.remind_time, date_time_format):
        raise HTTPException(status_code=406, detail="Wrong date-time data format")
    new_note = Note(user_id=user.id,
                    remind_time=note_to_create.remind_time,
                    message=note_to_create.message,
                    important=note_to_create.important,
                    is_completed=False)
    db_session.add(new_note)
    await db_session.commit()

#20:30 20.12.2024