"""remove user_id from student_marks

Revision ID: 5faa7f34c5d0
Revises: c1b582d75150
Create Date: 2024-12-25 14:16:04.327681

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '5faa7f34c5d0'
down_revision: Union[str, None] = 'c1b582d75150'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    
    op.drop_column('student_marks', 'user_id')


def downgrade() -> None:
    
    op.add_column('student_marks', sa.Column('user_id', sa.Integer(), nullable=False))
    op.create_foreign_key(None, 'student_marks', 'users', ['user_id'], ['id'])
