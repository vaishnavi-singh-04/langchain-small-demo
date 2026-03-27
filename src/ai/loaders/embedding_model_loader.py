from functools import lru_cache
from langchain_nvidia_ai_endpoints import NVIDIAEmbeddings
from src.utils.env_loader import settings

@lru_cache()
def get_embedding_model():
    return NVIDIAEmbeddings(
        model="nvidia/nv-embed-v1",
        api_key=settings.NVIDIA_API_KEY,
    )