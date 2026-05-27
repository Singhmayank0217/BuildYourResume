import pytest

from app.routers.ai_verify import verify_resume, VerifyPayload
from app.services.ai.template_auditor import TemplateAuditor


@pytest.mark.unit
def test_template_auditor_marks_missing_sections():
    result = TemplateAuditor.audit({"summary": "ok", "skills": []})
    assert not result["is_ats_safe"]
    assert "experience" in result["missing_sections"]


@pytest.mark.unit
def test_hallucination_prevention_flags_banned_phrase(sample_resume_payload):
    sample_resume_payload["summary"] = "As an AI language model, I cannot browse the internet"
    result = verify_resume(VerifyPayload(resume=sample_resume_payload))
    assert result["is_safe"] is False
    assert result["hallucination_flags"]
