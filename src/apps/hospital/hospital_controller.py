from fastapi import APIRouter, Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.orm import Session
from src.apps.hospital import hospital_schema, hospital_service
from src.lib.database import get_db
from src.lib.jwt import verify_token

router = APIRouter()
auth_scheme = HTTPBearer()

@router.get('/all', summary='모든 병원 정보 조회')
async def getAllHospital(db: Session = Depends(get_db), token: HTTPAuthorizationCredentials = Depends(auth_scheme)):
    verify_token(token.credentials)
    result = await hospital_service.getAllHospital(db)
    return result

@router.get('/:id', summary='병원 정보 조회')
async def getHospital(id: str, db: Session = Depends(get_db), token: HTTPAuthorizationCredentials = Depends(auth_scheme)):
    verify_token(token.credentials)
    result = await hospital_service.getHospital(db, id)
    return result

@router.post('/', summary='병원 정보 등록')
async def createHospital(body: hospital_schema.HospitalPostSchema, db: Session = Depends(get_db), token: HTTPAuthorizationCredentials = Depends(auth_scheme)):
    verify_token(token.credentials)
    result = await hospital_service.createHospital(db, body)
    return result

@router.patch('/:id', summary='병원 정보 수정')
async def updateHospital(id: str, body: hospital_schema.HospitalPostSchema, db: Session = Depends(get_db), token: HTTPAuthorizationCredentials = Depends(auth_scheme)):
    verify_token(token.credentials)
    result = await hospital_service.updateHospital(db, id, body)
    return result

@router.delete('/:id', summary='병원 정보 삭제')
async def deleteHospital(id: str, db: Session = Depends(get_db), token: HTTPAuthorizationCredentials = Depends(auth_scheme)):
    verify_token(token.credentials)
    await hospital_service.deleteHospital(db, id)
    return True

@router.post('/:hospital_id/:patient_id', summary='병원에 환자 등록')
async def hospitalPatient(hospital_id: str, patient_id: str, db: Session = Depends(get_db), token: HTTPAuthorizationCredentials = Depends(auth_scheme)):
    verify_token(token.credentials)
    result = await hospital_service.hospitalPatient(db, hospital_id, patient_id)
    return result