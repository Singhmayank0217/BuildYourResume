import pytest

from app.services.ats_engine.matcher import analyze_resume_match, normalize


@pytest.mark.unit
def test_normalize_handles_none_and_symbols():
    assert normalize(None) == ""
    assert normalize("Python/FastAPI!") == "python fastapi "


@pytest.mark.unit
def test_analyze_resume_match_returns_expected_shape(sample_resume_payload):
    jd = "Must have Python and FastAPI experience. Docker is preferred."

    result = analyze_resume_match(sample_resume_payload, jd)

    assert "ats_score" in result
    assert 0 <= result["ats_score"] <= 100
    assert isinstance(result["breakdown"], dict)
    assert "required_skills" in result["breakdown"]
    assert "suggestions" in result
