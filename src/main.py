from contextlib import asynccontextmanager
import os
from fastapi import Depends, FastAPI, HTTPException
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.security import HTTPBasicCredentials
from src.lib.database import check_db_connection
from src.lib.exception import generic_exception_handler, http_exception_handler, validation_exception_handler
from src.lib.interceptor import SuccessInterceptor
from src.lib.joi import settings
from src.lib.logger import setup_logging
from src.lib.swaager_auth import verify_credentials
from src.models.model import Base
from src.apps.module import router as items_router
from src.lib.database import engine
from fastapi.openapi.docs import get_swagger_ui_html, get_redoc_html
from fastapi.openapi.utils import get_openapi
import uvicorn

setup_logging()
app = FastAPI(docs_url=None, redoc_url=None, openapi_url=None)


## interceptor 등록
app.add_middleware(SuccessInterceptor)

# # 예외 핸들러 등록
app.add_exception_handler(RequestValidationError, validation_exception_handler)
app.add_exception_handler(HTTPException, http_exception_handler)
app.add_exception_handler(Exception, generic_exception_handler)

# Cors 설정
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

async def init_db():
    async with engine.begin() as conn:
        # 모든 테이블을 드롭하고 다시 생성 (실제 운영 환경에서는 드롭하지 않음)
        await conn.run_sync(Base.metadata.create_all)

@asynccontextmanager
async def lifespan(app: FastAPI):
    # 애플리케이션 시작 시
    await check_db_connection()

    if (settings.getOrThrow('ENV') == 'development'):
        await init_db()

    yield
    # 애플리케이션 종료 시 (필요시 추가 작업)

app.router.lifespan_context = lifespan

# Swagger auth
@app.get("/docs", include_in_schema=False)
async def custom_swagger_ui_html(credentials: HTTPBasicCredentials = Depends(verify_credentials)):
    return get_swagger_ui_html(openapi_url="/openapi.json", title="docs")

@app.get("/redoc", include_in_schema=False)
async def get_redoc_documentation(credentials: HTTPBasicCredentials = Depends(verify_credentials)):
    return get_redoc_html(openapi_url="/openapi.json", title="docs")

@app.get("/docs-json", include_in_schema=False)
async def get_swagger_ui_json(credentials: HTTPBasicCredentials = Depends(verify_credentials)):
    return JSONResponse(get_openapi(title="docs", version="1.0.0", routes=app.routes))

@app.get("/openapi.json", include_in_schema=False)
async def openapi(credentials: HTTPBasicCredentials = Depends(verify_credentials)):
    return get_openapi(title=app.title, version=app.version, routes=app.routes)

# router 및 prefix 설정
app.include_router(items_router, prefix="/api")

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=settings.getOrThrow('PORT'), reload=True if settings.getOrThrow('ENV') == 'development' else False, workers=1)
