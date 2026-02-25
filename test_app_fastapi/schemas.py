from pydantic import BaseModel, Field
from typing import Optional


class ItemCreate(BaseModel):
    name: str = Field(..., min_length=1)
    description: Optional[str] = None


class Item(ItemCreate):
    id: int
