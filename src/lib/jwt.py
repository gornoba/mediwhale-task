from http.client import HTTPException
from src.lib.joi import settings
import jwt
import uuid
from datetime import datetime, timedelta, timezone
from starlette.middleware.base import BaseHTTPMiddleware

tokens = ['0fcde7ff-e1b8-4fc5-9284-16ee40c93d87']

def create_jwt_token():
    try:
      user_id = str(uuid.uuid4())
      tokens.append(user_id)
      
      expire = datetime.now(timezone.utc) + timedelta(hours=1)
      expire_timestamp = int(expire.timestamp())

      to_encode = {
        "id": '0fcde7ff-e1b8-4fc5-9284-16ee40c93d87',
        "exp": expire_timestamp,
      }

      secret_key = settings.getOrThrow("SECRET_KEY")
      algorithm = settings.getOrThrow("ALGORITHM")

      encoded_jwt = jwt.encode(to_encode, secret_key, algorithm=algorithm)
      return encoded_jwt
    
    except jwt.PyJWTError:
        raise HTTPException(status_code=401, detail="token creation failed")

def verify_token(token: str):
    try:
      secret_key = settings.getOrThrow("SECRET_KEY")
      algorithm = settings.getOrThrow("ALGORITHM")

      payload = jwt.decode(token, secret_key, algorithms=[algorithm])
      user_id: str = payload.get("id")

      if user_id in tokens:
        return user_id
      else:
        raise HTTPException(status_code=401, detail="Invalid token")

    except jwt.PyJWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

