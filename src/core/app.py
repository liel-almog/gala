from contextlib import asynccontextmanager

from fastapi import FastAPI

from src.api.model.event_model import Event
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
    a = await Event.insert_one(Event(name="Liel"))
    b = await Event.find_one({"name": "Liel"}).update_one({"$set": {"age": 22}})
    c = dict(b.raw_result)
    return c
