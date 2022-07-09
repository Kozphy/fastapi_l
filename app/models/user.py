from fastapi import HTTPException, status

from sqlalchemy import select, insert
from persistences.postgresql.modules.user.users_in_formosa import users_in_formosa_table
from persistences.postgresql.modules.user.users_detail_in_formosa import (
    users_detail_in_formosa_table,
)
from persistences.postgresql.modules.user.users_status import users_status_table
from routers.dependency.security import utils
from loguru import logger

from sqlalchemy.engine import Connection


def user_to_sqldb(user, sqldb: Connection):
    logger.info("user data to sqldb")
    logger.debug(user)
    # exit()
    # check email
    stmt_check = select(users_in_formosa_table).where(
        users_in_formosa_table.c.email == user.email
    )
    check_email = sqldb.execute(stmt_check).first()
    if check_email:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"{user.email} email already exists",
        )

    # hash the password - user.password
    hash_password = utils.hash(user.password)
    user.password = hash_password

    new_user = user.dict()
    logger.debug(f"new user is {new_user}")

    ## TODO: insert value to table
    # insert_table
    insert_table = [
        users_in_formosa_table,
        users_detail_in_formosa_table,
        users_status_table,
    ]

    for table in insert_table:

        sqldb.execute().first()

    ## data to users_in_formosa
    stmt_insert = {
        "value": {
            "email": new_user["email"],
            "password": new_user["password"],
        },
        "insert": (
            insert(users_in_formosa_table)
            .values(**stmt_insert["value"])
            .returning(users_in_formosa_table)
        ),
    }

    ## data to users_detail_in_formosa
    stmt_insert["value"] = {}

    users_in_formosa_data = sqldb.execute(stmt_insert["insert"]).first()

    return None
