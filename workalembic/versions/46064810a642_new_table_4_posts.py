"""new table 4 posts

Revision ID: 46064810a642
Revises: 
Create Date: 2023-12-10 09:03:59.259061

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '46064810a642'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table("POSTSTABLE", sa.Column("id", sa.Integer, nullable=False, primary_key=True),
                    sa.Column("Title", sa. String, nullable=False ))
    


def downgrade() -> None:
    op.drop_table("POSTSTABLE")
    pass
