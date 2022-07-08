from fastapi import HTTPException, Depends, Response, status, APIRouter

from sqlalchemy.engine import Connection
from sqlalchemy import text, select, literal_column, insert, delete, update

from persistences.postgresql.modules.user.users_in_formosa import users_in_formosa_table

from routers.dependency.database.sqlalchemy_db import get_db
from routers.dependency.validation.pydantic.user import (
    User_create,
    User_response,
)
from routers.dependency.validation.auth import oauth2

from modules.user import user_to_sqldb

router = APIRouter(
    prefix="/users",
    tags=["Users"],
)

from loguru import logger


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=User_response)
def create_users(user: User_create, db: Connection = Depends(get_db)):
    logger.info("create user")
    user_data = user_to_sqldb(user, db)
    # print(result)

    user_title = ["id", "email", "password", "created_at"]
    res = {}
    for i, title in enumerate(user_title):
        res.update({title: result[i]})

    return res


@router.get("/{id}", response_model=User_response)
def get_user_info(
    id: int,
    current_user_data: dict = Depends(oauth2.get_current_user),
    db: Connection = Depends(get_db),
):

    current_user_id = current_user_data["id"]

    stmt = select(users_in_formosa_table).where(
        users_in_formosa_table.c.id == id,
        users_in_formosa_table.c.id == current_user_id,
    )

    user = db.execute(stmt).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"user with id: {id} does not exist",
        )

    return user
