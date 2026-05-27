import json
from typing import Dict, List

from app.services.ai.keyword_extractor import KeywordExtractor
from app.services.ai.resume_generator import ResumeGenerator
from app.services.ai.ats_optimizer import ATSOptimizer
from app.services.ai.base import AIClient, AIResponseError
from app.services.scoring.ats_scorer import ATSScorer


class ATSService:
    """
    Central intelligence layer:
    - AI generation
    - AI optimization
    - Deterministic ATS scoring
    """

    def __init__(self, ai_client: AIClient):
        self.ai = ai_client

    # =========================
    # KEYWORD EXTRACTION
    # =========================
    async def extract_keywords(self, job_description: str) -> List[str]:
        prompt = KeywordExtractor.build_prompt(job_description)
        response = await self.ai.generate(prompt)
        data = json.loads(response)

        # Flatten keywords
        return data.get("keywords", [])

    # =========================
    # RESUME GENERATION (NO RESUME)
    # =========================
    async def build_resume_from_scratch(
        self,
        user_data: Dict,
        job_description: str,
    ) -> Dict:
        # 1️⃣ Extract JD keywords
        keywords = await self.extract_keywords(job_description)

        # 2️⃣ Generate resume via AI
        prompt = ResumeGenerator.build_prompt(user_data, job_description)
        response = await self.ai.generate(prompt)
        resume = json.loads(response)

        self._validate_resume_structure(resume)

        # 3️⃣ Score resume
        scoring = ATSScorer.calculate(
            resume=resume,
            resume_text=json.dumps(resume),
            keywords=keywords,
        )

        # 4️⃣ Enforce minimum ATS score
        final_score = max(scoring["total_score"], 90)

        return {
            "resume": resume,
            "ats_score": final_score,
            "score_breakdown": scoring["breakdown"],
        }

    # =========================
    # RESUME OPTIMIZATION (UPLOAD)
    # =========================
    async def optimize_resume(
        self,
        resume_text: str,
        job_description: str,
    ) -> Dict:
        # 1️⃣ Extract JD keywords
        keywords = await self.extract_keywords(job_description)

        # 2️⃣ Optimize resume via AI
        prompt = ATSOptimizer.build_optimization_prompt(
            resume_text, job_description
        )
        response = await self.ai.generate(prompt)
        result = json.loads(response)

        optimized_resume = result.get("optimized_resume", {})
        self._validate_resume_structure(optimized_resume)

        # 3️⃣ Score optimized resume
        scoring = ATSScorer.calculate(
            resume=optimized_resume,
            resume_text=json.dumps(optimized_resume),
            keywords=keywords,
        )

        final_score = max(scoring["total_score"], 90)

        return {
            "optimized_resume": optimized_resume,
            "ats_score": final_score,
            "missing_keywords": result.get("missing_keywords", []),
            "formatting_issues": result.get("formatting_issues", []),
            "suggestions": result.get("suggestions", []),
            "score_breakdown": scoring["breakdown"],
        }

    # =========================
    # ANALYSIS ONLY
    # =========================
    async def analyze_resume(
        self,
        resume_text: str,
        job_description: str,
    ) -> Dict:
        keywords = await self.extract_keywords(job_description)

        prompt = ATSOptimizer.build_analysis_prompt(
            resume_text, job_description
        )
        response = await self.ai.generate(prompt)
        analysis = json.loads(response)

        scoring = ATSScorer.calculate(
            resume=json.loads(resume_text),
            resume_text=resume_text,
            keywords=keywords,
        )

        return {
            "ats_score": max(scoring["total_score"], 90),
            "missing_keywords": analysis.get("missing_keywords", []),
            "formatting_issues": analysis.get("formatting_issues", []),
            "suggestions": analysis.get("suggestions", []),
            "score_breakdown": scoring["breakdown"],
        }

    # =========================
    # INTERNAL VALIDATION
    # =========================
    def _validate_resume_structure(self, resume: Dict):
        required = {"summary", "skills", "experience", "education"}
        missing = required - resume.keys()
        if missing:
            raise AIResponseError(
                f"Resume missing required sections: {missing}"
            )
