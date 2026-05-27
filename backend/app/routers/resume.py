from fastapi import APIRouter, Depends, HTTPException

from app.routers.auth import get_current_user
from app.services.resume_service import ResumeService
from app.services.ats_analyzer import ats_analyzer
from app.database import db

from app.models.resume_dto import (
    ResumeCreate,
    ResumeUpdate,
    ResumeResponse,
)

from app.models.analysis import (
    ResumeGenerateRequest,
    ResumeGenerateResponse,
)

import json

router = APIRouter()



# =====================
# CRUD RESUME ROUTES
# =====================

@router.post("/", response_model=ResumeResponse)
def create_resume(
    resume: ResumeCreate,
    user_id: int = Depends(get_current_user),
):
    return ResumeService.create_resume(
        user_id=user_id,
        title=resume.title,
        content=resume.content,
        template_id=resume.template_id,
    )


@router.get("/")
def list_resumes(user_id: int = Depends(get_current_user)):
    return ResumeService.list_resumes(user_id)


@router.get("/{resume_id}")
def get_resume(resume_id: int, user_id: int = Depends(get_current_user)):
    resume = ResumeService.get_resume(resume_id, user_id)
    if not resume:
        raise HTTPException(status_code=404, detail="Resume not found")
    return resume


@router.put("/{resume_id}")
def update_resume(
    resume_id: int,
    resume: ResumeUpdate,
    user_id: int = Depends(get_current_user),
):
    updated = ResumeService.update_resume(
        resume_id=resume_id,
        user_id=user_id,
        title=resume.title,
        content=resume.content,
        template_id=resume.template_id,
    )
    if not updated:
        raise HTTPException(
            status_code=404,
            detail="Resume not found or no changes",
        )
    return updated


@router.delete("/{resume_id}")
def delete_resume(resume_id: int, user_id: int = Depends(get_current_user)):
    ResumeService.delete_resume(resume_id, user_id)
    return {"status": "deleted"}


# =====================
# GENERATE RESUME (AI)
# =====================

@router.post("/generate", response_model=ResumeGenerateResponse)
async def generate_resume(
    payload: ResumeGenerateRequest,
    user_id: int = Depends(get_current_user),
):
    # Convert resume schema to text
    resume_text = json.dumps(payload.resume.dict(), indent=2)

    # AI optimization
    analysis = await ats_analyzer.optimize_with_ai(
        resume_text=resume_text,
        job_description=payload.job_description,
    )

    optimized_resume = analysis.get(
        "optimized_content",
        payload.resume.dict(),
    )

    # Save generated resume
    query = """
    INSERT INTO resumes (user_id, title, content, ats_score)
    VALUES (%s, %s, %s, %s)
    RETURNING id
"""
    db.execute_insert(
    query,
    (
        user_id,
        "Generated Resume",
        json.dumps(optimized_resume),
        analysis.get("ats_score", 0),
    ),
)


    return ResumeGenerateResponse(
        optimized_resume=optimized_resume,
        ats_score=analysis.get("ats_score", 0),
        keywords_added=analysis.get("missing_keywords", []),
        suggestions=analysis.get("suggestions", []),
    )
