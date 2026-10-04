
from fastapi import FastAPI,Request

from starlette.responses import HTMLResponse

from starlette.templating import Jinja2Templates

from datetime import datetime

from random import randint

app = FastAPI()
templates = Jinja2Templates(directory="templates")
PAGE_VISITS = 0 @app.get("/", response_class=HTMLResponse)
async def show_root(request: Request):
    global PAGE_VISITS PAGE_VISITS += 1 values = { "title": "Заголовок", "message": "Это тренировочный сайт", "badge": "Сайт на FastAPI", "author": "Дмитрий", "category": "Задача на FastAPI", "status": "ОК", "current_date": datetime.now().strftime("%d-%m-%y"), "current_time": datetime.now().strftime("%H:%M:%S"), "page_visits": PAGE_VISITS, "random_number": randint(1, 100) }
    return templates.TemplateResponse(request, "complex_templated_page.html", values)