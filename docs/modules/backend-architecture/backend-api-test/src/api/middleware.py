import uuid
from typing import Callable

from fastapi import Request
from fastapi.responses import JSONResponse


async def request_id_middleware(request: Request, call_next: Callable):
    request_id = request.headers.get("X-Request-ID", str(uuid.uuid4()))
    try:
        response = await call_next(request)
    except Exception as exc:  # structured error with request id
        return JSONResponse(
            status_code=500,
            content={
                "error": "InternalServerError",
                "message": "An unexpected error occurred",
                "request_id": request_id,
            },
        )
    response.headers["X-Request-ID"] = request_id
    return response

