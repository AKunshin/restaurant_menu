"""Unique title for dish and submenu

Revision ID: 4e2a4b9765ec
Revises: bf03ea785947
Create Date: 2024-01-22 11:03:10.686913

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '4e2a4b9765ec'
down_revision: Union[str, None] = 'bf03ea785947'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_unique_constraint(None, 'dishes', ['title'])
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'dishes', type_='unique')
    # ### end Alembic commands ###
