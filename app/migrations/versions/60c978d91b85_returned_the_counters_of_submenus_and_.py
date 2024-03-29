"""Returned the counters of submenus and dishes fields

Revision ID: 60c978d91b85
Revises: 0da4a30f2280
Create Date: 2024-01-29 23:11:19.555845

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '60c978d91b85'
down_revision: Union[str, None] = '0da4a30f2280'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('menus', 'dishes_count')
    op.drop_column('menus', 'submenus_count')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('menus', sa.Column('submenus_count', sa.INTEGER(), autoincrement=False, nullable=True))
    op.add_column('menus', sa.Column('dishes_count', sa.INTEGER(), autoincrement=False, nullable=True))
    # ### end Alembic commands ###
