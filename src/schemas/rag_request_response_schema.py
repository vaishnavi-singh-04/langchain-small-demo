from pydantic import BaseModel
from uuid import UUID


class QueryRequest(BaseModel):
    document_id: UUID
    question: str


class QueryResponse(BaseModel):
    answer: str


class UploadResponse(BaseModel):
    document_id: UUID
    message: str