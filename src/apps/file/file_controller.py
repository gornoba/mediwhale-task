import os
from fastapi import APIRouter, Depends, HTTPException, UploadFile
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from src.apps.file import file_schema
from src.apps.file import file_service
from src.lib.database import get_db
from sqlalchemy.orm import Session
from src.lib.jwt import verify_token

router = APIRouter()
auth_scheme = HTTPBearer()

@router.post('/uploadfile', summary='dcm 파일 업로드', response_model=file_schema.PatientModelSchema)
async def uploadfile(file: UploadFile, db: Session = Depends(get_db), token: HTTPAuthorizationCredentials = Depends(auth_scheme)):
    verify_token(token.credentials)
    file_extension = os.path.splitext(file.filename)[1]

    if file_extension.lower() != ".dcm":
        raise HTTPException(status_code=400, detail="Invalid file extension. Only '.dcm' files are allowed.")

    result = await file_service.uploadfile(file, db)
    return result