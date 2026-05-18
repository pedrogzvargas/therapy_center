from pydantic import BaseModel
from fastapi import Query
from typing import Optional


class PaymentMethod(BaseModel):
    id: str
    name: str
    is_active: bool = True


class PatchPaymentMethod(BaseModel):
    name: Optional[str] = None
    is_active: Optional[bool] = None


class PaymentMethodQueryParams(BaseModel):
    name: Optional[str] = Query(default=None, required=False, description="product name")
    export: Optional[bool] = Query(required=False, default=False)
    limit: Optional[int] = Query(ge=1, le=500000, required=False, default=10)
    page: Optional[int] = Query(ge=1, le=500000, required=False, default=1)
