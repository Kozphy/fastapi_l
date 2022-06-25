from loguru import logger
from sqlalchemy import create_engine
from sqlalchemy.engine import Engine
from sqlalchemy.ext.asyncio import create_async_engine
from pprint import pprint

from typing import List, Dict, Any

# Currently, driver suppoet for sqlalchemy version > 1.4, < 2.0
support_databases = {
    "MYSQL": "mysql+mysqldb://",
    "POSTGRESQL": "postgresql+psycopg2://",
}

database_default_port = {"MYSQL": 3306, "POSTGRESQL": 5432}


support_ssl = ["MYSQL", "POSTGRESQL"]


def init_db_url(
    db, user, password, host, db_name, port, charset="utf8mb4", **kwargs
) -> str:

    if db not in support_databases:
        raise Exception("Database not supported")
    if db == "MYSQL":
        db_url = f"{support_databases[db]}{user}:{password}@{host}:{port}/{db_name}?charset={charset}"
    elif db == "POSTGRESQL":
        db_url = f"{support_databases[db]}{user}:{password}@{host}:{port}/{db_name}"

    return db_url


def init_db_engine(configured: Dict[str, Any], echo=True, future=True) -> Engine:
    """Initialize the database engine"""
    logger.info("init relational db engine")

    try:
        ssl = configured["ssl"] if "ssl" in configured else None

        db_args = {
            "db": configured["db"].upper(),
            "user": configured["user"],
            "password": configured["password"],
            "host": configured["host"],
            "db_name": configured["db_name"],
            "port": configured["port"],
        }

        db_url = init_db_url(**db_args)
        logger.debug(f"db url is {db_url}")

        if db_args["db"] not in support_ssl or not ssl:
            engine = create_engine(db_url, echo=echo, future=future)
            return engine, db_url, db_args["db_name"]

        # TODO: not set now, need to set
        connect_args = {
            "ssl": {
                "ssl_ca": "/etc/mysql/ca-cert.pem",
                "ssl_cert": "/etc/mysql/client-cert.pem",
                "ssl_key": "/etc/mysql/client-key.pem",
            }
        }

        engine = create_engine(db_url, connect_args, echo=echo, future=future)
        return engine, db_url, db_args["db_name"]

    except Exception as e:
        logger.error(e)
        raise Exception(e)
