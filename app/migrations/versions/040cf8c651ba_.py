"""empty message

Revision ID: 040cf8c651ba
Revises: d94952b96146
Create Date: 2024-06-25 19:15:44.942054

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '040cf8c651ba'
down_revision: Union[str, None] = 'd94952b96146'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('Tasks', sa.Column('is_completed', sa.Boolean(), nullable=False))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('Tasks', 'is_completed')
    # ### end Alembic commands ###
