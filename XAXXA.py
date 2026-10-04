from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import uvicorn


#МЫ тупые,  наш код - фигня


app = FastAPI()
templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse) async def main(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/register", response_class=HTMLResponse)
async def register(request: Request,
                name: str = Form(...),
                secondName: str = Form(...),
                password: str = Form(...),
                checkbox: str = Form(...),
               ):

    return templates.TemplateResponse("profile.html")

if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8020)