from fastapi import APIRouter

from fast_app.api.v1.backoffice.routes import customer
from fast_app.api.v1.backoffice.routes import user
from fast_app.api.v1.backoffice.routes import employee
from fast_app.api.v1.backoffice.routes import payment_method
from fast_app.api.v1.backoffice.routes import product

api_router = APIRouter()

api_router.include_router(customer.router, tags=["Backoffice - Customer"])
api_router.include_router(user.router, tags=["Backoffice - User"])
api_router.include_router(employee.router, tags=["Backoffice - Employee"])
api_router.include_router(payment_method.router, tags=["Backoffice - Payment method"])
api_router.include_router(product.router, tags=["Backoffice - Product"])
