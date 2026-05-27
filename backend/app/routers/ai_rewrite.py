import json
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel

from app.database import db
from app.routers.auth import get_current_user

router = APIRouter(prefix="/api/ai", tags=["AI Rewrite"])


class RewriteRequest(BaseModel):
    resume_id: int
    rewritten_content: dict
    source: str = "ai_rewrite"


@router.post("/rewrite")
def rewrite_resume(payload: RewriteRequest, user_id: int = Depends(get_current_user)):
    owner = db.execute_query(
        "SELECT id, current_version_id FROM resumes WHERE id = %s AND user_id = %s",
        (payload.resume_id, user_id),
    )
    if not owner:
        raise HTTPException(status_code=404, detail="Resume not found")

    previous_version_id = owner[0].get("current_version_id")

    inserted = db.execute_insert(
        """
        INSERT INTO resume_versions (resume_id, content, source, previous_version_id, created_by)
        VALUES (%s, %s::json, %s, %s, %s)
        RETURNING id
        """,
        (
            payload.resume_id,
            json.dumps(payload.rewritten_content),
            payload.source,
            previous_version_id,
            user_id,
        ),
    )

    db.execute_update(
        "UPDATE resumes SET current_version_id = %s WHERE id = %s",
        (inserted["id"], payload.resume_id),
    )

    return {"status": "ok", "version_id": inserted["id"]}
