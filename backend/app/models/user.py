from pydantic import BaseModel, EmailStr
from typing import Optional


class UserRegister(BaseModel):
    email: EmailStr
    password: str
    first_name: str
    last_name: str
    phone: Optional[str] = None
    location: Optional[str] = None
    role: Optional[str] = "user"


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class UserResponse(BaseModel):
    id: int
    email: EmailStr
    first_name: str
    last_name: str
    phone: Optional[str]
    location: Optional[str]
    linkedin_url: Optional[str] = None
    role: Optional[str] = "user"


class TokenResponse(BaseModel):
    access_token: str
    token_type: str
    user: UserResponse
