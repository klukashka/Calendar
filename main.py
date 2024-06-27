from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

app = FastAPI()

domain_template_directory = "templates"
templates = Jinja2Templates(directory=domain_template_directory)


@app.get("/first_page/", response_class=HTMLResponse)
async def create_user(request: Request):
    context = {"request": request}
    return templates.TemplateResponse("first_page.html", context)
# надо обработать две кнопки "регистрация" и "вход" и потом выкидывать на нужную страницу
# после регистрации выкидывать на первую страницу, сообщив об успешной регистрации


@app.get("/sign_up/", response_class=HTMLResponse)
async def create_user(request: Request):
    context = {"request": request}
    return templates.TemplateResponse("sign_up.html", context)


@app.get("/sign_in/", response_class=HTMLResponse)
async def sign_in(request: Request):
    context = {"request": request}
    return templates.TemplateResponse("sign_in.html", context)


@app.get("/account/", response_class=HTMLResponse)
async def create_user(request: Request):
    context = {"request": request}
    return templates.TemplateResponse("account.html", context)

