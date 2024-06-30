from fastapi import FastAPI, Request, Form, Response
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates

app = FastAPI()

templates = Jinja2Templates(directory="templates")

users = {"admin": ["123", "admin@"]}


@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    context = {"request": request}
    return templates.TemplateResponse("first_page.html", context)
# пожалуй, стоит сделать функцию redirect_to_page внутри бэкенда


@app.get("/sign_in", response_class=HTMLResponse)
async def sign_in_page(request: Request):
    context = {"request": request}
    return templates.TemplateResponse("sign_in.html", context)


@app.post("/sign_in")
async def sign_in_user(request: Request):
    form = await request.form()
    username = form.get("username")
    password = form.get("password")
    # добавить нормальную аутентификаию
    if username in users and users[username][0] == password:
        # заходить должен на собственную страницу
        return RedirectResponse(url="/account", status_code=303)
    else:
        return templates.TemplateResponse("sign_in.html", {"request": request, "error": True})


@app.get("/account", response_class=HTMLResponse)
async def account_inside(request: Request):
    # session = request.cookies.get("session")
    # if session != "authenticated":
    #     return "Not authenticated"
    context = {"request": request}
    return templates.TemplateResponse("account.html", context)


@app.get("/sign_up", response_class=HTMLResponse)
async def sign_up_page(request: Request):
    context = {"request": request}
    return templates.TemplateResponse("sign_up.html", context)


@app.post("/sign_up")
async def sign_up_user(request: Request):
    form = await request.form()
    username = form.get("username")
    password = form.get("password")
    if username not in users:
        users[username] = [password, "default"]
        return RedirectResponse(url="/", status_code=303)
    else:
        return templates.TemplateResponse("sign_up.html", {"request": request, "error": True})
