"""Add email to users

Revision ID: 29d9b43d9512
Revises: b08bf7387745
Create Date: 2023-02-23 19:22:55.709708

"""
from alembic import op
import sqlalchemy as sa
import sqlmodel


# revision identifiers, used by Alembic.
revision = "29d9b43d9512"
down_revision = "b08bf7387745"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column("user", sa.Column("email", sqlmodel.sql.sqltypes.AutoString(), nullable=False))
    op.add_column("user", sa.Column("hashed_password", sqlmodel.sql.sqltypes.AutoString(), nullable=False))
    op.add_column("user", sa.Column("is_active", sa.Boolean(), nullable=False))
    op.add_column("user", sa.Column("is_superuser", sa.Boolean(), nullable=False))
    op.drop_column("user", "name")
    op.drop_column("user", "age")
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column("user", sa.Column("age", sa.INTEGER(), autoincrement=False, nullable=True))
    op.add_column("user", sa.Column("name", sa.VARCHAR(), autoincrement=False, nullable=False))
    op.drop_column("user", "is_superuser")
    op.drop_column("user", "is_active")
    op.drop_column("user", "hashed_password")
    op.drop_column("user", "email")
    # ### end Alembic commands ###