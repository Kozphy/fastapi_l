from loguru import logger

from fastapi import HTTPException, Depends, Response, status, APIRouter
from fastapi.security.oauth2 import OAuth2PasswordRequestForm

from persistences.postgresql.modules.users import users_table
from persistences.utils import verify, hash

from sqlalchemy.engine import Connection
from sqlalchemy import text, select, literal_column, insert, delete, update

from routers.dependency.database.sqlalchemy_db import get_db
from routers.dependency.validation.pydantic.auth import Token
from routers.dependency.validation.auth.oauth2 import create_access_token

router = APIRouter(tags=["Authentication"])


@router.post("/login", status_code=status.HTTP_200_OK, response_model=Token)
def login(
    user_cridentials: OAuth2PasswordRequestForm = Depends(),
    db: Connection = Depends(get_db),
):

    check_email_stmt = select(users_table).where(
        users_table.c.email == user_cridentials.username
    )

    user = db.execute(check_email_stmt).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail=f"Invalid Credentials"
        )

    correct_pass_check = verify(user_cridentials.password, user.password)

    if not correct_pass_check:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail=f"Invalid Credentials"
        )

    # create token
    access_token = create_access_token(data={"user_id": user.id})

    return {"access_token": access_token, "token_type": "bearer"}
