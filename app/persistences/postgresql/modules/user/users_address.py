from sqlalchemy import (
    Column,
    ForeignKey,
    Table,
    BigInteger,
    Identity,
)
from sqlalchemy.types import VARCHAR
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.sql.expression import text
from persistences.postgresql.modules.user.users_outline import (
    users_table_meta,
)


users_address_table = Table(
    "users_address",
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
    Column(
        "user_country_id",
        ForeignKey("users_country.id", onupdate="CASCADE", ondelete="CASCADE"),
        nullable=False,
    ),
    Column("city", VARCHAR(255), nullable=False),
    Column("region", VARCHAR(255), nullable=False),
    Column("address1", VARCHAR(255), nullable=False),
    Column("address2", VARCHAR(255), nullable=False),
    Column("address3", VARCHAR(255), nullable=False),
    Column("zip_code", VARCHAR(6), nullable=False),
    Column(
        "created_at",
        TIMESTAMP(timezone=True),
        nullable=False,
        server_default=text("now()"),
    ),
    Column(
        "last_update",
        TIMESTAMP(timezone=True),
        nullable=False,
        server_default=text("now()"),
    ),
)
