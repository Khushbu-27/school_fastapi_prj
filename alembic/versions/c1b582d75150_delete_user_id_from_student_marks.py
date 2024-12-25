"""delete user_id from student_marks

Revision ID: c1b582d75150
Revises: 94694fcd60c0
Create Date: 2024-12-25 14:02:06.863746

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'c1b582d75150'
down_revision: Union[str, None] = '94694fcd60c0'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.drop_column('student_marks', 'user_id')


def downgrade() -> None:
    op.add_column('student_marks', sa.Column('user_id', nullable=False))
