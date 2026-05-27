from typing import Dict, List
from app.services.scoring.ats_rules import (
    REQUIRED_SECTIONS,
    FORMATTING_RULES,
    KEYWORD_WEIGHT,
    JD_RELEVANCE_WEIGHT,
)


class ATSScorer:

    @staticmethod
    def score_sections(resume: Dict) -> int:
        score = 0
        for section, points in REQUIRED_SECTIONS.items():
            if section in resume and resume[section]:
                score += points
        return score

    @staticmethod
    def score_keywords(resume_text: str, keywords: List[str]) -> int:
        if not keywords:
            return 0

        matched = sum(
            1 for kw in keywords if kw.lower() in resume_text.lower()
        )
        coverage = matched / len(keywords)

        return int(coverage * KEYWORD_WEIGHT)

    @staticmethod
    def score_formatting() -> int:
        # Placeholder – we assume ATS-safe formatting
        return sum(FORMATTING_RULES.values())

    @staticmethod
    def score_jd_relevance(keywords_score: int) -> int:
        # Relevance proportional to keyword coverage
        return int((keywords_score / KEYWORD_WEIGHT) * JD_RELEVANCE_WEIGHT)

    @classmethod
    def calculate(
        cls,
        resume: Dict,
        resume_text: str,
        keywords: List[str],
    ) -> Dict:
        section_score = cls.score_sections(resume)
        keyword_score = cls.score_keywords(resume_text, keywords)
        formatting_score = cls.score_formatting()
        relevance_score = cls.score_jd_relevance(keyword_score)

        total = (
            section_score
            + keyword_score
            + formatting_score
            + relevance_score
        )

        return {
            "total_score": min(total, 100),
            "breakdown": {
                "sections": section_score,
                "keywords": keyword_score,
                "formatting": formatting_score,
                "relevance": relevance_score,
            },
        }
