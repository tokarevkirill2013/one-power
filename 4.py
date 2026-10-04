from fastapi import FastAPI , File , UploadFile ,Request
from fastapi.responses import HTMLResponse
from starlette.templating import Jinja2Templates


app = FastAPI()
templates = Jinja2Templates(directory ="templates")

@app.get("/",response_class = HTMLResponse)
async  def main(requst: Request):
    return templates.TemplateResponse(requst,"HTMl.html")


@app.post("/upload")
async def upload(request: Request, file: UploadFile = File(...)):
    content = await file.read()
    text = content.decode("utf-8")
    return text