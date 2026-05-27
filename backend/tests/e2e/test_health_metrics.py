import pytest


@pytest.mark.e2e
@pytest.mark.asyncio
async def test_health_and_metrics_endpoints(async_client):
    live = await async_client.get("/api/health/live")
    assert live.status_code == 200
    assert live.json()["status"] == "ok"

    metrics = await async_client.get("/api/metrics")
    assert metrics.status_code == 200
    assert "http_requests_total" in metrics.text
