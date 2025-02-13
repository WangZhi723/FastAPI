from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Dict

# 创建 FastAPI 实例
app = FastAPI()

# 定义数据模型
class Item(BaseModel):
    name: str
    description: str = None
    price: float
    tax: float = None

# 模拟数据库
fake_db: Dict[int, Item] = {}

# 获取所有项目
@app.get("/items/", response_model=list[Item])
def read_items():
    return list(fake_db.values())

# 根据 ID 获取单个项目
@app.get("/items/{item_id}", response_model=Item)
def read_item(item_id: int):
    if item_id not in fake_db:
        raise HTTPException(status_code=404, detail="Item not found")
    return fake_db[item_id]

# 创建新项目
@app.post("/items/", response_model=Item, status_code=201)
def create_item(item: Item):
    new_id = max(fake_db.keys(), default=0) + 1
    fake_db[new_id] = item
    return item

# 更新项目
@app.put("/items/{item_id}", response_model=Item)
def update_item(item_id: int, item: Item):
    if item_id not in fake_db:
        raise HTTPException(status_code=404, detail="Item not found")
    fake_db[item_id] = item
    return item

# 删除项目
@app.delete("/items/{item_id}", status_code=204)
def delete_item(item_id: int):
    if item_id not in fake_db:
        raise HTTPException(status_code=404, detail="Item not found")
    del fake_db[item_id]
    return {"message": "Item deleted"}