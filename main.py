from typing import Annotated

from datetime import datetime

from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates

from fastapi import FastAPI, Depends, Request, Form, Body, HTTPException
from fastapi_users import FastAPIUsers

from auth.auth import auth_backend
from db.database import User
from auth.manager import get_user_manager
from auth.schemas import UserRead, UserCreate

from sqlalchemy.orm import Session

from models.models import note

from db.database import get_user_db

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

# app.include_router(notes_router)

current_active_user = fastapi_users.current_user(active=True)


@app.get("/account")
def account(user: User = Depends(current_active_user)):
    return f"Hello, {user.username}"


@app.get("/account/create")
async def note_create(remind_time: Annotated[str, Body(embed=True)],
                      message: Annotated[str, Form()],
                      important: Annotated[bool, Form()],
                      db_session: Session = Depends(get_user_db)
                      ):
    date_time_format = "%H:%M %d.%m.%Y"
    if datetime.strptime(remind_time, date_time_format):
        raise HTTPException(status_code=406, detail="Wrong date-time data format")
    new_note = note(user_id=current_active_user.id,
                    remind_time=remind_time,
                    message=message,
                    important=important,
                    is_complited=False)
    db_session.add(new_note)
    db_session.commit()
