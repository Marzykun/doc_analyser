from pydantic_settings import BaseSettings, SettingsConfigDict
from functools import lru_cache
from typing import Optional

class Settings(BaseSettings):
    """Application configuration"""
    DEBUG: bool = True
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    FRONTEND_URL: str = "http://localhost:5173"
    MAX_UPLOAD_SIZE: int = 10485760  # 10MB
    SPACY_MODEL: str = "en_core_web_sm"
    LOG_LEVEL: str = "INFO"
    GEMINI_API_KEY: Optional[str] = None
    GEMINI_MODEL: str = "gemini-1.5-flash"

    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore",
    )

@lru_cache()
def get_settings():
    return Settings()
