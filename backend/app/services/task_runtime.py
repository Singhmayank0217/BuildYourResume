import hashlib
from datetime import datetime


def build_idempotency_key(namespace: str, payload: str) -> str:
    digest = hashlib.sha256(f"{namespace}:{payload}".encode("utf-8")).hexdigest()
    return f"{namespace}:{digest}"


def compute_retry_delay(retries: int, base_seconds: int = 2, max_seconds: int = 300) -> int:
    if retries <= 0:
        return base_seconds
    delay = base_seconds * (2 ** retries)
    return min(delay, max_seconds)


def utcnow_iso() -> str:
    return datetime.utcnow().isoformat() + "Z"
