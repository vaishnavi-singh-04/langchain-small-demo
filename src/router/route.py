from fastapi import APIRouter, UploadFile, File, HTTPException, Depends
from src.schemas.rag_request_response_schema import UploadResponse, QueryRequest, QueryResponse
from src.services.service import Service
from src.dependencies.dependency import get_service  
import io
import PyPDF2
from typing import cast
from uuid import UUID

router = APIRouter()


@router.post("/upload", response_model=UploadResponse, summary="Upload a PDF document")
async def upload_pdf(
    file: UploadFile = File(..., description="Must be a PDF file."),
    service: Service = Depends(get_service),   
):
    try:
        if not file.filename or not file.filename.lower().endswith('.pdf'):
            raise HTTPException(status_code=400, detail="Only PDF files are allowed.")

        if file.content_type and file.content_type != "application/pdf":
            raise HTTPException(status_code=400, detail="Invalid content type. Only application/pdf is allowed.")

        # Read file
        content = await file.read()

        # Try parsing as PDF first
        try:
            pdf_reader = PyPDF2.PdfReader(io.BytesIO(content))
            text = ""
            for page in pdf_reader.pages:
                extracted = page.extract_text()
                if extracted:
                    text += extracted + "\n"
        except Exception:
            # Fallback to UTF-8 decoding if not a valid PDF
            try:
                text = content.decode("utf-8")
            except Exception:
                raise HTTPException(status_code=400, detail="Could not extract text from document.")

        if not text.strip():
            raise HTTPException(status_code=400, detail="No extractable text found in document.")

        # Call service
        document_id = await service.ingest_method(
            file_name=file.filename or "unknown.pdf",
            text=text,
        )

        return UploadResponse(
            document_id=cast(UUID, document_id),
            message="Document uploaded successfully",
        )

    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/ask", response_model=QueryResponse)
async def ask_question(
    request: QueryRequest,
    service: Service = Depends(get_service),
):
    try:
        answer = await service.ask_question(
            question=request.question,
            document_id=str(request.document_id)
        )
        return QueryResponse(answer=answer)

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))