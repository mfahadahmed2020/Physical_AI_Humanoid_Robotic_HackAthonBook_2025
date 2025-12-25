from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    DATABASE_URL: str = "postgresql://user:password@localhost:5432/robotics_textbook"
    TEST_DATABASE_URL: str = "postgresql://user:password@localhost:5432/robotics_textbook_test"

    class Config:
        env_file = ".env"


settings = Settings()