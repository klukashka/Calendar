import os
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

app = FastAPI()

domain_template_directory = "templates"
templates = Jinja2Templates(directory=domain_template_directory)


@app.get("/sign_in/", response_class=HTMLResponse)
async def sign_in(request: Request):
    context = {"request": request}
    return templates.TemplateResponse("sign_in.html", context)
