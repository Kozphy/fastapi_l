from sqlalchemy import (
    Column,
    ForeignKey,
    Table,
    MetaData,
    Boolean,
    BigInteger,
    String,
    Identity,
)
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.sql.expression import text, null

from persistences.postgresql.modules.user.account_status import account_status_table
from persistences.postgresql.modules.user.users_detail import users_detail_table

users_meta = MetaData()

users_table = Table(
    "users",
    users_meta,
    Column(
        "id",
        BigInteger,
        Identity(),
        primary_key=True,
        autoincrement=True,
        nullable=False,
    ),
    Column(
        "user_detail_id",
        BigInteger,
        ForeignKey(users_detail_table.c.id, ondelete="CASCADE"),
        nullable=False,
    ),
    Column(
        "account_status_id",
        BigInteger,
        ForeignKey(account_status_table.c.id, ondelete="CASCADE"),
        server_default="0",
        nullable=False,
    ),
    Column("email", String, nullable=False, unique=True),
    Column("password", String, nullable=False),
    Column(
        "created_at",
        TIMESTAMP(timezone=True),
        nullable=False,
        server_default=text("now()"),
    ),
    Column("forbidden_at", TIMESTAMP(timezone=True), server_default=null()),
)
