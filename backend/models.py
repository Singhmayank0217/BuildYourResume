from pydantic import BaseModel, EmailStr
from typing import Optional, List, Dict, Any
from datetime import datetime

# User Models
class UserRegister(BaseModel):
    email: EmailStr
    password: str
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    phone: Optional[str] = None
    location: Optional[str] = None

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class UserResponse(BaseModel):
    id: int
    email: str
    first_name: Optional[str]
    last_name: Optional[str]
    phone: Optional[str]
    location: Optional[str]
    linkedin_url: Optional[str]

class TokenResponse(BaseModel):
    access_token: str
    token_type: str
    user: UserResponse

# Resume Models
class ResumeCreate(BaseModel):
    title: str
    template_id: Optional[int] = None
    content: Dict[str, Any]

class ResumeUpdate(BaseModel):
    title: Optional[str] = None
    content: Optional[Dict[str, Any]] = None
    template_id: Optional[int] = None

class ResumeResponse(BaseModel):
    id: int
    user_id: int
    title: str
    content: Dict[str, Any]
    ats_score: Optional[float]
    created_at: datetime
    updated_at: datetime

# Job Description Models
class JobDescriptionCreate(BaseModel):
    title: str
    description: str

class JobDescriptionResponse(BaseModel):
    id: int
    title: str
    description: str
    keywords: Optional[List[str]]

# ATS Analysis Models
class ATSAnalysisRequest(BaseModel):
    resume_id: int
    job_description_id: Optional[int] = None
    job_description_text: Optional[str] = None

class ATSAnalysisResponse(BaseModel):
    ats_score: float
    missing_keywords: List[str]
    formatting_issues: List[str]
    suggestions: List[str]
    optimized_resume: Dict[str, Any]

# Template Models
class TemplateResponse(BaseModel):
    id: int
    name: str
    description: str
    structure: Dict[str, Any]
    ats_safe: bool
    is_recommended: bool

# Occupation Models
class OccupationResponse(BaseModel):
    id: int
    title: str
    summary_template: str
    common_skills: List[str]
    experience_bullets: List[str]
