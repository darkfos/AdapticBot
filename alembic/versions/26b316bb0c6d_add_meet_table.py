"""add: meet table

Revision ID: 26b316bb0c6d
Revises: d59324b62748
Create Date: 2025-03-30 18:59:02.264401

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "26b316bb0c6d"
down_revision: Union[str, None] = "d59324b62748"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "meetmodel",
        sa.Column("id_who", sa.BigInteger(), nullable=False),
        sa.Column("id_with", sa.BigInteger(), nullable=True),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("date_meeting", sa.DateTime(), nullable=True),
        sa.Column("id", sa.Integer(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        op.f("ix_meetmodel_id_who"), "meetmodel", ["id_who"], unique=False
    )
    op.create_index(
        op.f("ix_meetmodel_id_with"), "meetmodel", ["id_with"], unique=False
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    """Downgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f("ix_meetmodel_id_with"), table_name="meetmodel")
    op.drop_index(op.f("ix_meetmodel_id_who"), table_name="meetmodel")
    op.drop_table("meetmodel")
    # ### end Alembic commands ###
