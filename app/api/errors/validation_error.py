from fastapi import Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
import json


async def request_validation_exception_handler(
    request: Request, exc: RequestValidationError
):
    try:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"detail": json.loads(json.dumps(exc.errors(), default=str))},
        )
    except Exception as _e:
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content="Internal Server Error",
        )
