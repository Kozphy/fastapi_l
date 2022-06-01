from sqlalchemy import (Column, Table, MetaData, Boolean, BigInteger, 
String)
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.sql.expression import text, true

post_meta = MetaData()

Post_table = Table('posts', post_meta,
    Column('id', BigInteger, primary_key=True, nullable=False),
    Column('title', String, nullable=False),
    Column('content', String, nullable=False),
    Column('published', Boolean, server_default=true(), nullable=False),
    Column('create_at', TIMESTAMP(timezone=True), 
            nullable=False, server_default=text('now()')),
)
