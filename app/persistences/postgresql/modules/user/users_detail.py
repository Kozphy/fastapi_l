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

users_detail_meta = MetaData()

users_detail_table = Table(
    "users_detail",
    users_detail_meta,
    Column(
        "id",
        BigInteger,
        Identity(),
        primary_key=True,
        autoincrement=True,
        nullable=False,
    ),
    Column("surname", String, server_default="", nullable=False),
    Column("given_name", String, server_default="", nullable=False),
    Column("gender"),
    Column("address1"),
    Column("address2"),
    Column("address3"),
    Column("country"),
    Column("city"),
    Column("region"),
    Column("zip_code"),
    Column("phone_number", int, nullable=False),
    Column("last_update"),
)
