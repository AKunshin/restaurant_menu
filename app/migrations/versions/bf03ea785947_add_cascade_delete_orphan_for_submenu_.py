"""Add cascade delete-orphan for submenu, dish in releations

Revision ID: bf03ea785947
Revises: bd146d636fc0
Create Date: 2024-01-22 09:26:02.788036

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'bf03ea785947'
down_revision: Union[str, None] = 'bd146d636fc0'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    pass
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    pass
    # ### end Alembic commands ###