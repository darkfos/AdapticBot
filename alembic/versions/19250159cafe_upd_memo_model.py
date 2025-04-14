"""upd: memo model

Revision ID: 19250159cafe
Revises: bf97f520b76a
Create Date: 2025-04-14 22:08:28.652110

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "19250159cafe"
down_revision: Union[str, None] = "bf97f520b76a"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column(
        "meetmodel",
        sa.Column("date_last_meeting", sa.DateTime(), nullable=True),
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    """Downgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column("meetmodel", "date_last_meeting")
    # ### end Alembic commands ###
