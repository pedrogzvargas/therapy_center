from decimal import Decimal
from pydantic import BaseModel
from fastapi import Query
from typing import Optional


class Product(BaseModel):
    id: str
    name: str
    description: str
    price: Decimal
    is_active: bool = True


class PatchProduct(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    price: Optional[Decimal] = None
    is_active: Optional[bool] = True


class ProductQueryParams(BaseModel):
    name: Optional[str] = Query(default=None, required=False, description="product name")
    description: Optional[str] = Query(default=None, required=False, description="product description")
    price: Optional[str] = Query(default=None, required=False, description="product price")
    export: Optional[bool] = Query(required=False, default=False)
    limit: Optional[int] = Query(ge=1, le=500000, required=False, default=10)
    page: Optional[int] = Query(ge=1, le=500000, required=False, default=1)
