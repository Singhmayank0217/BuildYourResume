import io

import pytest
from starlette.datastructures import UploadFile

from app.routers import auth as auth_router
from app.routers import upload as upload_router


@pytest.mark.integration
@pytest.mark.asyncio
async def test_upload_api_parses_docx(async_client, fastapi_test_app, monkeypatch):
    fastapi_test_app.dependency_overrides[auth_router.get_current_user] = lambda: 1

    async def fake_parse_resume(file):
        return {"full_name": "Alex Johnson", "skills": ["python"]}

    monkeypatch.setattr(upload_router, "parse_resume", fake_parse_resume)

    files = {
        "file": (
            "resume.docx",
            b"fake-content",
            "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        )
    }

    response = await async_client.post("/api/resume/upload", files=files)

    assert response.status_code == 200
    body = response.json()
    assert body["parsed_resume"]["full_name"] == "Alex Johnson"


@pytest.mark.integration
@pytest.mark.asyncio
async def test_upload_api_rejects_invalid_extension(async_client, fastapi_test_app):
    fastapi_test_app.dependency_overrides[auth_router.get_current_user] = lambda: 1

    files = {"file": ("resume.txt", b"hello", "text/plain")}
    response = await async_client.post("/api/resume/upload", files=files)

    assert response.status_code == 400
    assert "Only PDF or DOCX" in response.json()["detail"]
