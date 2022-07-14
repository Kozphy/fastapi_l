from sqlalchemy import (
    Column,
    Table,
    MetaData,
    BigInteger,
    Identity,
)
from sqlalchemy.types import VARCHAR
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.sql.expression import text

users_country_meta = MetaData()

users_country_table = Table(
    "users_country",
    users_country_meta,
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
    Column("last_update", TIMESTAMP(timezone=True), server_default=text("now()")),
)
