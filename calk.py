from fastapi import FastAPI, Request, Form
from starlette.responses import HTMLResponse
from starlette.templating import Jinja2Templates

app = FastAPI()
templates = Jinja2Templates(directory="templates")


@app.get("/", response_class=HTMLResponse)
async def show_root(request: Request):
    values = { "result": None }
    return templates.TemplateResponse(request, "calculator.html", values)

@app.post("/calculate", response_class=HTMLResponse)
async def calculate(request: Request,
                    num1: float = Form(...),
                    num2: float = Form(...),
                    operation: str = Form(...)):
    if operation == "add":
        result = num1 + num2
    elif operation == "subtract":
        result = num1 - num2
    elif operation == "multiply":
        result = num1 * num2
    elif operation == "divide":
        result = num1 / num2
    values = { "result": result }
    return templates.TemplateResponse(request, "calculator.html", values)