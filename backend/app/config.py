"""
Configuration management for USPTO Trademark Risk Analyzer
"""
from pydantic_settings import BaseSettings
from typing import List


class Settings(BaseSettings):
    """Application settings loaded from environment variables"""

    # API Keys
    USPTO_API_KEY: str
    ANTHROPIC_API_KEY: str

    # Application
    ENVIRONMENT: str = "development"
    DEBUG: bool = True
    API_V1_PREFIX: str = "/api/v1"

    # CORS
    CORS_ORIGINS: List[str] = [
        "http://localhost:3000",
        "http://127.0.0.1:3000"
    ]

    # USPTO API Configuration
    USPTO_BASE_URL: str = "https://data.uspto.gov"
    USPTO_TSDR_URL: str = "https://tsdr.uspto.gov/statusxml"

    # Rate Limiting
    RATE_LIMIT_PER_MINUTE: int = 60

    # AI Analysis
    CLAUDE_MODEL: str = "claude-sonnet-4-5-20250929"
    MAX_RESULTS_TO_ANALYZE: int = 50

    class Config:
        env_file = ".env"
        case_sensitive = True


# Create global settings instance
settings = Settings()
