"""add_vector_index

Revision ID: 88c0ef049a66
Revises: d32fe4998a9c
Create Date: 2026-03-18 14:31:55.371553

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '88c0ef049a66'
down_revision: Union[str, Sequence[str], None] = 'd32fe4998a9c'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.execute("""
        CREATE INDEX document_chunks_embedding_idx
        ON document_chunks
        USING ivfflat (embedding vector_cosine_ops)
        WITH (lists = 100);
    """)

def downgrade():
    op.execute("""
        DROP INDEX document_chunks_embedding_idx;
    """)