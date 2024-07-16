from typing import List
from fastapi import APIRouter, Depends, Query
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.orm import Session
from src.apps.file import file_schema
from src.apps.patient import patient_service
from src.lib.database import get_db
from src.lib.jwt import verify_token

router = APIRouter()
auth_scheme = HTTPBearer()

@router.get('/all/:skip/:limit', summary='모든 환자 정보 조회', response_model=List[file_schema.PatientModelSchema])
async def getAllPatient(
    skip: int = Query(0, description="조회 시작 위치"),
    limit: int = Query(10, description="조회할 항목 수"),
    db: Session = Depends(get_db),
    token: HTTPAuthorizationCredentials = Depends(auth_scheme)
    ):
    verify_token(token.credentials)
    result = await patient_service.getAllPatient(db, skip, limit)
    return result

@router.get('/:id', summary='환자 정보 조회')
async def getPgetAllPatient(id: str, db: Session = Depends(get_db), token: HTTPAuthorizationCredentials = Depends(auth_scheme)):
    verify_token(token.credentials)
    result = await patient_service.getPgetAllPatient(db, id)
    return result