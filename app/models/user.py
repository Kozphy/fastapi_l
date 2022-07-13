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
from attrs import define
from typing import Any
from collections import namedtuple


@define
class Node_value:
    data: list[str, Any]
    stmt: tuple[Any]


def user_to_sqldb(user, sqldb: Connection):
    logger.info("user data to sqldb")
    logger.debug(user)
    # check email
    try:
        stmt_check_email = select(users_in_formosa_table).where(
            users_in_formosa_table.c.email == user.email
        )
        check_email = sqldb.execute(stmt_check_email).first()
    except Exception as e:
        logger.error(e)
        raise e

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
    try:
        ## TODO: insert value to table
        # insert_table
        insert_table = [
            users_detail_in_formosa_table,
            users_in_formosa_table,
        ]
        stmt_insert_value = [
            {
                "surname": new_user["surname"],
                "given_name": new_user["given_name"],
                "gender": new_user["gender"],
                "formosa_id_card_letter": new_user["id_card"][0],
                "formosa_id_card": new_user["id_card"][1:],
                "address1": new_user["address1"],
                "address2": new_user["address2"],
                "address3": new_user["address3"],
                "country": new_user["country"],
                "city": new_user["city"],
                "region": new_user["region"],
                "zip_code": new_user["zip_code"],
                "country_code": new_user["country_code"],
                "subscriber_number": new_user["subscriber_number"],
                "description": new_user["description"],
            },
            {
                "email": new_user["email"],
                "password": new_user["password"],
            },
        ]
        table_returning = []
        for i, table in enumerate(insert_table):
            # stmt_insert_value = namedtuple(table.name, {})
            # logger.debug(type(table.name))
            stmt_insert = insert(table).values(stmt_insert_value[i]).returning(table)

            result = sqldb.execute(stmt_insert).first()
            table_returning.append(result)

        logger.debug(table_returning)

        ## data to users_in_formosa
        # stmt_insert = {
        #     "insert": (
        #         insert(users_in_formosa_table)
        #         .values(**stmt_insert["value"])
        #         .returning(users_in_formosa_table)
        #     ),
        # }

    ## data to users_detail_in_formosa
    # stmt_insert["value"] = {}

    # users_in_formosa_data = sqldb.execute(stmt_insert["insert"]).first()
    except Exception as e:
        logger.error(e)
        raise e

    return None
