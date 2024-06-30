from fastapi import FastAPI, Request, Form, Response
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates

app = FastAPI()

templates = Jinja2Templates(directory="templates")


@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    context = {"request": request}
    return templates.TemplateResponse("index.html", context)
# пожалуй, стоит сделать функцию redirect_to_page внутри бэкенда


@app.get("/sign_in", response_class=HTMLResponse)
async def sign_in_page(request: Request):
    context = {"request": request}
    return templates.TemplateResponse("sign_in.html", context)


@app.post("/sign_in")
async def sign_in_user(response: Response, username: str = Form(...), password: str = Form(...)):
    if username == "admin" and password == "123":
        return RedirectResponse(url="/account", status_code=303)
    else:
        return "Invalid Data"


@app.get("/account", response_class=HTMLResponse)
async def account_inside(request: Request):
    # session = request.cookies.get("session")
    # if session != "authenticated":
    #     return "Not authenticated"
    context = {"request": request}
    return templates.TemplateResponse("account.html", context)
