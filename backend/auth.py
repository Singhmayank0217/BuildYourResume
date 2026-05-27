from datetime import datetime, timedelta, timezone
from typing import Optional

import jwt
from passlib.context import CryptContext
from config import settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


# =========================
# Password utilities
# =========================

def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


# =========================
# JWT utilities
# =========================

def create_access_token(
    *,
    user_id: int,
    expires_delta: Optional[timedelta] = None,
) -> str:
    """
    Create JWT access token.
    `sub` MUST be a string (JWT spec).
    """

    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(
            minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
        )

    payload = {
        "sub": str(user_id),  # ✅ always string
        "exp": expire,
        "iat": datetime.now(timezone.utc),
        "type": "access",
    }

    token = jwt.encode(
        payload,
        settings.SECRET_KEY,
        algorithm=settings.ALGORITHM,
    )

    print("[DEBUG] JWT created:", payload)
    return token


def verify_token(token: str) -> Optional[int]:
    try:
        payload = jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=[settings.ALGORITHM],
        )

        print("[DEBUG] JWT decoded:", payload)

        sub = payload.get("sub")
        if not sub:
            print("[DEBUG] Missing sub claim")
            return None

        return int(sub)

    except jwt.ExpiredSignatureError:
        print("[DEBUG] Token expired")
        return None
    except jwt.InvalidTokenError as e:
        print("[DEBUG] Invalid token:", str(e))
        return None
