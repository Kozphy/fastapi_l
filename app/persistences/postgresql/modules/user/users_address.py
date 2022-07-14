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
from sqlalchemy.sql.expression import text
from persistences.postgresql.modules.user.users_country import users_country_table

users_address_in_formosa_meta = MetaData()

users_address_in_formosa_table = Table(
    "users_address_in_formosa",
    users_address_in_formosa_meta,
    Column(
        "id",
        BigInteger,
        Identity(),
        primary_key=True,
        autoincrement=True,
        nullable=False,
    ),
    Column(
        "user_country_id",
        ForeignKey(users_country_table.c.id, ondelete="CASCADE"),
        nullable=False,
    ),
    Column("city", VARCHAR(255), nullable=False),
    Column("region", VARCHAR(255), nullable=False),
    Column("address1", VARCHAR(255), nullable=False),
    Column("address2", VARCHAR(255), nullable=False),
    Column("address3", VARCHAR(255), nullable=False),
    Column("zip_code", VARCHAR(6), nullable=False),
    Column("last_update", TIMESTAMP(timezone=True), server_default=text("now()")),
)
