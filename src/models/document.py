from sqlalchemy import UUID, Column, String, TIMESTAMP
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import uuid

from src.database.database import Base

class Document(Base):
    __tablename__ = "documents"

    id = Column(UUID, primary_key=True, default=lambda: (uuid.uuid4()))
    file_name = Column(String, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), server_default=func.now())
    
    chunks = relationship("DocumentChunk", backref="document", cascade="all, delete")