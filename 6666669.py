from fastapi import FastAPI, Form
from starlette.responses import HTMLResponse

app = FastAPI()

with open("templates/45.html", "r", encoding='utf-8') as file:
    main_page = file.read()


@app.get("/", response_class=HTMLResponse)
async def show_form():
    return main_page

@app.post("/answer")
async def show_results(name: str = Form(...),
                       email: str = Form(...),
                       password: str = Form(...),
                       age: int = Form(...)):
    if len(password) < 10:
        return "Длина пароля должна быть как минимум 10 символов"

    return f"Пользователь с именем {name} зарегистрировался с почтой {email} с паролем длины в {len(password)} символов. Возраст пользователя {age} лет."
