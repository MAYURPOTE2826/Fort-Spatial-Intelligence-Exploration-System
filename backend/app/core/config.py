from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import List
import os
import warnings


class Settings(BaseSettings):
    PROJECT_NAME: str = "FortSight AI"
    VERSION: str = "1.0.0"
    API_V1_STR: str = "/api/v1"

    ENVIRONMENT: str = "development"
    DEBUG: bool = True

    # Database
    DATABASE_URL: str = "postgresql://postgres:postgres@db:5432/fortsight"
    DB_POOL_SIZE: int = 5
    DB_MAX_OVERFLOW: int = 10

    # Redis
    REDIS_URL: str = "redis://redis:6379/0"

    # DEM / Terrain
    # Set to a local file path for the Copernicus DEM GeoTIFF, e.g. "data/dem/maharashtra_dem.tif"
    # If empty, elevation lookups will return None (visibility will classify as UNCERTAIN).
    DEM_DATA_DIR: str = "data/dem"
    DEM_DEFAULT_FILE: str = ""  # e.g. "maharashtra_30m.tif" — leave empty to disable DEM

    # Security
    SECRET_KEY: str = "a-very-secret-key-that-should-be-changed-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 8  # 8 days

    # CORS
    BACKEND_CORS_ORIGINS: List[str] = [
        "http://localhost:5173",
        "http://localhost:3000",
        "http://localhost",
    ]

    # Rate limiting
    RATE_LIMIT_VISIBILITY: str = "10/minute"
    RATE_LIMIT_CHAT: str = "20/minute"

    # LLM
    GEMINI_API_KEY: str = ""
    GEMINI_MODEL: str = "gemini-2.5-flash"

    # Embedding
    EMBEDDING_MODEL: str = "paraphrase-multilingual-MiniLM-L12-v2"
    EMBEDDING_DIM: int = 384

    # Cache TTL (hours)
    VISIBILITY_CACHE_TTL_HOURS: int = 24
    NETWORK_CACHE_TTL_HOURS: int = 168  # 7 days

    # Logging
    LOG_LEVEL: str = "INFO"
    LOG_JSON: bool = False  # Set True in production for structured JSON logs

    model_config = SettingsConfigDict(
        env_file=".env",
        case_sensitive=True,
        extra="ignore",
    )

    def validate_production(self) -> None:
        """Warn about insecure defaults in production."""
        if self.ENVIRONMENT == "production":
            if self.SECRET_KEY == "a-very-secret-key-that-should-be-changed-in-production":
                raise ValueError(
                    "SECRET_KEY must be changed from the default value in production. "
                    "Generate one with: python -c \"import secrets; print(secrets.token_hex(32))\""
                )
            if not self.GEMINI_API_KEY:
                warnings.warn("GEMINI_API_KEY is not set. RAG chatbot will not function.", stacklevel=2)
            if not self.DEM_DEFAULT_FILE:
                warnings.warn(
                    "DEM_DEFAULT_FILE is not set. Visibility will fall back to UNCERTAIN for all results.",
                    stacklevel=2,
                )


settings = Settings()

# Validate on import in production
if settings.ENVIRONMENT == "production":
    try:
        settings.validate_production()
    except ValueError as e:
        raise SystemExit(f"Configuration error: {e}") from e
