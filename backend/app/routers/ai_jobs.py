from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel

from app.database import db
from app.routers.auth import get_current_user

router = APIRouter(prefix="/api/ai/jobs", tags=["AI Jobs"])


class CreateJobRequest(BaseModel):
    job_type: str
    resume_version_id: int | None = None
    provider: str = "local"
    prompt: str | None = None
    idempotency_key: str | None = None


@router.post("")
def create_job(payload: CreateJobRequest, _: int = Depends(get_current_user)):
    job = db.execute_insert(
        """
        INSERT INTO ai_jobs (job_type, resume_version_id, status, provider, prompt, idempotency_key, attempts, max_retries)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        RETURNING id, job_type, status
        """,
        (
            payload.job_type,
            payload.resume_version_id,
            "queued",
            payload.provider,
            payload.prompt,
            payload.idempotency_key,
            0,
            3,
        ),
    )
    return job


@router.get("/{job_id}")
def get_job(job_id: int, _: int = Depends(get_current_user)):
    rows = db.execute_query("SELECT * FROM ai_jobs WHERE id = %s", (job_id,))
    if not rows:
        raise HTTPException(status_code=404, detail="Job not found")
    return rows[0]
