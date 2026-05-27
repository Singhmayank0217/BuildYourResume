import json
from app.services.ai.base import AIClient


class MockAIClient(AIClient):
    """
    Temporary AI client.
    Will be replaced by OpenAI / Claude later.
    """

    async def generate(self, prompt: str) -> str:
        # Deterministic safe output for now
        return json.dumps({
            "summary": "ATS-optimized professional summary.",
            "skills": [],
            "experience": [],
            "education": [],
            "certifications": [],
            "ats_score": 90,
            "missing_keywords": [],
            "formatting_issues": [],
            "suggestions": [],
            "optimized_resume": {}
        })
