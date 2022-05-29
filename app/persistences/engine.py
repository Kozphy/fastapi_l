from loguru import logger
from sqlalchemy import create_engine

support_databases = {
    'MYSQL': "mysql+mysqldb://",
    'PostgreSQL': "postgresql+psycopg://"
}

support_ssl = ['MYSQL']

def init_db_engine(db, user, password, host, dbname, port=3306, charset="utf8mb4", ssl=False, echo=True, future=True) -> None:
        """Initialize the database engine"""
        db = db.upper()

        if db not in support_databases:
            raise Exception(f"{db} Database not supported")
        try:
            db_url = f"{support_databases[db]}{user}:{password}@{host}:{port}/{dbname}?charset={charset}"

            if db not in support_ssl or ssl == False:
                engine = create_engine(db_url, echo=echo, future=future)
                return engine

            # TODO: not set now, need to set
            connect_args ={
                "ssl": {
                    "ssl_ca": "/etc/mysql/ca-cert.pem",
                    "ssl_cert": "/etc/mysql/client-cert.pem",
                    "ssl_key": "/etc/mysql/client-key.pem"
                }
            }

            engine = create_engine(db_url, connect_args, echo=echo, future=future)
            return engine
            
        except Exception as e:
            logger.error(e)
            raise Exception("Database connection failed")
# SQLALCHEMY_DATABASE_URL = "postgresql://user:password@postgresserver/db"


