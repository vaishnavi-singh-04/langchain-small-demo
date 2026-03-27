from fastapi import Depends

from src.database.database import AsyncSessionLocal
from src.repositories.repository import Repository
from src.services.service import Service
from src.ai.loaders.embedding_model_loader import get_embedding_model
from src.ai.loaders.llm_chat_loader import get_llm
from src.ai.prompt_templates.prompt_template import get_prompt
from src.ai.pipelines.text_splitter_pipeline import TextSplitterLlmPipeline
from sqlalchemy.ext.asyncio import AsyncSession

# DB session
async def get_db():
    async with AsyncSessionLocal() as session:
        yield session


# Service dependency
def get_service(
    db: AsyncSession = Depends(get_db),  
):
    repo = Repository(db)
    splitter = TextSplitterLlmPipeline()

    return Service(
        repository=repo,
        text_splitter=splitter,
        embedding_model=get_embedding_model(),
        llm=get_llm(),
        prompt=get_prompt(),
    )