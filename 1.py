from fastapi import FastAPI, HTTPException
from typing import List, Dict, Optional  # <-- ВАЖНО: импорт типов
from pydantic import BaseModel

app = FastAPI(title="Сервис товаров")

# Теперь ошибка исчезнет
products_db: List[Dict] = []  # или list[dict]
product_id_counter = 1

class ProductCreate(BaseModel):
    name: str
    price: float
    description: Optional[str] = None

class ProductResponse(BaseModel):
    id: int
    name: str
    price: float
    description: Optional[str] = None

@app.post("/products/", response_model=ProductResponse)
def create_product(product: ProductCreate):
    """Добавить новый товар"""
    global product_id_counter
    if product.price < 0:
        raise HTTPException(status_code=400, detail="Цена не может быть отрицательной")

    new_product = {
        "id": product_id_counter,
        "name": product.name,
        "price": product.price,
        "description": product.description
    }
    products_db.append(new_product)
    product_id_counter += 1
    return new_product


@app.get("/products/", response_model=List[ProductResponse])
def get_all_products():
    """Получить все товары"""
    return products_db


@app.get("/products/search/", response_model=List[ProductResponse])
def search_products(prefix: str):
    """Поиск товаров по началу названия"""
    if not prefix:
        return products_db
    results = [p for p in products_db if p["name"].lower().startswith(prefix.lower())]
    return results


@app.get("/products/{product_id}", response_model=ProductResponse)
def get_product(product_id: int):
    """Получить товар по ID"""
    for product in products_db:
        if product["id"] == product_id:
            return product
    raise HTTPException(status_code=404, detail="Товар не найден")


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8001)