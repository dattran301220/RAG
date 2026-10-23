from pydantic_settings import BaseSettings
from pydantic import computed_field
from typing import Optional

class Settings(BaseSettings):
    # 1. Cấu hình chung cho FastAPI
    PROJECT_NAME: str = "Academic RAG Assistant"
    ENVIRONMENT: str = "development"
    API_V1_STR: str = "/api/v1"
    SECRET_KEY: str = "academic_rag_secret_key_change_me_in_production_12345"

    # 2. Cơ sở dữ liệu PostgreSQL
    POSTGRES_SERVER: str = "postgres"
    POSTGRES_PORT: int = 5432
    POSTGRES_USER: str = "rag_admin"
    POSTGRES_PASSWORD: str = "rag_password123"
    POSTGRES_DB: str = "rag_academic_db"

    # Tự động ghép chuỗi kết nối SQLAlchemy: postgresql://user:pass@host:port/db
    @computed_field
    @property
    def SQLALCHEMY_DATABASE_URI(self) -> str:
        return (
            f"postgresql+psycopg2://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@"
            f"{self.POSTGRES_SERVER}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"
        )

    # 3. Object Storage MinIO (S3)
    MINIO_ENDPOINT: str = "minio:9000"
    MINIO_ROOT_USER: str = "minio_admin"
    MINIO_ROOT_PASSWORD: str = "minio_password123"
    MINIO_BUCKET_NAME: str = "academic-docs"
    MINIO_PUBLIC_URL: str = "http://localhost:9000"
    MINIO_SECURE: bool = False

    # 4. Vector Database Qdrant
    QDRANT_HOST: str = "qdrant"
    QDRANT_PORT: int = 6333
    QDRANT_COLLECTION_NAME: str = "academic_knowledge"

    # 5. Message Queue Redis & Celery
    REDIS_HOST: str = "redis"
    REDIS_PORT: int = 6379
    CELERY_BROKER_URL: str = "redis://redis:6379/0"
    CELERY_RESULT_BACKEND: str = "redis://redis:6379/1"

    # 6. Mô hình AI Offline Ollama
    OLLAMA_BASE_URL: str = "http://host.docker.internal:11434"
    OLLAMA_LLM_MODEL: str = "qwen2.5:latest"
    OLLAMA_EMBED_MODEL: str = "bge-m3:latest"

    # Cấu hình bảo Pydantic tự động nạp từ file .env
    class Config:
        env_file = ".env"
        extra = "ignore"  # Bỏ qua nếu có biến thừa trong file .env
settings = Settings()
