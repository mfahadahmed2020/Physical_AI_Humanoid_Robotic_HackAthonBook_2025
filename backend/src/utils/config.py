from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    # Database settings
    database_url: str = "postgresql://user:password@localhost:5432/robotics_textbook"
    
    # JWT settings
    secret_key: str = "your-secret-key-change-in-production"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    
    # Qdrant settings
    qdrant_url: str = "http://localhost:6333"
    qdrant_api_key: Optional[str] = None
    
    # OpenAI settings
    openai_api_key: str = ""
    
    # Application settings
    app_name: str = "Physical AI & Humanoid Robotics Textbook API"
    debug: bool = True
    
    class Config:
        env_file = ".env"


settings = Settings()