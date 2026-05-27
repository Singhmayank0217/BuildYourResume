import pytest

from app.services.scoring.ats_scorer import ATSScorer


@pytest.mark.unit
def test_ats_scorer_calculate_scores_resume(sample_resume_payload):
    resume_text = "Python FastAPI Docker SQL"
    keywords = ["python", "fastapi", "sql"]

    result = ATSScorer.calculate(sample_resume_payload, resume_text, keywords)

    assert "total_score" in result
    assert 0 <= result["total_score"] <= 100
    assert result["breakdown"]["keywords"] > 0
