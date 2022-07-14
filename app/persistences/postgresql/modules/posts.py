from sqlalchemy import Column, Table, MetaData, Boolean, BigInteger, String, Identity
from sqlalchemy.schema import ForeignKey
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.sql.expression import text, true
from persistences.postgresql.modules.user.users_id_card_in_formosa import (
    users_in_formosa_table,
)

posts_meta = MetaData()

posts_table = Table(
    "posts",
    posts_meta,
    Column(
        "id",
        BigInteger,
        Identity(),
        primary_key=True,
        autoincrement=True,
        nullable=False,
    ),
    Column(
        "owner_id",
        BigInteger,
        ForeignKey(users_in_formosa_table.c.id, ondelete="CASCADE"),
        nullable=False,
    ),
    Column("title", String, nullable=False),
    Column("content", String, nullable=False),
    Column("published", Boolean, server_default=true(), nullable=False),
    Column(
        "create_at",
        TIMESTAMP(timezone=True),
        nullable=False,
        server_default=text("now()"),
    ),
)
