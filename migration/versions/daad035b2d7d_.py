"""empty message

Revision ID: daad035b2d7d
Revises: 
Create Date: 2024-01-18 12:03:28.365793

"""
from typing import Sequence, Union

# revision identifiers, used by Alembic.
revision: str = 'daad035b2d7d'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    from internal.db import database
    database.init(True)
    pass


def downgrade() -> None:
    pass
