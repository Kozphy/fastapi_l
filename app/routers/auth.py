from loguru import logger

from fastapi import (HTTPException,
Depends, Response, status, APIRouter)
from fastapi.security.oauth2 import OAuth2PasswordRequestForm

from persistences.fastapi_dependency.db import get_db
from persistences.postgresql.modules.users import User_table
from persistences.utils import verify, hash

from sqlalchemy.engine import Transaction
from sqlalchemy import text, select, literal_column, insert, delete, update

from routers.validation.fast_api_pydantic.user import User_login
from routers.validation.auth.oauth2 import create_access_token

router = APIRouter(tags=['Authentication'])

@router.post("/login", status_code=status.HTTP_200_OK)
def login(user_cridentials: OAuth2PasswordRequestForm = Depends() ,db: Transaction = Depends(get_db)):

    check_email_stmt = select(User_table).where(User_table.c.email == user_cridentials.username)

    user = db.execute(check_email_stmt).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Invalid Credentials")

    correct_pass_check = verify(user_cridentials.password, user.password)

    if not correct_pass_check:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Invalid Credentials")
    
    # create token
    access_token = create_access_token(data = {"user_id": user.id})

    return {"access_token": access_token, "token_type": "bearer"} 


    


    