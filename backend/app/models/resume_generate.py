from pydantic import BaseModel
from typing import Dict


class ResumeGenerateRequest(BaseModel):
    user_data: Dict
    job_description: str


class ResumeGenerateResponse(BaseModel):
    resume_id: int
    resume: Dict
    ats_score: int
    score_breakdown: Dict
