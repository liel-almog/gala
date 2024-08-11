from fastapi.exceptions import RequestValidationError
from fastapi import Request, status
from fastapi.responses import JSONResponse


async def request_validation_exception_handler(
    request: Request, exc: RequestValidationError
):
    print(exc)
    try:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"detail": exc.errors()},
        )
    except Exception as _e:
        return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
