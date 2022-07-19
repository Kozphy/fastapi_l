from fastapi import HTTPException, status

from sqlalchemy import select, insert, or_
from sqlalchemy.engine import Connection

from persistences.postgresql.modules.user import (
    users_account,
    users_address,
    users_country,
    users_id_card_in_formosa,
    users_outline,
    users_registration,
    users_status,
)
from routers.dependency.security import utils
from loguru import logger

from attrs import define
from typing import Any
from collections import namedtuple


@define
class Node_value:
    data: list[str, Any]
    stmt: tuple[Any]


def check_whether_input_account(user):
    account_check_none = {
        "sum_none": 0,
        "email": 0,
        "phone": 0,
        "username": 0,
    }
    for account in account_check_none.keys():
        if user[account] is None:
            account_check_none["sum_none"] += 1
            account_check_none[account] += 1

    if account_check_none["sum_none"] == 3:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="please input account"
        )
    return account_check_none


def check_email_exist(user, sqldb: Connection):
    # check account
    stmt_check_email = select(users_registration.users_register_table).where(
        or_(
            users_registration.users_register_table.c.registration == user["email"],
            users_registration.users_register_table.c.registration == user["phone"],
            users_registration.users_register_table.c.registration == user["username"],
        )
    )
    check_email = sqldb.execute(stmt_check_email).first()
    return check_email


def user_to_sqldb(user, sqldb: Connection):
    logger.info("user data to sqldb")
    logger.debug(user)
    user = user.dict()
    try:
        # password check
        if user["password"] != user["password_check"]:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="please check your password field value, \
                whether same as password check field value.",
            )

        account_check_none = check_whether_input_account(user)
        check_email = check_email_exist(user, sqldb)
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

    logger.debug(f"Now user with password: {user}")
    try:
        ## TODO: insert value to table
        stmt_insert_t_v = {
            users_outline.users_table: {
                "surname": user["surname"],
                "password": user["password"],
                "given_name": user["given_name"],
                "description": user["description"],
            },
            users_registration.users_register_table: {},
            # users_country.users_country_table: {
            #     "country": user["country"],
            #     "country_code": user["country_code"],
            # },
            # users_id_card_in_formosa.users_id_card_in_formosa_table: {
            #     "gender": user["gender"],
            #     "formosa_id_card_letter": user["id_card"][0],
            #     "formosa_id_card": user["id_card"][1:],
            #     "subscriber_number": user["subscriber_number"],
            # },
            # users_address.users_address_table: {
            #     "city": user["city"],
            #     "region": user["region"],
            #     "address1": user["address1"],
            #     "address2": user["address2"],
            #     "address3": user["address3"],
            #     "zip_code": user["zip_code"],
            # },
        }

        ## add not None account to stmt_insert_t_v
        for account, v in account_check_none.items():
            if v == 0:
                stmt_insert_t_v[users_registration.users_register_table].update(
                    {account: user[account]}
                )

        ## TODO: 7/18 Anchor point
        stmt_insert_t_r = {
            users_outline.users_table: {},
            users_registration.users_register_table: {},
        }
        table_returned = []
        for table, value in stmt_insert_t_v.items():
            # stmt_insert_value = namedtuple(table.name, {})
            # logger.debug(type(table.name))
            stmt_insert = insert(table).values(**value).returning(table)

            table_return = sqldb.execute(stmt_insert).first()._asdict()
            if table == users_detail_in_formosa_table:
                logger.debug(
                    f"users_detail_in_formosa_table return is : {table_return}"
                )
                stmt_insert_t_v[users_in_formosa_table].update(
                    {"user_detail_in_formosa_id": table_return["id"]}
                )
            table_returned.append(table_return)

        logger.debug(table_returned)

    except Exception as e:
        logger.error(e)
        raise e

    return None
