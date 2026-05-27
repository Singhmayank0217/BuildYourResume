from pydantic import BaseModel
from typing import List


class Header(BaseModel):
    full_name: str
    email: str
    phone: str | None = None
    location: str | None = None
    linkedin: str | None = None


class ExperienceItem(BaseModel):
    job_title: str
    company: str
    location: str | None = None
    start_date: str
    end_date: str
    bullets: List[str]


class EducationItem(BaseModel):
    degree: str
    institution: str
    location: str | None = None
    start_year: str
    end_year: str


class ResumeContent(BaseModel):
    header: Header
    summary: str
    experience: List[ExperienceItem]
    education: List[EducationItem]
    skills: List[str]
