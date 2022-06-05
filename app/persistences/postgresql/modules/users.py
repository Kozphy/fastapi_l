from sqlalchemy import (Column, Table, MetaData, Boolean, BigInteger, 
String, Identity)
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.sql.expression import text, true

user_meta = MetaData()

User_table = Table('users', user_meta,
    Column('id', BigInteger, Identity(), primary_key=True, autoincrement=True, nullable=False),
    Column('email', String, nullable=False, unique=True),
    Column('password', String, nullable=False),
    Column('created_at', TIMESTAMP(timezone=True),
     nullable=False, server_default=text('now()')),
)
