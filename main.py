from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.router.route import router as document_router


app = FastAPI(
    title="LangChain RAG API",
    description="API for uploading documents and asking questions.",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(document_router, prefix="/api/v1", tags=["Documents"])


@app.get("/")
async def root():
    return {"message": "Welcome to the Document RAG API!"}
