"""delete otp from users table

Revision ID: 52d95f7ff9da
Revises: 4524ea50efee
Create Date: 2024-12-10 12:03:48.064016

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '52d95f7ff9da'
down_revision: Union[str, None] = '4524ea50efee'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('users', 'otp')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('otp', sa.VARCHAR(length=6), autoincrement=False, nullable=True))
    # ### end Alembic commands ###
