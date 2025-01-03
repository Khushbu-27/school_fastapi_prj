"""Change phone_number to String and update otp column

Revision ID: 4524ea50efee
Revises: a1f4c50ae82d
Create Date: 2024-12-10 11:54:27.274624

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '4524ea50efee'
down_revision: Union[str, None] = 'a1f4c50ae82d'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('users', 'otp',
               existing_type=sa.INTEGER(),
               type_=sa.String(length=6),
               existing_nullable=True)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('users', 'otp',
               existing_type=sa.String(length=6),
               type_=sa.INTEGER(),
               existing_nullable=True)
    # ### end Alembic commands ###
