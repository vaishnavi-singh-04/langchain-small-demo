from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, text
from typing import List
from uuid import UUID

from src.models.document import Document
from src.models.document_chunk import DocumentChunk


class Repository:
    def __init__(self, session: AsyncSession):
        self.session = session

    # Document Methods
    async def save_document(self, entity: Document) -> Document:
        self.session.add(entity)
        await self.session.commit()
        await self.session.refresh(entity)
        return entity

    async def get_document(self, doc_id: UUID) -> Document | None:
        result = await self.session.execute(
            select(Document).where(Document.id == doc_id)
        )
        return result.scalar_one_or_none()

    # Chunck Methods
    async def save_chunks(self, chunks: List[DocumentChunk]):
        self.session.add_all(chunks)
        await self.session.commit()

    async def similarity_search(self, query_embedding: list, doc_id: str, k: int = 5):
        stmt = text("""
            SELECT content
            FROM document_chunks
            WHERE document_id = :doc_id
            ORDER BY embedding <-> :embedding
            LIMIT :k
        """)

        result = await self.session.execute(
            stmt,
            {"embedding": str(query_embedding), "k": k, "doc_id": str(doc_id)},
        )

        return [row[0] for row in result.fetchall()]
