from contextlib import asynccontextmanager

from fastapi import FastAPI

from src.core.db import start_async_mongo
from ..api.routes import api_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    await start_async_mongo()
    yield


app = FastAPI(title="Optimus Gala", lifespan=lifespan)
app.include_router(router=api_router, prefix="/api")


@app.get("/")
async def get():
    return "health"
