import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    NVIDIA_API_KEY = os.getenv("NVIDIA_KEY")

settings = Settings()