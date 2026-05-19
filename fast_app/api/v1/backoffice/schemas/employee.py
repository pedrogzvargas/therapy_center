from pydantic import BaseModel
from fastapi import Query
from typing import Optional


class Employee(BaseModel):
    id: str
    name: str
    last_name: str
    second_last_name: str | None = None
    username: str
    password: str
    is_active: bool = True


class EmployeeQueryParams(BaseModel):
    name: Optional[str] = Query(default=None, required=False, description="employee name")
    last_name: Optional[str] = Query(default=None, required=False, description="employee last name")
    second_last_name: Optional[str] = Query(default=None, required=False, description="employee second last name")
    export: Optional[bool] = Query(required=False, default=False)
    limit: Optional[int] = Query(ge=1, le=500000, required=False, default=10)
    page: Optional[int] = Query(ge=1, le=500000, required=False, default=1)
