from fastapi import HTTPException, status

from sqlalchemy import select, insert
from persistences.postgresql.modules.user.users import users_table
from persistences import utils
from loguru import logger


def user_to_sqldb(user, sqldb):
    logger.info("user data to sqldb")
    stmt_check = select(users_table).where(users_table.c.email == user.email)
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

    stmt = insert(users_table).values(**new_user).returning(users_table)

    user_data = sqldb.execute(stmt).first()
    return user_data
