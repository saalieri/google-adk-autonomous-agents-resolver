from fastapi import FastAPI, HTTPException, status
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from typing import Dict

try:
    from .schemas import ItemCreate, Item
except Exception:
    from schemas import ItemCreate, Item

app = FastAPI(title="Test App FastAPI")


_items: Dict[int, Item] = {}
_next_id = 1

_DEFAULT_ITEMS = [
    {"name": "apple", "description": "A juicy red fruit"},
    {"name": "banana", "description": "Yellow and sweet"},
]

def _load_defaults():
    global _next_id
    for entry in _DEFAULT_ITEMS:
        new_item = Item(id=_next_id, **entry)
        _items[_next_id] = new_item
        _next_id += 1

_load_defaults()

@app.get("/")
def root():
    return {"message": "Welcome Change 3"}

@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/items", response_model=Item, status_code=status.HTTP_201_CREATED)
def create_item(item: ItemCreate):
    global _next_id
    new_item = Item(id=_next_id, **item.dict())
    _items[_next_id] = new_item
    _next_id += 1
    return JSONResponse(
        status_code=status.HTTP_201_CREATED,
        content=jsonable_encoder(new_item),
        headers={"Location": f"/items/{new_item.id}"},
    )


@app.get("/items", response_model=list[Item])
def list_items():
    return list(_items.values())


@app.get("/items/{item_id}", response_model=Item)
def get_item(item_id: int):
    item = _items.get(item_id)
    if not item:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not found")
    return item


@app.put("/items/{item_id}", response_model=Item)
def update_item(item_id: int, item_in: ItemCreate):
    item = _items.get(item_id)
    if not item:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not found")
    updated = Item(id=item_id, **item_in.dict())
    _items[item_id] = updated
    return updated


@app.delete("/items/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_item(item_id: int):
    if item_id not in _items:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not found")
    del _items[item_id]
    return JSONResponse(status_code=status.HTTP_204_NO_CONTENT, content=None)
