from fastapi import HTTPException, status
from loguru import logger
from attrs import define
from typing import Any, Union
import phonenumbers
from phonenumbers import NumberParseException, geocoder, PhoneNumber


from sqlalchemy import select, insert, or_
from sqlalchemy.engine import Connection
from sqlalchemy.schema import Table

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
from enums.country_code import CountryCodeId
from routers.dependency.security import utils


# @define
# class Node_value:
#     data: list[str, Any]
#     stmt: tuple[Any]
# @define
# class Table_stmt:
#     data: list[str, Any]


def filter_out_input_account(user: dict[str, Any]):
    ## if account input exist, following value will equal input value.
    account_input_exist = {
        "email": user.get("email", None),
        "phone": user.get("phone", None),
        "username": user.get("username", None),
    }

    return dict(
        filter(
            lambda account: account[1] is not None and account[1] != "",
            account_input_exist.items(),
        )
    )
    # account_input_exist = {
    #     "email": False,
    #     "phone": False,
    #     "username": False,
    # }
    # for account in account_input_exist.keys():
    #     if user[account] is None or user[account] == "":
    #         continue
    #     else:
    #         account_input_exist[account] = user[account]

    # return account_input_exist


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


def insert_to_db_table(
    data: dict[Any, Any],
    table: Table,
    sqldb: Connection,
    returning: Union[None, list[Any]] = None,
):
    logger.debug(f"data: {data}, table: {table}, returning: {returning}")
    table_return = None
    if returning is None:
        stmt_insert = insert(table).values(**data)
        sqldb.execute(stmt_insert)
    else:
        stmt_insert = insert(table).values(**data).returning(*returning)
        table_return = sqldb.execute(stmt_insert).first()._asdict()

    sqldb.commit()
    return table_return


# TODO: phone number convert to comply database format
def user_to_sqldb(user, sqldb: Connection):
    logger.info("user data to sqldb")
    logger.debug(user)
    user = user.dict()
    try:
        account_input_exist = filter_out_input_account(user)
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

    logger.debug(f"Now account with password: {user}")

    # construct what data want to insert to database table
    try:
        stmt_insert_t_v: dict[Table, dict] = {
            users_outline.users_table: {
                "surname": user["surname"],
                "password": user["password"],
                "given_name": user["given_name"],
                "description": user["description"],
            },
            users_registration.users_register_table: {},
        }

        # what values do you want to return from database
        stmt_insert_t_r: dict[Table, list] = {
            users_outline.users_table: [
                users_outline.users_table.c.id,
            ],
            users_registration.users_register_table: [
                users_registration.users_register_table.c.registration,
                users_registration.users_register_table.c.registration_type,
                users_registration.users_register_table.c.created_at,
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
            table_return = insert_to_db_table(value, table, sqldb, returning_check)
            logger.debug(f"table_return: {table.name}: {table_return}")
            sql_return_data.update({table.name: table_return})

            if table == users_outline.users_table:
                stmt_insert_t_v[users_registration.users_register_table].update(
                    {"user_id": table_return["id"]}
                )

        logger.debug(f"sql_return_data is: {sql_return_data}")
    except Exception as e:
        logger.error(e)
        raise e
    return sql_return_data


def account_to_proper_sqldb_table(account: dict[str, Any], sqldb: Connection):
    """
    Args:
        account (dict[str, Any]):  {
            users: {'id': 12},
            users_register: {'registration': '0961300141', 'registration_type': <Register.phone: 2>
        }
        sqldb (Connection): _description_

    Raises:
        e: _description_
    """
    try:
        ## TODO: properly construct
        # construct what data want to insert to database table
        logger.debug(f"account: {account}")
        account_data: dict[str, Any] = {
            **account["users"],
            **account["users_register"],
        }
        logger.debug(f"account_data: {account_data}")

        regis_type = account["users_register"]["registration_type"]
        ph_parse: PhoneNumber = phonenumbers.parse(account_data["registration"])
        country_name = geocoder.description_for_number(ph_parse, "en")

        stmt_insert_t_v: dict[str, Any] = {
            "user_id": account_data["id"],
            "user_country_id": CountryCodeId[country_name].value,
            "subscriber_number": ph_parse.national_number,
            "email": account_data["registration"],
            "username": account_data["registration"],
        }

        filter_out_stmt_insert_t_v = {}

        if regis_type == Register["phone"]:
            phone_stmt_insert_t_v = dict(
                filter(
                    lambda x: x[0]
                    in ["user_id", "user_country_id", "subscriber_number"],
                    stmt_insert_t_v.items(),
                )
            )
            filter_out_stmt_insert_t_v.update(**phone_stmt_insert_t_v)
        elif regis_type == Register["email"]:
            email_stmt_insert_t_v = dict(
                filter(
                    lambda x: x[0] in ["user_id", "email"],
                    stmt_insert_t_v.items(),
                )
            )
            filter_out_stmt_insert_t_v.update(**email_stmt_insert_t_v)
        elif regis_type == Register["username"]:
            username_stmt_insert_t_v = dict(
                filter(
                    lambda x: x[0] in ["user_id", "username"],
                    stmt_insert_t_v.items(),
                )
            )
            filter_out_stmt_insert_t_v.update(**username_stmt_insert_t_v)

        # for key, value in account_data.items():
        #     if key in ["email", "username"]:
        #         stmt_insert_t_v.update(
        #             {
        #                 table_map[key]: {
        #                     "user_id": account["id"],
        #                     key: value,
        #                 }
        #             }
        #         )
        #     if key in ["mobile"]:
        #         stmt_insert_t_v.update(
        #             {
        #                 table_map[key]: {
        #                     "user_id": account["id"],
        #                     "user_country_id": account["user_country_id"],
        #                     "subscriber_number": account["subscriber_number"],
        #                 }
        #             }
        #         )
    except NumberParseException as e:
        logger.error(e)
        raise e
    except Exception as e:
        logger.error(e)
        raise e

    # execute sql stmt
    try:
        table_map = {
            Register["username"]: users_account.users_username_table,
            Register["email"]: users_account.users_email_table,
            Register["phone"]: users_account.users_phone_table,
        }
        insert_to_db_table(
            filter_out_stmt_insert_t_v,
            table_map[regis_type],
            sqldb=sqldb,
        )
    except Exception as e:
        logger.error(e)
        raise e
