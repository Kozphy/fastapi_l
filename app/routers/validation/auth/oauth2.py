from jose import JWTError, jwt
from datetime import datetime, timedelta
from loguru import logger


from fastapi import (Depends, status, HTTPException)
from fastapi.security import OAuth2PasswordBearer

from persistences.postgresql.modules.users import User_table
from persistences.fastapi_dependency.db import get_db

from sqlalchemy import select, literal_column, insert, delete, update
from sqlalchemy.engine import Connection, CursorResult


from routers.validation.fast_api_pydantic.auth import TokenData

from configuration.api_service_config.config_fastapi import settings

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

# SECRET_KEY
# Algorithm
# Experation time

SECRET_KEY = settings['jwt_secret'] 
KEY_SALT = settings['jwt_salt']
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

def create_access_token(data: dict):
    to_encode = data.copy()

    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})

    encode_jwt =jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


    return encode_jwt
    
def verify_access_token(token: str, credentials_exception):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

        id: str = payload.get("user_id")

        if id is None:
            raise credentials_exception

        token_data = TokenData(id=id)
    except JWTError:
        raise credentials_exception

    return token_data

def get_current_user(access_token: str = Depends(oauth2_scheme), db: Connection = Depends(get_db)) -> CursorResult:
    credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
    detail=f"Could not validate credentials", headers={"WWW-Authenticate": "Bearer"})

    token_data = verify_access_token(access_token, credentials_exception)
    logger.debug(f'token_data: {token_data}')
    # check access token id whether in database
    stmt = select(User_table).where(User_table.c.id == token_data.id)
    user = db.execute(stmt).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"token credentials is invalid")

    return user