from sqlalchemy import (
    Column,
    ForeignKey,
    Table,
    BigInteger,
    Identity,
    Enum,
)
from sqlalchemy.types import VARCHAR, TEXT
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.sql.expression import text
from sqlalchemy.schema import UniqueConstraint
from enums.gender import Gender
from persistences.postgresql.modules.user.users_outline_table import (
    users_table_meta,
)


users_id_card_in_formosa_table = Table(
    "users_id_card_in_formosa",
    users_table_meta,
    Column(
        "id",
        BigInteger,
        Identity(),
        primary_key=True,
        autoincrement=True,
        nullable=False,
    ),
    Column("users_id", ForeignKey("users.id", ondelete="CASCADE"), nullable=False),
    Column(
        "user_country_id",
        ForeignKey("users_country.id", ondelete="CASCADE"),
        nullable=False,
    ),
    Column("gender", Enum(Gender, create_type=False), nullable=False),
    Column("formosa_id_card_letter", VARCHAR(1), nullable=False),
    Column("formosa_id_card", VARCHAR(9), nullable=False),
    Column("issuance_type", VARCHAR(3), nullable=False),
    Column("issuance_date", TIMESTAMP(timezone=True), nullable=False),
    Column("description", TEXT()),
    Column("create_at", TIMESTAMP(timezone=True), server_default=text("now()")),
    Column("last_update", TIMESTAMP(timezone=True), server_default=text("now()")),
    UniqueConstraint("formosa_id_card_letter", "formosa_id_card"),
)
