from fastapi import HTTPException, Depends, Response, status, APIRouter

from sqlalchemy.engine import Connection
from sqlalchemy import text, select, literal_column, insert, delete, update

from persistences.postgresql.modules.users import users_table
from persistences import utils

from routers.dependency.database.sqlalchemy_db import get_db
from routers.dependency.validation.pydantic.user import (
    User_create,
    User_response,
)
from routers.dependency.validation.auth import oauth2

router = APIRouter(
    prefix="/users",
    tags=["Users"],
)


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=User_response)
def create_users(user: User_create, db: Connection = Depends(get_db)):
    stmt_check = select(users_table).where(users_table.c.email == user.email)
    check_email = db.execute(stmt_check).first()
    if check_email:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"{user.email} email already exists",
        )

    # hash the password - user.password
    hash_password = utils.hash(user.password)
    user.password = hash_password

    new_user = user.dict()
    # print(new_user)
    stmt = insert(users_table).values(**new_user).returning(users_table)

    result = db.execute(stmt).first()
    user_title = ["id", "email", "password", "created_at"]
    # print(result)
    res = {}
    for i, title in enumerate(user_title):
        res.update({title: result[i]})

    return res


@router.get("/{id}", response_model=User_response)
def get_user(
    id: int,
    current_user_data: dict = Depends(oauth2.get_current_user),
    db: Connection = Depends(get_db),
):

    current_user_id = current_user_data["id"]

    stmt = select(users_table).where(
        users_table.c.id == id, users_table.c.id == current_user_id
    )

    user = db.execute(stmt).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"user with id: {id} does not exist",
        )

    return user
