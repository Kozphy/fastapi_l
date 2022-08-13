from fastapi import HTTPException, Depends, Response, status, APIRouter, BackgroundTasks

from sqlalchemy.engine import Connection
from sqlalchemy import text, select, literal_column, insert, delete, update

from persistences.postgresql.modules.user.users_outline import (
    users_table,
)

from routers.dependency.database.sqlalchemy_db import get_db
from routers.dependency.pydantic.user import (
    User_create,
    User_response,
)
from routers.dependency.security import oauth2

from models.user import user_to_sqldb, account_to_proper_sqldb_table

router = APIRouter(
    prefix="/users",
    tags=["Users"],
)


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=User_response)
def create_users(
    user: User_create,
    background_tasks: BackgroundTasks,
    db: Connection = Depends(get_db),
):
    logger.info("create user")
    sql_return_data = user_to_sqldb(user, db)
    # background_tasks.add_task(account_to_proper_sqldb_table, sql_return_data, db)

    db.commit()
    # print(result)

    # user_title = ["id", "email", "password", "created_at"]
    # res = {}
    # for i, title in enumerate(user_title):
    #     res.update({title: result[i]})

    # return res


@router.get("/{id}", response_model=User_response)
def get_user_info(
    id: int,
    current_user_data: dict = Depends(oauth2.get_current_user),
    db: Connection = Depends(get_db),
):

    current_user_id = current_user_data["id"]

    stmt = select(users_table).where(
        users_table.c.id == id,
        users_table.c.id == current_user_id,
    )

    user = db.execute(stmt).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"user with id: {id} does not exist",
        )

    return user
