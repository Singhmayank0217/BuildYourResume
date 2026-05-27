from typing import Any, Dict, List

from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter(prefix="/api/ai", tags=["AI Verify"])

REQUIRED_SECTIONS = {"summary", "skills", "experience", "education"}
BANNED_PHRASES = {
    "as an ai language model",
    "i cannot browse the internet",
    "i do not have access",
}


class VerifyPayload(BaseModel):
    resume: Dict[str, Any]


@router.post("/verify")
def verify_resume(payload: VerifyPayload):
    resume = payload.resume

    missing_sections = sorted([s for s in REQUIRED_SECTIONS if not resume.get(s)])

    raw_text = str(resume).lower()
    hallucination_flags: List[str] = [
        phrase for phrase in BANNED_PHRASES if phrase in raw_text
    ]

    safe = not missing_sections and not hallucination_flags

    return {
        "is_safe": safe,
        "missing_sections": missing_sections,
        "hallucination_flags": hallucination_flags,
    }
