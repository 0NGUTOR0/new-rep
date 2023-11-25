"""create users table

Revision ID: a1882a349a4d
Revises: 0b2542814c94
Create Date: 2023-11-02 09:11:39.224439

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'a1882a349a4d'
down_revision: Union[str, None] = '0b2542814c94'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
