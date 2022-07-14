from sqlalchemy import (
    Column,
    ForeignKey,
    Table,
    MetaData,
    BigInteger,
    Identity,
)
from sqlalchemy.types import VARCHAR, TEXT
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.sql.expression import text, null
from persistences.postgresql.modules.user import users_status

users_table_meta = MetaData()

# TODO: Fix Phone number and id_card must be unique
users_table = Table(
    "users",
    users_table_meta,
    Column(
        "id",
        BigInteger,
        Identity(),
        primary_key=True,
        autoincrement=True,
        nullable=False,
    ),
    Column("account", VARCHAR(50), nullable=False, unique=True),
    Column("password", VARCHAR(100), nullable=False),
    Column("surname", VARCHAR(30), server_default="", nullable=False),
    Column("given_name", VARCHAR(50), server_default="", nullable=False),
    Column("description", TEXT()),
    Column(
        "user_status_id",
        BigInteger,
        ForeignKey(users_status.users_status_table.c.id, ondelete="CASCADE"),
        server_default="0",
        nullable=False,
    ),
    Column(
        "created_at",
        TIMESTAMP(timezone=True),
        nullable=False,
        server_default=text("now()"),
    ),
    Column("forbidden_at", TIMESTAMP(timezone=True), server_default=null()),
)
