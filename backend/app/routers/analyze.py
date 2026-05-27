from fastapi import APIRouter, Depends, HTTPException
import json

from app.models.analysis import ATSAnalysisRequest, ATSAnalysisResponse
from app.routers.auth import get_current_user
from app.database import db

# 🔹 AI integration
from app.services.ats_service import ATSService
from app.services.ai.mock_client import MockAIClient

router = APIRouter()

# 🔹 Create ONE AI client and ONE ATS service instance
ai_client = MockAIClient()
ats_service = ATSService(ai_client)


@router.post("/", response_model=ATSAnalysisResponse)
async def analyze_resume(
    request: ATSAnalysisRequest,
    user_id: int = Depends(get_current_user),
):
    # 1️⃣ Fetch resume from DB
    query = """
        SELECT content
        FROM resumes
        WHERE id = %s AND user_id = %s
    """
    result = db.execute_query(query, (request.resume_id, user_id))

    if not result:
        raise HTTPException(status_code=404, detail="Resume not found")

    resume_text = json.dumps(result[0]["content"])

    # 2️⃣ Get job description
    job_description = request.job_description_text or ""

    # 3️⃣ Call ATS service (AI gateway)
    analysis = await ats_service.analyze_resume(
        resume_text=resume_text,
        job_description=job_description,
    )

    # 4️⃣ Return normalized response
    return ATSAnalysisResponse(
        ats_score=analysis.get("ats_score", 0),
        missing_keywords=analysis.get("missing_keywords", []),
        formatting_issues=analysis.get("formatting_issues", []),
        suggestions=analysis.get("suggestions", []),
        optimized_resume=analysis.get("optimized_resume", {}),
    )

from app.services.ats_parser import ats_parser
from app.database import db
import json
from fastapi import Depends, HTTPException
from app.routers.auth import get_current_user


@router.get("/parser-preview/{resume_id}")
def ats_parser_preview(
    resume_id: int,
    user_id: int = Depends(get_current_user)
):
    query = """
        SELECT content
        FROM resumes
        WHERE id = %s AND user_id = %s
    """
    result = db.execute_query(query, (resume_id, user_id))

    if not result:
        raise HTTPException(status_code=404, detail="Resume not found")

    resume = json.loads(result[0]["content"])
    parsed = ats_parser.parse(resume)

    return parsed


from fastapi import APIRouter
from app.services.ats_analyzer import ats_analyzer
import json

router = APIRouter()

@router.post("/preview")
async def preview_ats(payload: dict):
    """
    Preview ATS score without saving.
    Used for live improvement & before/after.
    """
    resume = payload.get("resume")
    job_description = payload.get("job_description", "")

    if not resume:
        return {"error": "Resume data missing"}

    analysis = await ats_analyzer.optimize_with_ai(
        resume_text=json.dumps(resume),
        job_description=job_description
    )

    return analysis

from fastapi import APIRouter, Depends
from app.routers.auth import get_current_user
from app.services.ats_engine.matcher import analyze_resume_match


router = APIRouter()

@router.post("/analyze")
def analyze_resume(payload: dict, user_id: int = Depends(get_current_user)):
    parsed_resume = payload.get("parsed_resume")
    job_description_text = payload.get("job_description")

    result = analyze_resume_match(parsed_resume, job_description_text)
    return result

