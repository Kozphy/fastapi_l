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
from sqlalchemy.types import VARCHAR
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.sql.expression import text, null

from persistences.postgresql.modules.user.users_status import users_status_table
from persistences.postgresql.modules.user.users_detail_in_formosa import (
    users_detail_in_formosa_table,
)

users_in_formosa_meta = MetaData()

users_in_formosa_table = Table(
    "users_in_formosa",
    users_in_formosa_meta,
    Column(
        "id",
        BigInteger,
        Identity(),
        primary_key=True,
        autoincrement=True,
        nullable=False,
    ),
    Column(
        "user_detail_in_formosa_id",
        BigInteger,
        ForeignKey(users_detail_in_formosa_table.c.id, ondelete="CASCADE"),
        nullable=False,
    ),
    Column(
        "account_status_id",
        BigInteger,
        ForeignKey(users_status_table.c.id, ondelete="CASCADE"),
        server_default="0",
        nullable=False,
    ),
    Column("email", VARCHAR(50), nullable=False, unique=True),
    Column("password", VARCHAR(100), nullable=False),
    Column(
        "created_at",
        TIMESTAMP(timezone=True),
        nullable=False,
        server_default=text("now()"),
    ),
    Column("forbidden_at", TIMESTAMP(timezone=True), server_default=null()),
)
