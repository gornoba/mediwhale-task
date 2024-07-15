from fastapi import APIRouter
from src.controller import router as items_router

router = APIRouter()

# 서비스와 컨트롤러 통합
router.include_router(items_router)
