import re
import json
from datetime import datetime
from collections import defaultdict
from difflib import SequenceMatcher

CURRENT_YEAR = datetime.now().year


# ----------------------------
# Utility helpers
# ----------------------------
def normalize_text(text: str) -> str:
    if not text:
        return ""
    return re.sub(r"[^a-z0-9 ]", " ", text.lower())


def similarity(a: str, b: str) -> float:
    return SequenceMatcher(None, a, b).ratio()


# ----------------------------
# Skill & Concept Normalization
# ----------------------------
SKILL_SYNONYMS = {
    "machine learning": [
        "ml", "machine-learning", "statistical learning",
        "supervised learning", "unsupervised learning",
        "reinforcement learning", "predictive modeling"
    ],
    "deep learning": [
        "dl", "neural networks", "artificial neural networks",
        "cnn", "rnn", "lstm", "gru", "transformer",
        "pytorch", "tensorflow", "keras"
    ],
    "natural language processing": [
        "nlp", "text processing", "text analytics",
        "language modeling", "tokenization",
        "named entity recognition", "ner",
        "sentiment analysis", "text classification"
    ],
    "computer vision": [
        "cv", "image processing", "image classification",
        "object detection", "image segmentation",
        "opencv", "yolo", "resnet"
    ],
    "python": ["python3"],
    "sql": ["postgresql", "mysql", "sqlite"],
    "aws": ["amazon web services", "ec2", "s3", "lambda"],
    "docker": ["containerization"],
    "kubernetes": ["k8s"],
    "rest api": ["restful api", "fastapi", "flask"],
    "mlops": ["model deployment", "model monitoring"],
    "communication": ["written communication", "verbal communication"],
}


# ----------------------------
# MAIN ATS ENGINE
# ----------------------------
class ATSAnalyzer:

    async def optimize_with_ai(self, resume_text: str, job_description: str):
        resume = json.loads(resume_text)

        jd_text = normalize_text(job_description)
        resume_text_norm = normalize_text(resume_text)

        # ====================================================
        # A. KEYWORD & CONCEPT MATCH (35)
        # ====================================================
        matched_keywords = set()
        missing_keywords = set()

        for canonical, variants in SKILL_SYNONYMS.items():
            jd_requires = any(
                term in jd_text for term in [canonical] + variants
            )

            if not jd_requires:
                continue

            resume_has = any(
                term in resume_text_norm for term in [canonical] + variants
            )

            if resume_has:
                matched_keywords.add(canonical)
            else:
                missing_keywords.add(canonical)

        keyword_score = int(
            (len(matched_keywords) /
             max(len(matched_keywords) + len(missing_keywords), 1)) * 35
        )

        # ====================================================
        # B. SKILL DEPTH & RECENCY (25)
        # ====================================================
        skills = resume.get("skills", [])
        experience = resume.get("experience", [])

        skill_usage = defaultdict(int)
        skill_recency = defaultdict(int)

        for exp in experience:
            exp_text = normalize_text(json.dumps(exp))
            end_year = exp.get("end_year", CURRENT_YEAR)

            for skill in skills:
                if skill.lower() in exp_text:
                    skill_usage[skill] += 1
                    skill_recency[skill] = max(
                        skill_recency[skill], end_year
                    )

        skill_scores = []

        for skill in skills:
            usage = skill_usage.get(skill, 0)
            last_used = skill_recency.get(skill, 0)

            depth_score = min(1.0, usage / 3) if usage else 0.25
            recency_score = (
                1.0 if CURRENT_YEAR - last_used <= 2 else
                0.7 if CURRENT_YEAR - last_used <= 5 else
                0.4
            )

            skill_scores.append(depth_score * recency_score)

        skills_score = int(
            (sum(skill_scores) / max(len(skill_scores), 1)) * 25
        )

        # ====================================================
        # C. EXPERIENCE & ROLE ALIGNMENT (25)
        # ====================================================
        resume_titles = [
            normalize_text(exp.get("title", ""))
            for exp in experience
        ]

        jd_words = jd_text.split()

        title_similarity = max(
            (
                similarity(jd_word, title)
                for jd_word in jd_words
                for title in resume_titles
            ),
            default=0
        )

        years_experience = len(experience) * 1.5

        experience_score = min(
            25,
            int((title_similarity * 15) + min(years_experience, 10))
        )

        # ====================================================
        # D. FORMATTING & ATS PARSING (15)
        # ====================================================
        formatting_score = 0
        required_fields = ["full_name", "email", "skills", "experience"]

        for field in required_fields:
            if resume.get(field):
                formatting_score += 3

        formatting_score = min(formatting_score, 15)

        # ====================================================
        # FINAL SCORE
        # ====================================================
        ats_score = min(
            100,
            keyword_score + skills_score +
            experience_score + formatting_score
        )

        # ====================================================
        # OUTPUT
        # ====================================================
        return {
            "ats_score": ats_score,
            "breakdown": {
                "keyword_relevance": keyword_score,
                "skills_depth": skills_score,
                "experience_alignment": experience_score,
                "formatting": formatting_score
            },
            "matched_keywords": sorted(matched_keywords),
            "missing_keywords": sorted(list(missing_keywords))[:15],
            "suggestions": self._build_suggestions(
                missing_keywords,
                skills_score,
                formatting_score
            )
        }

    # ----------------------------
    # Suggestions Engine
    # ----------------------------
    def _build_suggestions(
        self,
        missing_keywords,
        skills_score,
        formatting_score
    ):
        suggestions = []

        if missing_keywords:
            suggestions.append(
                "Add job-relevant skills such as: "
                + ", ".join(list(missing_keywords)[:5])
            )

        if skills_score < 15:
            suggestions.append(
                "Show how your skills were used in experience bullets, "
                "not just listed in the skills section."
            )

        if formatting_score < 12:
            suggestions.append(
                "Use simple headings, avoid tables, icons, and multi-column layouts."
            )

        return suggestions


# ----------------------------
# INIT
# ----------------------------
ats_analyzer = ATSAnalyzer()
