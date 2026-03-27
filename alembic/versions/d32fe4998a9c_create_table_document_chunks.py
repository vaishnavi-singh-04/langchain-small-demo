"""create-table_document_chunks

Revision ID: d32fe4998a9c
Revises: e10c172b2be5
Create Date: 2026-03-18 12:33:52.937783

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = 'd32fe4998a9c'
down_revision: Union[str, Sequence[str], None] = 'e10c172b2be5'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.execute("""
        CREATE TABLE document_chunks (
            id UUID PRIMARY KEY,
            document_id UUID REFERENCES documents(id) ON DELETE CASCADE,
            content TEXT NOT NULL,
            embedding VECTOR(1024),
            chunk_index INT,
            created_at TIMESTAMP WITH TIME ZONE DEFAULT now()
        );
    """)

def downgrade():
    op.execute("DROP TABLE IF EXISTS document_chunks;")
