from sqlalchemy import (
    Column,
    ForeignKey,
    Table,
    MetaData,
    BigInteger,
    Identity,
    UniqueConstraint,
)
from sqlalchemy.types import VARCHAR
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.sql.expression import text
from persistences.postgresql.modules.user.users_outline import (
    users_table_meta,
)

users_username_table = Table(
    "users_username",
    users_table_meta,
    Column(
        "id",
        BigInteger,
        Identity(),
        primary_key=True,
        autoincrement=True,
        nullable=False,
    ),
    Column(
        "users_id",
        ForeignKey("users.id", onupdate="CASCADE", ondelete="CASCADE"),
        nullable=False,
    ),
    Column("username", VARCHAR(255), nullable=False, unique=True),
    Column("create_at", TIMESTAMP(timezone=True), server_default=text("now()")),
    Column("last_update", TIMESTAMP(timezone=True), server_default=text("now()")),
)

users_email_table = Table(
    "users_email",
    users_table_meta,
    Column(
        "id",
        BigInteger,
        Identity(),
        primary_key=True,
        autoincrement=True,
        nullable=False,
    ),
    Column(
        "users_id",
        ForeignKey("users.id", onupdate="CASCADE", ondelete="CASCADE"),
        nullable=False,
    ),
    Column("email", VARCHAR(255), nullable=False, unique=True),
    Column("create_at", TIMESTAMP(timezone=True), server_default=text("now()")),
    Column("last_update", TIMESTAMP(timezone=True), server_default=text("now()")),
)

users_phone_table = Table(
    "users_phone",
    users_table_meta,
    Column(
        "id",
        BigInteger,
        Identity(),
        primary_key=True,
        autoincrement=True,
        nullable=False,
    ),
    Column(
        "user_id",
        ForeignKey("users.id", onupdate="CASCADE", ondelete="CASCADE"),
        nullable=False,
    ),
    Column(
        "user_country_id",
        ForeignKey("users_country.id", onupdate="CASCADE", ondelete="CASCADE"),
        nullable=False,
    ),
    Column("subscriber_number", VARCHAR(15), nullable=False),
    Column("create_at", TIMESTAMP(timezone=True), server_default=text("now()")),
    Column("last_update", TIMESTAMP(timezone=True), server_default=text("now()")),
    UniqueConstraint("user_country_id", "subscriber_number"),
)
