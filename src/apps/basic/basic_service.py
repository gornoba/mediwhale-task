from src.apps.basic import basic_repository
from sqlalchemy.orm import Session
from src.lib import jwt

async def upsertUrl(db: Session, url: str):
    result = await basic_repository.upsertUrl(db, url=url)
    return result

def generateToken():
    jwt_token = jwt.create_jwt_token()
    return jwt_token