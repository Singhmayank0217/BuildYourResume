from fastapi import APIRouter, UploadFile, File, Depends, HTTPException
from app.services.resume_parser import parse_resume
from app.routers.auth import get_current_user

router = APIRouter()


@router.post("/upload")
async def upload_resume(
    file: UploadFile = File(...),
    user_id: int = Depends(get_current_user)
):
    if not file.filename.lower().endswith((".pdf", ".docx")):
        raise HTTPException(
            status_code=400,
            detail="Only PDF or DOCX files are allowed"
        )

    # ✅ Parse resume (includes ATS preview internally)
    parsed = await parse_resume(file)

    # ❌ DO NOT rebuild ATS preview here
    # ❌ DO NOT recompute confidence here
    # ❌ DO NOT touch detected_sections here

    return {
        "parsed_resume": parsed,
        "message": "Resume parsed successfully",
    }
