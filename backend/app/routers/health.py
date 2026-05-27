from fastapi import APIRouter
import psycopg2
import redis

from app.config import settings
from app.observability.metrics import metrics_response

router = APIRouter(prefix="/api", tags=["Health"])


@router.get("/health/live")
def liveness():
    return {"status": "ok"}


@router.get("/health/ready")
def readiness():
    checks = {"database": False, "redis": False}

    try:
        conn = psycopg2.connect(settings.DATABASE_URL)
        with conn.cursor() as cur:
            cur.execute("SELECT 1")
            cur.fetchone()
        conn.close()
        checks["database"] = True
    except Exception:
        checks["database"] = False

    try:
        redis_url = settings.REDIS_URL or settings.CELERY_BROKER_URL
        if redis_url:
            client = redis.Redis.from_url(redis_url)
            checks["redis"] = bool(client.ping())
    except Exception:
        checks["redis"] = False

    all_ready = all(checks.values())
    return {
        "status": "ready" if all_ready else "degraded",
        "checks": checks,
    }


@router.get("/metrics")
def metrics():
    return metrics_response()
