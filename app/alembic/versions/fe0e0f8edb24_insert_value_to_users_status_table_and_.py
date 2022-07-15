"""insert value to users_status_table and users_country_table

Revision ID: fe0e0f8edb24
Revises: 5437b85fc3e7
Create Date: 2022-07-15 08:03:11.066408

"""
from alembic import op
import sqlalchemy as sa
from persistences.postgresql.modules.user.users_status import users_status_table
from persistences.postgresql.modules.user.users_country import users_country_table


# revision identifiers, used by Alembic.
revision = "fe0e0f8edb24"
down_revision = "5437b85fc3e7"
branch_labels = None
depends_on = None


def upgrade():
    op.bulk_insert(
        users_status_table,
        [
            {
                "id": 0,
                "activate": False,
                "forbidden": False,
            },
            {
                "id": 1,
                "activate": True,
                "forbidden": False,
            },
            {
                "id": 2,
                "activate": False,
                "forbidden": True,
            },
        ],
    )
    op.bulk_insert(
        users_country_table, [{"id": 0, "country": "Taiwan", "country_code": "+886"}]
    )


def downgrade():
    op.execute("DELETE FROM users_status")
    op.execute("DELETE FROM users_country")
