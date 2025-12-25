from pydantic_settings import BaseSettings
from typing import Optional


class VectorStoreSettings(BaseSettings):
    QDRANT_URL: str = "http://localhost:6333"
    QDRANT_API_KEY: Optional[str] = None
    VECTOR_STORE_COLLECTION_NAME: str = "robotics_textbook"
    
    class Config:
        env_file = "../.env"  # Relative to this file's location


settings = VectorStoreSettings()