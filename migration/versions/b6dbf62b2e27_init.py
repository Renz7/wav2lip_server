"""init

Revision ID: b6dbf62b2e27
Revises: 
Create Date: 2023-11-29 11:16:16.078667

"""
from typing import Sequence, Union

from alembic import op
from internal.db.models import DigitalTemplate
from sqlalchemy import Column, String

# revision identifiers, used by Alembic.
revision: str = 'b6dbf62b2e27'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        DigitalTemplate.__tablename__,
        Column("preview_pic", String(512), nullable=True)
    )


def downgrade() -> None:
    pass
