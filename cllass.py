from fastapi import FastAPI, Request

app = FastAPI()
NOTES = { }

@app.get("/get/{name}")
async def get_note(request: Request, name: str):
    if not name in NOTES.keys():
        return f"Заметка с именем {name} не найдена"
    return NOTES[name]

@app.post("/add")
async def add_note(name: str, text: str):
    if name in NOTES.keys():
        return f"Заметка с именем {name} уже существует"
    NOTES[name] = text
    return f"Заметка с именем {name} успешно добавлена"