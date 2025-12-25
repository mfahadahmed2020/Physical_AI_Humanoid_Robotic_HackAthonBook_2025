from pydantic_settings import BaseSettings
from typing import Optional


class AISettings(BaseSettings):
    OPENAI_API_KEY: str  # Required
    OPENAI_MODEL: str = "gpt-4-turbo"
    EMBEDDING_MODEL: str = "text-embedding-ada-002"
    
    class Config:
        env_file = "../.env"  # Relative to this file's location


settings = AISettings()