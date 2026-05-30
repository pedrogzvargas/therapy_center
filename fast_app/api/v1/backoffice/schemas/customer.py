from pydantic import BaseModel
from pydantic import EmailStr
from fastapi import Query
from typing import Optional


class Customer(BaseModel):
    id: str
    name: str
    last_name: str
    second_last_name: str | None = None
    email: EmailStr
    password: str
    is_active: bool = True


class CustomerQueryParams(BaseModel):
    name: Optional[str] = Query(default=None, required=False, description="customer name")
    last_name: Optional[str] = Query(default=None, required=False, description="customer last name")
    second_last_name: Optional[str] = Query(default=None, required=False, description="customer second last name")
    export: Optional[bool] = Query(required=False, default=False)
    limit: Optional[int] = Query(ge=1, le=500000, required=False, default=10)
    page: Optional[int] = Query(ge=1, le=500000, required=False, default=1)
