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
from enums.register import Register
from routers.dependency.security import utils
from loguru import logger

from attrs import define
from typing import Any


@define
class Node_value:
    data: list[str, Any]
    stmt: tuple[Any]


def check_whether_input_account(user):
    sum_none = 0
    ## if account input exist, following value will equal input value and
    ## if account input not exist, sum_none will increase 1.
    account_input_exist = {
        "email": False,
        "phone": False,
        "username": False,
    }
    for account in account_input_exist.keys():
        if user[account] is None or user[account] == "":
            sum_none += 1
            del user[account]
        else:
            account_input_exist[account] = user[account]

    if sum_none == 3:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="please input what account do you want.",
        )
    return user, account_input_exist


def check_account_exist(user, account_input_exist: dict, sqldb: Connection):
    stmt_where = []
    for account, v in account_input_exist.items():
        if v != False:
            stmt_where.append(
                users_registration.users_register_table.c.registration == user[account]
            )

    # check account
    stmt_check_account = select(
        users_registration.users_register_table.c.registration
    ).where(or_(*stmt_where))
    check_account = sqldb.execute(stmt_check_account).first()
    return check_account


def insert_to_table(data, table, returning, sqldb: Connection):
    if returning is None:
        stmt_insert = insert(table).values(**data)
        sqldb.execute(stmt_insert)
    else:
        stmt_insert = insert(table).values(**data).returning(*returning)
        table_return = sqldb.execute(stmt_insert).first()._asdict()

    return table_return


# TODO: phone number convert to comply database format
def user_to_sqldb(user, sqldb: Connection):
    logger.info("user data to sqldb")
    logger.debug(user)
    user = user.dict()
    try:
        # password check whether equal
        if user["password"] != user["password_check"]:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="please check your password field value, \
                whether same as password check field value.",
            )
        del user["password_check"]
        user, account_input_exist = check_whether_input_account(user)
        check_account = check_account_exist(user, account_input_exist, sqldb)
    except Exception as e:
        logger.error(e)
        raise e

    if check_account:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"{check_account.registration} already exists",
        )

    # hash the password - user.password
    hash_password = utils.hash(user["password"])
    user["password"] = hash_password

    logger.debug(f"Now user with password: {user}")

    # construct what data want to insert to database table
    try:
        stmt_insert_t_v = {
            users_outline.users_table: {
                "surname": user["surname"],
                "password": user["password"],
                "given_name": user["given_name"],
                "description": user["description"],
            },
            users_registration.users_register_table: {},
        }

        # what values do you want to return from database
        stmt_insert_t_r = {
            users_outline.users_table: [
                users_outline.users_table.c.id,
            ],
            users_registration.users_register_table: [
                users_registration.users_register_table.c.registration,
                users_registration.users_register_table.c.registration_type,
            ],
        }

        sql_return_data = {}

        ## add not None account to stmt_insert_t_v
        for account, v in account_input_exist.items():
            if v != False:
                stmt_insert_t_v[users_registration.users_register_table].update(
                    {
                        "registration": user[account],
                        "registration_type": Register[account],
                    }
                )
    except Exception as e:
        logger.error(e)
        raise e

    # execute sql stmt
    try:
        for table, value in stmt_insert_t_v.items():
            returning_check = stmt_insert_t_r.get(table, None)
            # if returning_check is not None:
            table_return = insert_to_table(value, table, returning_check, sqldb)
            logger.debug(f"table_name: {table.name}")
            logger.debug(f"table_return: {table_return}")
            sql_return_data.update({table.name: table_return})

            if table == users_outline.users_table:
                logger.debug(f"users_table return is : {table_return}")
                stmt_insert_t_v[users_registration.users_register_table].update(
                    {"user_id": table_return["id"]}
                )

        logger.debug(f"sql_return_data is: {sql_return_data}")
    except Exception as e:
        logger.error(e)
        raise e
    return sql_return_data


def account_to_proper_sqldb_table(sql_return_data: dict, sqldb: Connection):
    """

    Args:
        sql_return_data (dict): {"id": 1, "email": 123@gmail.com}
        sqldb (Connection): _description_

    Raises:
        e: _description_
    """
    try:
        table_map = {
            "email": users_account.users_email_table,
            "mobile": users_account.users_phone_table,
            "username": users_account.users_username_table,
        }
        stmt_insert_t_v = {}
        # stmt_insert_t_r = {}
        for key, value in sql_return_data.items():
            if key in ["email", "username"]:
                stmt_insert_t_v.update(
                    {
                        table_map[key]: {
                            "user_id": sql_return_data["id"],
                            key: value,
                        }
                    }
                )
            if key in ["mobile"]:
                stmt_insert_t_v.update(
                    {
                        table_map[key]: {
                            "user_id": sql_return_data["id"],
                            "user_country_id": sql_return_data["user_country_id"],
                            "subscriber_number": sql_return_data["subscriber_number"],
                        }
                    }
                )

        # execute sql stmt
        for table, value in stmt_insert_t_v.items():
            stmt_insert = insert(table).value(**value)
            sqldb.execute(stmt_insert)

    except Exception as e:
        logger.error(e)
        raise e
