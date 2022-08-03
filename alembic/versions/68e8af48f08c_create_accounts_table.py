"""create accounts table

Revision ID: 68e8af48f08c
Revises: 
Create Date: 2021-04-02 12:53:45.046990

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "68e8af48f08c"
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "accounts",
        sa.Column("account_id", sa.Integer, primary_key=True, autoincrement=True),
        sa.Column("name", sa.String),
        sa.Column("category", sa.String),
        sa.Column("budgeted_amount", sa.Integer),
        sa.Column("current_balance", sa.Integer),
    )


def downgrade():
    op.drop_table("accounts")
