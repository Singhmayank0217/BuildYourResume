import pytest

from app.routers import auth as auth_router


@pytest.mark.integration
def test_register_and_login_api_with_mocked_db(fastapi_test_app, monkeypatch):
    inserted_user = {
        "id": 1,
        "email": "user@example.com",
        "first_name": "Test",
        "last_name": "User",
        "phone": None,
        "location": None,
        "linkedin_url": None,
        "role": "user",
    }

    stored = {"password_hash": None}

    def fake_insert(_query, params):
        stored["password_hash"] = params[1]
        return inserted_user

    def fake_query(_query, params):
        if params[0] == "user@example.com":
            return [{
                **inserted_user,
                "password_hash": stored["password_hash"],
            }]
        return []

    monkeypatch.setattr(auth_router.db, "execute_insert", fake_insert)
    monkeypatch.setattr(auth_router.db, "execute_query", fake_query)

    from fastapi.testclient import TestClient

    client = TestClient(fastapi_test_app)

    register_payload = {
        "email": "user@example.com",
        "password": "StrongPass123",
        "first_name": "Test",
        "last_name": "User",
        "phone": None,
        "location": None,
        "role": "user",
    }
    register_response = client.post("/api/auth/register", json=register_payload)
    assert register_response.status_code == 200
    token = register_response.json()["access_token"]
    assert token

    login_response = client.post("/api/auth/login", json={"email": "user@example.com", "password": "StrongPass123"})
    assert login_response.status_code == 200
    assert login_response.json()["token_type"] == "bearer"
