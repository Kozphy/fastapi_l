from loguru import logger
from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import create_async_engine
from pprint import pprint

from typing import List, Dict, Any

support_databases = {
    'MYSQL': "mysql+mysqldb://",
    'POSTGRESQL': "postgresql+psycopg://"
}

support_ssl = ['MYSQL']


def init_db_url(db, user, password, host, db_name, port, charset="utf8mb4",
 ssl=False, echo=True, future=True, **kwargs) -> str:

    if db not in support_databases:
        raise Exception("Database not supported")
    if db == 'MySQL':
        db_url = f"{support_databases[db]}{user}:{password}@{host}:{port}/{db_name}?charset={charset}"
    elif db == 'POSTGRESQL':
        db_url = f"{support_databases[db]}{user}:{password}@{host}:{port}/{db_name}"
    

    return db_url

def init_db_engine(configured: Dict[str, Any], echo, future) -> None:
        """Initialize the database engine"""
        pprint(configured)
        ssl = configured['ssl']
        db_args = {
            'db': configured['db'].upper(),
            'user': configured['user'],
            'password': configured['password'],
            'host': configured['host'],
            'db_name': configured['db_name'],
            'port': configured['port'],
        }
        # exit()

        try:
            db_url = init_db_url(**db_args)
            logger.debug(f"db url is {db_url}")

            if db_args['db'] not in support_ssl or ssl == False:
                engine = create_engine(db_url, echo=echo, future=future)
                return engine, db_url

            # TODO: not set now, need to set
            connect_args ={
                "ssl": {
                    "ssl_ca": "/etc/mysql/ca-cert.pem",
                    "ssl_cert": "/etc/mysql/client-cert.pem",
                    "ssl_key": "/etc/mysql/client-key.pem"
                }
            }

            engine = create_engine(db_url, connect_args, echo=echo, future=future)
            return engine, db_url
            
        except Exception as e:
            logger.error(e)
            raise Exception(e)
# SQLALCHEMY_DATABASE_URL = "postgresql://user:password@postgresserver/db"


