"""
Configuration Management for Manus Agent System
"""
from pydantic_settings import BaseSettings
from typing import List, Optional
import os
import secrets


class Settings(BaseSettings):
    """Application settings loaded from environment variables"""

    # Application
    APP_NAME: str = "Manus Agent System"
    DEBUG: bool = False
    ENVIRONMENT: str = "production"

    # Security
    SECRET_KEY: str = secrets.token_urlsafe(32)

    # API Keys
    OPENAI_API_KEY: Optional[str] = None
    ANTHROPIC_API_KEY: Optional[str] = None
    NEWS_API_KEY: Optional[str] = None

    # Database
    # On Render.com: auto-set to PostgreSQL connection string
    # Locally: defaults to SQLite
    DATABASE_URL: str = "sqlite:///./manus_agent.db"

    # Redis (for Celery background tasks)
    # On Render.com: auto-set to Redis connection string
    REDIS_URL: str = "redis://localhost:6379/0"

    # LLM Settings
    LLM_PROVIDER: str = "openai"  # "openai" or "anthropic"
    LLM_MODEL: str = "gpt-3.5-turbo"
    LLM_MAX_TOKENS: int = 2000
    LLM_TEMPERATURE: float = 0.7

    # CORS
    ALLOWED_ORIGINS: List[str] = ["*"]

    # News settings
    NEWS_FETCH_INTERVAL: int = 30  # minutes
    NEWS_CATEGORIES: List[str] = ["technology", "business", "science"]

    @property
    def is_postgresql(self) -> bool:
        """Check if using PostgreSQL database"""
        return self.DATABASE_URL.startswith("postgresql") or self.DATABASE_URL.startswith("postgres")

    @property
    def celery_broker_url(self) -> str:
        """Celery broker URL (Redis)"""
        return self.REDIS_URL

    @property
    def celery_result_backend(self) -> str:
        """Celery result backend (Redis)"""
        return self.REDIS_URL

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = True
        # Allow extra fields from environment
        extra = "ignore"


settings = Settings()
