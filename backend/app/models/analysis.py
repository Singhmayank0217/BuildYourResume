from pydantic import BaseModel
from typing import List, Optional
from app.models.resume import ResumeContent


# =========================
# GENERATE RESUME (BUILDER)
# =========================

class ResumeGenerateRequest(BaseModel):
    resume: ResumeContent
    job_description: str


class ResumeGenerateResponse(BaseModel):
    optimized_resume: ResumeContent
    ats_score: int
    keywords_added: List[str]
    suggestions: List[str]


# =========================
# ANALYZE RESUME (ANALYZER)
# =========================

class ATSAnalysisRequest(BaseModel):
    resume_id: Optional[int] = None
    resume: Optional[ResumeContent] = None
    job_description: Optional[str] = None


class ATSAnalysisResponse(BaseModel):
    ats_score: int
    missing_keywords: List[str]
    formatting_issues: List[str]
    suggestions: List[str]
    optimized_resume: Optional[ResumeContent] = None
