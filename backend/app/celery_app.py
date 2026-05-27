from celery import Celery
from celery.utils.log import get_task_logger
from redis import Redis

from app.config import settings
from app.observability.metrics import WORKER_TASK_COUNT
from app.services.task_runtime import build_idempotency_key, utcnow_iso

broker_url = settings.CELERY_BROKER_URL or settings.REDIS_URL or "redis://localhost:6379/0"

celery = Celery("smart_resume_builder", broker=broker_url, backend=broker_url)
celery.conf.update(
    task_serializer="json",
    result_serializer="json",
    accept_content=["json"],
    task_track_started=True,
    task_acks_late=True,
    worker_prefetch_multiplier=1,
)

logger = get_task_logger(__name__)


def _redis_client() -> Redis:
    return Redis.from_url(settings.REDIS_URL or broker_url)


@celery.task(bind=True, max_retries=5, autoretry_for=(Exception,), retry_backoff=True, retry_jitter=True)
def ping_task(self, payload: str = "ok"):
    WORKER_TASK_COUNT.labels("ping_task", "started").inc()
    logger.info("ping_task_started", extra={"task_id": self.request.id})

    idempotency_key = build_idempotency_key("ping", payload)
    lock_key = f"task-lock:{idempotency_key}"

    client = _redis_client()
    acquired = client.set(lock_key, utcnow_iso(), nx=True, ex=120)
    if not acquired:
        WORKER_TASK_COUNT.labels("ping_task", "duplicate").inc()
        return {"status": "duplicate", "payload": payload}

    WORKER_TASK_COUNT.labels("ping_task", "success").inc()
    return {"status": "ok", "payload": payload, "idempotency_key": idempotency_key}
