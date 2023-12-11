"""用户头像和昵称记录

Revision ID: a60febc2a910
Revises: b6dbf62b2e27
Create Date: 2023-12-11 09:49:53.757573

"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = 'a60febc2a910'
down_revision: Union[str, None] = 'b6dbf62b2e27'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('user',
                  sa.Column('avatar', sa.BLOB(), nullable=True))
    op.add_column('user',
                  sa.Column('nickname', sa.String(length=256), nullable=True))
    print("upgrade success")


def downgrade() -> None:
    op.drop_column('user', 'nickname')
    op.drop_column('user', 'avatar')
