from pydantic_settings import BaseSettings
from typing import Optional, List


class Settings(BaseSettings):
    DATABASE_URL: str
    JWT_SECRET: str

    ENVIRONMENT: str = "development"
    LOG_LEVEL: str = "INFO"
    ENABLE_METRICS: bool = True
    SERVICE_NAME: str = "smart-resume-builder"
    CORS_ALLOWED_ORIGINS: List[str] = ["*"]

    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7

    OPENAI_API_KEY: Optional[str] = None
    LLM_PROVIDER: str = "local"
    REDIS_URL: Optional[str] = None
    CELERY_BROKER_URL: Optional[str] = None
    S3_ENDPOINT: Optional[str] = None
    S3_ACCESS_KEY: Optional[str] = None
    S3_SECRET_KEY: Optional[str] = None
    S3_BUCKET: Optional[str] = None

    class Config:
        env_file = ".env"


settings = Settings()
