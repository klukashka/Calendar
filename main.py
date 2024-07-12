from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates

from fastapi import FastAPI, Depends, Request
from fastapi_users import FastAPIUsers

from auth.auth import auth_backend
from auth.database import User
from auth.manager import get_user_manager
from auth.schemas import UserRead, UserCreate

templates = Jinja2Templates(directory="templates")


app = FastAPI(title="Calendar")

fastapi_users = FastAPIUsers[User, int](
    get_user_manager,
    [auth_backend],
)

current_active_user = fastapi_users.current_user(active=True)

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

current_user = fastapi_users.current_user()


@app.get("/account")
def protected_route(request: Request, user: User = Depends(current_active_user)):
    context = {"request": request}
    # add user info inside account page
    return templates.TemplateResponse("account.html", context)


@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    context = {"request": request}
    return templates.TemplateResponse("first_page.html", context)
