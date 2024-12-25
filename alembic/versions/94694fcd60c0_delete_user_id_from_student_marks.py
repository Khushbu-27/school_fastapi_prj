"""delete user_id from student_marks

Revision ID: 94694fcd60c0
Revises: 879cae28f8bb
Create Date: 2024-12-25 13:05:47.606382

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '94694fcd60c0'
down_revision: Union[str, None] = '879cae28f8bb'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
