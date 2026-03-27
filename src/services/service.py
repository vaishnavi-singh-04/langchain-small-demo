from uuid import uuid4, UUID
from typing import cast
from src.logger.logger import logger
from langchain_core.prompts import ChatPromptTemplate
from langchain_nvidia_ai_endpoints import ChatNVIDIA, NVIDIAEmbeddings
from src.ai.pipelines.text_splitter_pipeline import TextSplitterLlmPipeline
from src.repositories.repository import Repository
from src.models.document import Document
from src.models.document_chunk import DocumentChunk

class Service:
    def __init__(
            self,
            repository: Repository,
            text_splitter: TextSplitterLlmPipeline,
            embedding_model: NVIDIAEmbeddings,   
            llm: ChatNVIDIA,                     
            prompt: ChatPromptTemplate,
        ):
            self.repo = repository
            self.splitter = text_splitter
            self.embedding = embedding_model
            self.llm = llm
            self.prompt = prompt
            
    async def ingest_method(self, file_name:str, text:str) -> UUID:
        logger.info(f"Starting ingestion for document: {file_name}")
        
        if not text or not text.strip():
            logger.error(f"Ingestion failed for {file_name}: Text is empty.")
            raise ValueError("Text cannot be empty")
        
        document: Document = await self.repo.save_document(Document(file_name=file_name))
        logger.debug(f"Document record saved with ID: {document.id}")
        
        chunks = self.splitter.text_split(text=text)
        logger.debug(f"Document {file_name} split into {len(chunks) if chunks else 0} chunks.")
        
        if not chunks:
            logger.error(f"Ingestion failed for {file_name}: No chunks generated.")
            raise ValueError("No chunks generated from text")
        
        embeddings =  self.embedding.embed_documents(chunks)
        logger.debug(f"Generated {len(embeddings)} embeddings for document {file_name}.")
        
        if len(chunks) != len(embeddings):
            logger.error(f"Mismatch between chunk count ({len(chunks)}) and embedding count ({len(embeddings)}).")
            raise RuntimeError("Mismatch between chunks and embeddings")

        chunk_entities: list[DocumentChunk] = [
            DocumentChunk(
                document_id=cast(UUID, document.id),
                content=chunk,
                embedding=embeddings[i],
                chunk_index=i,
            )
            for i, chunk in enumerate(chunks)
        ]
        
        await self.repo.save_chunks(chunk_entities)
        logger.info(f"Successfully ingested document {file_name} with ID {document.id}.")

        return cast(UUID, document.id)
    
    
    
    
    async def ask_question(self, question: str, document_id: str) -> str:
        logger.info(f"Received question for document {document_id}: '{question}'")
        
        # 1. Validate input
        if not question or not question.strip():
            logger.error("Question validation failed: Question is empty.")
            raise ValueError("Question cannot be empty")
        if not document_id:
            logger.error("Question validation failed: Document ID is empty.")
            raise ValueError("Document ID cannot be empty")

        # 2. Generate query embedding
        logger.debug("Generating query embedding...")
        query_embedding: list[float] = self.embedding.embed_query(question)

        # 3. Retrieve relevant chunks
        logger.debug(f"Searching for similar chunks in document {document_id}...")
        chunks: list[str] = await self.repo.similarity_search(query_embedding, doc_id=document_id)

        if not chunks:
            logger.info(f"No relevant context chunks found for document {document_id}.")
            return "No relevant information found."

        # 4. Build context
        context: str = "\n".join(chunks)

        # 5. Format prompt
        messages = self.prompt.format_messages(
            context=context,
            question=question,
        )

        # 6. Call LLM
        logger.debug("Prompt built and sent to LLM for completion...")
        response = self.llm.invoke(messages)
        
        logger.info(f"Successfully generated answer for document {document_id}.")

        return str(response.content)