from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import text
from app.db.session import get_db
from app.core.config import settings
import redis
import httpx

router = APIRouter()


@router.get("", summary="Kiểm tra trạng thái hệ thống")
def check_health(db: Session = Depends(get_db)):
    health_status = {
        "status": "healthy",
        "services": {
            "database": "unknown",
            "redis": "unknown",
            "qdrant": "unknown",
            "minio": "unknown"
        }
    }

    # 1. Kiểm tra kết nối PostgreSQL
    try:
        db.execute(text("SELECT 1"))
        health_status["services"]["database"] = "connected"
    except Exception as e:
        health_status["services"]["database"] = f"error: {str(e)}"
        health_status["status"] = "degraded"

    # 2. Kiểm tra Redis
    try:
        r = redis.Redis(
            host=settings.REDIS_HOST,
            port=settings.REDIS_PORT,
            socket_timeout=2
        )
        if r.ping():
            health_status["services"]["redis"] = "connected"
    except Exception as e:
        health_status["services"]["redis"] = f"error: {str(e)}"
        health_status["status"] = "degraded"

    # 3. Kiểm tra Qdrant Vector DB
    try:
        qdrant_url = (
            f"http://{settings.QDRANT_HOST}:{settings.QDRANT_PORT}/healthz"
        )
        res = httpx.get(qdrant_url, timeout=2.0)
        if res.status_code == 200:
            health_status["services"]["qdrant"] = "connected"
    except Exception as e:
        health_status["services"]["qdrant"] = f"error: {str(e)}"
        health_status["status"] = "degraded"

    # 4. Kiểm tra Object Storage MinIO
    try:
        scheme = "https" if settings.MINIO_SECURE else "http"
        minio_url = f"{scheme}://{settings.MINIO_ENDPOINT}/minio/health/live"
        res = httpx.get(minio_url, timeout=2.0)
        if res.status_code == 200:
            health_status["services"]["minio"] = "connected"
    except Exception as e:
        health_status["services"]["minio"] = f"error: {str(e)}"
        health_status["status"] = "degraded"

    return health_status
