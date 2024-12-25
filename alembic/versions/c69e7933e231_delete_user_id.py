"""delete user_id

Revision ID: c69e7933e231
Revises: c1e490709f0c
Create Date: 2024-12-25 13:03:18.889196

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'c69e7933e231'
down_revision: Union[str, None] = 'c1e490709f0c'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
