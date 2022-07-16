from sqlalchemy import (
    Column,
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

users_country_table = Table(
    "users_country",
    users_table_meta,
    Column(
        "id",
        BigInteger,
        Identity(),
        primary_key=True,
        autoincrement=True,
        nullable=False,
    ),
    Column("country", VARCHAR(255), nullable=False),
    Column("country_code", VARCHAR(10), nullable=False),
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
