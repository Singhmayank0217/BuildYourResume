from fastapi import APIRouter, Depends, HTTPException
from app.models.job_description import (
    JobDescriptionCreate,
    JobDescriptionResponse,
)
from app.routers.auth import get_current_user
from app.services.jd_service import JobDescriptionService

router = APIRouter()


@router.post("/", response_model=JobDescriptionResponse)
def create_job_description(
    job: JobDescriptionCreate,
    user_id: int = Depends(get_current_user),
):
    # Keyword extraction will be AI-driven later
    keywords = []

    return JobDescriptionService.create_job_description(
        user_id=user_id,
        title=job.title,
        description=job.description,
        keywords=keywords,
    )
