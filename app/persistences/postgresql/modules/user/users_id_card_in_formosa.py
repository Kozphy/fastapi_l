from sqlalchemy import (
    Column,
    ForeignKey,
    Table,
    MetaData,
    BigInteger,
    Identity,
    Enum,
)
from sqlalchemy.types import VARCHAR, TEXT
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.sql.expression import text
from enums.gender import Gender
from persistences.postgresql.modules.user.users_outline_table import users_table

users_in_formosa_meta = MetaData()

users_id_card_in_formosa_table = Table(
    "users_id_card_in_formosa",
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
        "users_id", ForeignKey(users_table.c.id, ondelete="CASCADE"), nullable=False
    ),
    Column("gender", Enum(Gender, create_type=False), nullable=False),
    Column("formosa_id_card_letter", VARCHAR(1), nullable=False),
    Column("formosa_id_card", VARCHAR(9), nullable=False),
    Column("issuance_type", VARCHAR(3), nullable=False),
    Column("issuance_date", TIMESTAMP(timezone=True), nullable=False),
    Column("description", TEXT()),
    Column("last_update", TIMESTAMP(timezone=True), server_default=text("now()")),
)
