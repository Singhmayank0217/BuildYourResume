from fastapi import APIRouter, Depends, HTTPException, Header
from datetime import timedelta
from typing import Optional

from app.config import settings
from app.database import db
from app.models.user import (
    UserRegister,
    UserLogin,
    UserResponse,
    TokenResponse,
)

from app.services.auth_service import (
    hash_password,
    verify_password,
    create_access_token,
    verify_token,
)

router = APIRouter()

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from app.services.jwt_service import verify_token, get_token_claims

security = HTTPBearer()

def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security)
) -> int:
    token = credentials.credentials.replace("Bearer ", "")
    print("TOKEN RECEIVED:", token)

    user_id = verify_token(token)
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
        )

    return user_id


def get_current_user_claims(credentials: HTTPAuthorizationCredentials = Depends(security)):
    token = credentials.credentials.replace("Bearer ", "")
    claims = get_token_claims(token)
    if not claims:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid or expired token")
    return claims


# =========================
# REGISTER
# =========================
@router.post("/register", response_model=TokenResponse)
def register(user: UserRegister):
    try:
        hashed_password = hash_password(user.password)

        query = """
            INSERT INTO users (email, password_hash, first_name, last_name, phone, location, role)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            RETURNING id, email, first_name, last_name, phone, location, linkedin_url, role
        """
        result = db.execute_insert(
            query,
            (
                user.email,
                hashed_password,
                user.first_name,
                user.last_name,
                user.phone,
                user.location,
                user.role or "user",
            ),
        )

        if not result:
            raise HTTPException(status_code=400, detail="Registration failed")

        access_token = create_access_token(
            user_id=result["id"],
            expires_delta=timedelta(days=7),
            role=result.get("role", "user"),
        )

        return {
            "access_token": access_token,
            "token_type": "bearer",
            "user": UserResponse(**result),
        }

    # except Exception as e:
    #     raise HTTPException(status_code=400, detail=str(e))

    except Exception as e:
        print("REGISTER ERROR:", e)
        raise



# =========================
# LOGIN
# =========================
@router.post("/login", response_model=TokenResponse)
def login(user: UserLogin):
    query = "SELECT id, email, password_hash, first_name, last_name, phone, location, linkedin_url, COALESCE(role, 'user') AS role FROM users WHERE email = %s"
    result = db.execute_query(query, (user.email,))

    if not result:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    user_data = result[0]

    if not verify_password(user.password, user_data["password_hash"]):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    access_token = create_access_token(
        user_id=user_data["id"],
        expires_delta=timedelta(days=7),
        role=user_data.get("role", "user"),
    )

    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user": UserResponse(**user_data),
    }


# =========================
# CURRENT USER PROFILE
# =========================
@router.get("/me", response_model=UserResponse)
def get_profile(user_id: int = Depends(get_current_user)):
    query = """
        SELECT id, email, first_name, last_name, phone, location, linkedin_url
        FROM users
        WHERE id = %s
    """
    result = db.execute_query(query, (user_id,))

    if not result:
        raise HTTPException(status_code=404, detail="User not found")

    return UserResponse(**result[0])

