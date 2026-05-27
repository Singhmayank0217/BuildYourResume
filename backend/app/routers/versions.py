import json

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel

from app.database import db
from app.routers.auth import get_current_user

router = APIRouter(prefix="/api/versions", tags=["Versions"])


class RollbackRequest(BaseModel):
    resume_id: int
    target_version_id: int


@router.get("/{resume_id}")
def list_versions(resume_id: int, user_id: int = Depends(get_current_user)):
    owner = db.execute_query("SELECT id FROM resumes WHERE id = %s AND user_id = %s", (resume_id, user_id))
    if not owner:
        raise HTTPException(status_code=404, detail="Resume not found")

    versions = db.execute_query(
        """
        SELECT id, resume_id, content, created_at, source, previous_version_id, created_by
        FROM resume_versions
        WHERE resume_id = %s
        ORDER BY id DESC
        """,
        (resume_id,),
    )
    return {"items": versions}


@router.post("/rollback")
def rollback_version(payload: RollbackRequest, user_id: int = Depends(get_current_user)):
    owner = db.execute_query("SELECT id FROM resumes WHERE id = %s AND user_id = %s", (payload.resume_id, user_id))
    if not owner:
        raise HTTPException(status_code=404, detail="Resume not found")

    target = db.execute_query(
        "SELECT id, content FROM resume_versions WHERE id = %s AND resume_id = %s",
        (payload.target_version_id, payload.resume_id),
    )
    if not target:
        raise HTTPException(status_code=404, detail="Target version not found")

    new_version = db.execute_insert(
        """
        INSERT INTO resume_versions (resume_id, content, source, previous_version_id, created_by)
        VALUES (%s, %s::json, %s, %s, %s)
        RETURNING id
        """,
        (
            payload.resume_id,
            json.dumps(target[0]["content"]),
            "rollback",
            payload.target_version_id,
            user_id,
        ),
    )

    db.execute_update(
        "UPDATE resumes SET current_version_id = %s WHERE id = %s",
        (new_version["id"], payload.resume_id),
    )

    return {"status": "rolled_back", "new_version_id": new_version["id"]}
