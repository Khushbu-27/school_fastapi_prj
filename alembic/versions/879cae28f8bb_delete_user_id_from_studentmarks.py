"""delete user_id from StudentMarks

Revision ID: 879cae28f8bb
Revises: c69e7933e231
Create Date: 2024-12-25 13:04:42.350090

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '879cae28f8bb'
down_revision: Union[str, None] = 'c69e7933e231'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
