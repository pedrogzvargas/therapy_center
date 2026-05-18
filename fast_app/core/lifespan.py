from contextlib import asynccontextmanager
from fastapi import FastAPI

@asynccontextmanager
async def lifespan(app: FastAPI):
    # startup
    print("🚀 App starting...")
    yield
    # shutdown
    print("🛑 App shutting down...")
