from sqlalchemy import (
    Column,
    ForeignKey,
    Table,
    MetaData,
    BigInteger,
    Identity,
)
from sqlalchemy.types import VARCHAR
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.sql.expression import text
from persistences.postgresql.modules.user.users_outline_table import users_table
from persistences.postgresql.modules.user.users_country import users_country_table

users_account_meta = MetaData()

users_email_table = Table(
    "users_email",
    users_account_meta,
    Column(
        "id",
        BigInteger,
        Identity(),
        primary_key=True,
        autoincrement=True,
        nullable=False,
    ),
    Column(
        "users_id", ForeignKey(users_table.c.id, ondelete="CASCADE"), nullable=False
    ),
    Column("email", VARCHAR(50), nullable=False, unique=True),
    Column("last_update", TIMESTAMP(timezone=True), server_default=text("now()")),
)

users_phone_table = Table(
    "users_phone",
    users_account_meta,
    Column(
        "id",
        BigInteger,
        Identity(),
        primary_key=True,
        autoincrement=True,
        nullable=False,
    ),
    Column("user_id", ForeignKey(users_table.c.id, ondelete="CASCADE"), nullable=False),
    Column(
        "user_country_id",
        ForeignKey(users_country_table.c.id, ondelete="CASCADE"),
        nullable=False,
    ),
    Column("subscriber_number", VARCHAR(9), nullable=False),
    Column("last_update", TIMESTAMP(timezone=True), server_default=text("now()")),
)
