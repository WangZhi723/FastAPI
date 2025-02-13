from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Dict

app = FastAPI()

class Item(BaseModel):
    name: str
    description: str = None
    price: float
    tax: float = None

fake_db: Dict[int, Item] = {}

@app.get("/items/", response_model=list[Item])
def read_items():
    return list(fake_db.values())

@app.get("/items/{item_id}", response_model=Item)
def read_item(item_id: int):
    if item_id not in fake_db:
        raise HTTPException(status_code=404, detail="Item not found")
    return fake_db[item_id]

@app.post("/items/", response_model=Item, status_code=201)
def create_item(item: Item):
    new_id = max(fake_db.keys(), default=0) + 1
    fake_db[new_id] = item
    return item