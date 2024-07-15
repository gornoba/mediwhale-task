import os
from fastapi import APIRouter, Depends, HTTPException, UploadFile
from typing import List
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from src import schema, service
from src.core.database import get_db
from sqlalchemy.orm import Session

router = APIRouter()

auth_scheme = HTTPBearer()
@router.post('/ai_url', summary='AI URL 생성')
async def upsertUrl(body: schema.URLModel, db: Session = Depends(get_db)):
    url = body.url
    result = await service.upsertUrl(url, db)
    return result

@router.post('/uploadfile', summary='dcm 파일 업로드')
async def uploadfile(file: UploadFile, db: Session = Depends(get_db)):
    file_extension = os.path.splitext(file.filename)[1]

    if file_extension.lower() != ".dcm":
        raise HTTPException(status_code=400, detail="Invalid file extension. Only '.dcm' files are allowed.")

    result = await service.uploadfile(file, db)

    return result