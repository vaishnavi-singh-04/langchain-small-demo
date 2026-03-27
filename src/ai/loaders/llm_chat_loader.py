from functools import lru_cache

from langchain_nvidia_ai_endpoints import ChatNVIDIA
from src.utils.env_loader import settings

@lru_cache()
def get_llm():
    return ChatNVIDIA(
        model="meta/llama3-70b-instruct",
        api_key=settings.NVIDIA_API_KEY,
        temperature=0,
    )