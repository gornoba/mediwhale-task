from fastapi import APIRouter, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from src.apps.basic import basic_schema
from src.apps.basic import basic_service
from src.lib.database import get_db
from sqlalchemy.orm import Session

from src.lib.jwt import verify_token

router = APIRouter()
auth_scheme = HTTPBearer()

@router.get('/token_generate',
            summary='토큰 생성',
            description='해당 api를 사용하면 토큰이 발급됩니다. 인메모리를 사용함으로 서버 재시작시 토큰이 초기화 됩니다.<br/>이미 설정된 토큰: eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6IjBmY2RlN2ZmLWUxYjgtNGZjNS05Mjg0LTE2ZWU0MGM5M2Q4NyJ9.mYiUQujOKncU-R2Qn6IgS2b2EKrlUTwjOMplS7sKF5U',
            )
def generateToken():
    token = basic_service.generateToken()
    return token

@router.post('/ai_url', summary='AI URL 생성', response_model=basic_schema.URLModel,)
async def upsertUrl(body: basic_schema.URLModel, db: Session = Depends(get_db), token: HTTPAuthorizationCredentials = Depends(auth_scheme)):
    verify_token(token.credentials)
    url = body.url
    result = await basic_service.upsertUrl(db, url)
    return result