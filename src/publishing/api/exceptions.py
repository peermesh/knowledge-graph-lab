from fastapi import Request
from fastapi.responses import JSONResponse
from datetime import datetime


def problem_detail(status: int, type_url: str, title: str, detail: str, instance: str):
    return {
        "data": {},
        "meta": {
            "timestamp": datetime.utcnow().isoformat(),
        },
        "errors": [
            {
                "type": type_url,
                "title": title,
                "status": status,
                "detail": detail,
                "instance": instance,
            }
        ],
    }


async def rfc7807_exception_handler(request: Request, exc: Exception):
    content = problem_detail(
        status=500,
        type_url="https://api.knowledge-graph-lab.com/errors/internal-server-error",
        title="Internal Server Error",
        detail=str(exc),
        instance=str(request.url),
    )
    return JSONResponse(status_code=500, content=content)
