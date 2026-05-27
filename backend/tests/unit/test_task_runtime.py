import pytest

from app.services.task_runtime import build_idempotency_key, compute_retry_delay


@pytest.mark.unit
def test_idempotency_key_deterministic():
    key1 = build_idempotency_key("rewrite", "resume-1")
    key2 = build_idempotency_key("rewrite", "resume-1")
    key3 = build_idempotency_key("rewrite", "resume-2")

    assert key1 == key2
    assert key1 != key3


@pytest.mark.unit
def test_retry_delay_exponential_and_capped():
    assert compute_retry_delay(0) == 2
    assert compute_retry_delay(3) == 16
    assert compute_retry_delay(20, max_seconds=60) == 60
