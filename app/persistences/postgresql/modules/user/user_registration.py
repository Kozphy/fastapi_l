from sqlalchemy import (
    Column,
    ForeignKey,
    Table,
    MetaData,
    BigInteger,
    Identity,
    UniqueConstraint,
    Enum,
)
from sqlalchemy.types import VARCHAR
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.sql.expression import text
from persistences.postgresql.modules.user.users_outline_table import (
    users_table_meta,
)
from enums.register import Register

users_register_table = Table(
    "users_register",
    users_table_meta,
    Column(
        "id",
        BigInteger,
        Identity(),
        primary_key=True,
        autoincrement=True,
        nullable=False,
    ),
    # Column("users_id", ForeignKey("users.id", ondelete="CASCADE"), nullable=False),
    Column(
        "registration",
        VARCHAR(255),
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
    ),
    Column("registration_type", Enum(Register, create_type=False), nullable=False),
    Column("last_update", TIMESTAMP(timezone=True), server_default=text("now()")),
)
