from fastapi import FastAPI

app = FastAPI()
ITEMS = list()


@app.post("/add")
async def add_item(name: str):
    if name in ITEMS:
        return f"Товар с именем {name} уже существует"

    ITEMS.append(name)
    return f"Товар {name} успешно добавлен"


@app.get("/search")
async def search_items(name_prefix: str):
    found_items = list()
    for item in ITEMS:
        if item.startswith(name_prefix):
            found_items.append(item)

    return found_items