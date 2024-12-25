"""delete user_id from studentmarks

Revision ID: a0a1c634fb95
Revises: ee22f1fe51d2
Create Date: 2024-12-25 13:00:14.360790

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'a0a1c634fb95'
down_revision: Union[str, None] = 'ee22f1fe51d2'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
