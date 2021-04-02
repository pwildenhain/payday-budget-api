"""create transactions table

Revision ID: b833ff51f56d
Revises: 68e8af48f08c
Create Date: 2021-04-02 12:55:59.050387

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b833ff51f56d'
down_revision = '68e8af48f08c'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "transactions",
        sa.Column("transaction_id", sa.Integer, primary_key=True, autoincrement=True),
        sa.Column("date", sa.String),
        sa.Column("account_id", sa.Integer, sa.ForeignKey("accounts.account_id")),
        sa.Column("comment", sa.String),
        sa.Column("transaction_type", sa.String),
        sa.Column("amount", sa.Integer)
    )


def downgrade():
    op.drop_table("transactions")