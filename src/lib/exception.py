from fastapi import Request, HTTPException
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError

async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=400,
        content={"success": False, "errors": exc.errors()},
    )

async def http_exception_handler(request: Request, exc: HTTPException):
    excluded_paths = ['/docs', '/redoc', '/docs-json', '/openapi.json']
    
    # 요청 경로가 제외할 경로에 포함되어 있는지 확인
    if any(path in request.url.path for path in excluded_paths):
        # 기본 HTTPException 처리 방식 사용
        return JSONResponse(
            status_code=exc.status_code,
            content={"detail": exc.detail},
            headers=getattr(exc, "headers", None)
        )

    return JSONResponse(
        status_code=exc.status_code,
        content={"success": False, "message": exc.detail},
    )

async def generic_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content={"success": False, "message": "Internal Server Error"},
    )
