from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError

from app.api.errors.validation_error import request_validation_exception_handler
from app.core.db import start_async_mongo
from app.core.logger import setup_logger
from ..api.routes import api_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    setup_logger()
    await start_async_mongo()
    yield


app = FastAPI(title="Optimus Gala", lifespan=lifespan)
app.add_exception_handler(RequestValidationError, request_validation_exception_handler)
app.include_router(router=api_router, prefix="/api")


@app.get("/health")
async def health():
    return "Health"
