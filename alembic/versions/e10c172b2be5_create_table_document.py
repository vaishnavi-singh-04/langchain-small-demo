"""create-table_document

Revision ID: e10c172b2be5
Revises: 6e40732098d7
Create Date: 2026-03-18 12:28:14.213950

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'e10c172b2be5'
down_revision: Union[str, Sequence[str], None] = '6e40732098d7'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.execute("""
        CREATE TABLE documents (
            id UUID PRIMARY KEY,
            file_name TEXT NOT NULL,
            created_at TIMESTAMP WITH TIME ZONE DEFAULT now()
        );
    """)

def downgrade():
    op.execute("DROP TABLE IF EXISTS documents;")
