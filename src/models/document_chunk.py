from sqlalchemy import UUID, Column, Text, Integer, ForeignKey, TIMESTAMP
from sqlalchemy.sql import func
from pgvector.sqlalchemy import Vector
import uuid
from src.database.database import Base



class DocumentChunk(Base):
    __tablename__ = "document_chunks"

    id = Column(UUID, primary_key=True, default=lambda: uuid.uuid4())
    document_id = Column(UUID, ForeignKey("documents.id", ondelete="CASCADE"))
    content = Column(Text, nullable=False)
    embedding = Column(Vector(4096))
    chunk_index = Column(Integer)
    created_at = Column(TIMESTAMP(timezone=True), server_default=func.now())