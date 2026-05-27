from pydantic import BaseModel
from typing import Optional
from app.models.resume import ResumeContent


class ResumeCreate(BaseModel):
    title: str
    template_id: Optional[int] = None
    content: ResumeContent


class ResumeUpdate(BaseModel):
    title: Optional[str] = None
    template_id: Optional[int] = None
    content: Optional[ResumeContent] = None


class ResumeResponse(BaseModel):
    id: int
    title: str
    content: ResumeContent
    ats_score: Optional[int] = None
    created_at: Optional[str] = None
    updated_at: Optional[str] = None
