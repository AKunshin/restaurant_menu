"""Add cascade delete for submenu, dish in releations

Revision ID: 061d38b000d9
Revises: 9a925d0753f3
Create Date: 2024-01-22 08:54:24.784491

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '061d38b000d9'
down_revision: Union[str, None] = '9a925d0753f3'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint('dishes_submenu_id_fkey', 'dishes', type_='foreignkey')
    op.create_foreign_key(None, 'dishes', 'submenus', ['submenu_id'], ['id'])
    op.drop_constraint('submenus_menu_id_fkey', 'submenus', type_='foreignkey')
    op.create_foreign_key(None, 'submenus', 'menus', ['menu_id'], ['id'])
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'submenus', type_='foreignkey')
    op.create_foreign_key('submenus_menu_id_fkey', 'submenus', 'menus', ['menu_id'], ['id'], ondelete='CASCADE')
    op.drop_constraint(None, 'dishes', type_='foreignkey')
    op.create_foreign_key('dishes_submenu_id_fkey', 'dishes', 'submenus', ['submenu_id'], ['id'], ondelete='CASCADE')
    # ### end Alembic commands ###