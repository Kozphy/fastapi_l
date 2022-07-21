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


# TODO: phone number convert to comply database format
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

        stmt_insert_t_r = {
            users_outline.users_table: [users_outline.users_table.c.id],
            # users_registration.users_register_table: [
            #     users_registration.users_register_table.c.registration,
            #     users_registration.users_register_table.c.registration_type,
            # ],
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
                sql_return_data.update({account: user[account]})

        # execute sql stmt
        for table, value in stmt_insert_t_v.items():
            returning_check = stmt_insert_t_r.get(table, None)
            if returning_check is not None:
                stmt_insert = insert(table).values(**value).returning(*returning_check)
                table_return = sqldb.execute(stmt_insert).first()._asdict()
                sql_return_data.update(**table_return)
            else:
                stmt_insert = insert(table).values(**value)
                sqldb.execute(stmt_insert)

            if table == users_outline.users_table:
                logger.debug(f"users_table return is : {table_return}")
                stmt_insert_t_v[users_registration.users_register_table].update(
                    {"user_id": table_return["id"]}
                )

    except Exception as e:
        logger.error(e)
        raise e
    logger.debug(f"sql_return_data is: {sql_return_data}")
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
