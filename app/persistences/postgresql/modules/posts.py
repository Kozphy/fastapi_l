from sqlalchemy import (Column, Table, MetaData, Boolean, BigInteger, 
String, Identity)
from sqlalchemy.schema import ForeignKey
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.sql.expression import text, true
from persistences.postgresql.modules.users import User_table

post_meta = MetaData()

Post_table = Table('posts', post_meta,
    Column('id', BigInteger, Identity(), primary_key=True, autoincrement=True, nullable=False),
    Column('owner_id', BigInteger, ForeignKey(User_table.c.id, ondelete="CASCADE"), nullable=False),
    Column('title', String, nullable=False),
    Column('content', String, nullable=False),
    Column('published', Boolean, server_default=true(), nullable=False),
    Column('create_at', TIMESTAMP(timezone=True), 
            nullable=False, server_default=text('now()')),
)
