from fastapi import APIRouter

from fast_app.api.v1.app.routes import health

api_router = APIRouter()

api_router.include_router(health.router, tags=["Health"])
