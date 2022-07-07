"""add account_status_id col to users_table, create account_status_table

Revision ID: 16afde913cb3
Revises: 7cb3bb78ea41
Create Date: 2022-07-07 14:31:47.185428

"""
from alembic import op
import sqlalchemy as sa
from persistences.postgresql.modules.user.account_status import account_status_table

# revision identifiers, used by Alembic.
revision = "16afde913cb3"
down_revision = "7cb3bb78ea41"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "account_status",
        sa.Column(
            "id",
            sa.BigInteger(),
            sa.Identity(always=False),
            autoincrement=True,
            nullable=False,
        ),
        sa.Column(
            "activate", sa.Boolean(), server_default=sa.text("false"), nullable=False
        ),
        sa.Column(
            "forbidden", sa.Boolean(), server_default=sa.text("false"), nullable=False
        ),
        sa.Column(
            "forbidden_at",
            sa.TIMESTAMP(timezone=True),
            server_default=sa.text("NULL"),
            nullable=True,
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.bulk_insert(
        account_status_table,
        [
            {"id": 0, "activate": False, "forbidden": False},
            {"id": 1, "activate": True, "forbidden": False},
            {"id": 2, "activate": False, "forbidden": True},
        ],
    )
    op.add_column(
        "users",
        sa.Column(
            "account_status_id", sa.BigInteger(), server_default="0", nullable=False
        ),
    )
    op.create_foreign_key(
        "FK_account_status_table_id",
        "users",
        "account_status",
        ["account_status_id"],
        ["id"],
        ondelete="CASCADE",
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint("FK_account_status_table_id", "users", type_="foreignkey")
    op.drop_column("users", "account_status_id")
    op.drop_table("account_status")
    # ### end Alembic commands ###