"""delete user_id from studentmarks

Revision ID: c1e490709f0c
Revises: a0a1c634fb95
Create Date: 2024-12-25 13:02:31.984900

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'c1e490709f0c'
down_revision: Union[str, None] = 'a0a1c634fb95'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
