from sqlalchemy import (
    Column,
    ForeignKey,
    Table,
    MetaData,
    Boolean,
    BigInteger,
    String,
    Identity,
    Enum,
)
from sqlalchemy.types import VARCHAR, TEXT
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.sql.expression import text, null
from enums.gender import Gender

users_detail_in_formosa_meta = MetaData()

users_detail_in_formosa_table = Table(
    "users_detail_in_formosa",
    users_detail_in_formosa_meta,
    Column(
        "id",
        BigInteger,
        Identity(),
        primary_key=True,
        autoincrement=True,
        nullable=False,
    ),
    Column("surname", VARCHAR(30), server_default="", nullable=False),
    Column("given_name", VARCHAR(50), server_default="", nullable=False),
    Column("gender", Enum(Gender, create_type=False), nullable=False),
    Column("formosa_id_card_letter", VARCHAR(1), nullable=False),
    Column("formosa_id_card", VARCHAR(9), nullable=False),
    Column("address1", VARCHAR(255), nullable=False),
    Column("address2", VARCHAR(255), nullable=False),
    Column("address3", VARCHAR(255), nullable=False),
    Column("country", VARCHAR(255), nullable=False),
    Column("city", VARCHAR(255), nullable=False),
    Column("region", VARCHAR(255), nullable=False),
    Column("zip_code", VARCHAR(6), nullable=False),
    Column("country_code", VARCHAR(4), default="+886", nullable=False),
    Column("subscriber_number", VARCHAR(9), nullable=False),
    Column("description", TEXT(), nullable=False),
    Column("last_update", TIMESTAMP(timezone=True), server_default=text("now()")),
)
