"""add contents column to new table 4 posts

Revision ID: 79d5c27b5579
Revises: 46064810a642
Create Date: 2023-12-10 09:33:46.110876

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '79d5c27b5579'
down_revision: Union[str, None] = '46064810a642'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("POSTSTABLE", sa.Column("Contents", sa.String(), nullable= False))
    pass


def downgrade() -> None:
    op.drop_column("POSTSTABLE", "Contents")
    pass
