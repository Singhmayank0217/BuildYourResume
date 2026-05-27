from datetime import timedelta

import pytest

from app.services.auth_service import create_access_token as create_auth_token
from app.services.auth_service import hash_password, verify_password
from app.services.jwt_service import get_token_claims, verify_token


@pytest.mark.unit
def test_password_hash_roundtrip():
    hashed = hash_password("StrongPass123")
    assert hashed != "StrongPass123"
    assert verify_password("StrongPass123", hashed)


@pytest.mark.unit
def test_jwt_issue_and_verify():
    token = create_auth_token(user_id=7, expires_delta=timedelta(minutes=5), role="admin")

    assert verify_token(token) == 7
    claims = get_token_claims(token)
    assert claims is not None
    assert claims["role"] == "admin"
