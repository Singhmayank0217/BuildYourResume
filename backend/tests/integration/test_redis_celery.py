import pytest

from app.celery_app import ping_task


@pytest.mark.integration
def test_redis_is_reachable(redis_client):
    assert redis_client.ping() is True


@pytest.mark.integration
def test_celery_ping_task_idempotent_behavior(redis_client):
    result1 = ping_task.apply(args=["resume-123"])
    payload1 = result1.get(timeout=10)
    assert payload1["status"] == "ok"

    result2 = ping_task.apply(args=["resume-123"])
    payload2 = result2.get(timeout=10)
    assert payload2["status"] in {"ok", "duplicate"}
