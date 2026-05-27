import re
from difflib import SequenceMatcher
from collections import defaultdict
from datetime import datetime

CURRENT_YEAR = datetime.now().year


# ============================================================
# TEXT NORMALIZATION
# ============================================================

def normalize(text: str) -> str:
    if not text:
        return ""
    return re.sub(r"[^a-z0-9 ]", " ", text.lower())


# ============================================================
# SKILL MAP
# ============================================================

SKILL_SYNONYMS = {
    "python": ["python3"],
    "fastapi": ["rest api", "api development"],
    "sql": ["postgresql", "mysql"],
    "aws": ["amazon web services", "ec2", "s3"],
    "docker": ["containerization"],
    "machine learning": ["ml", "llm", "large language models"],
    "git": [],
}


def build_resume_analysis_text(resume: dict) -> str:
    """
    Builds normalized text for ATS scoring using structured fields.
    This avoids relying only on raw_text.
    """

    parts = []

    # Raw text (if exists and valid)
    raw = resume.get("raw_text")
    if raw and len(raw) > 50:
        parts.append(raw)

    # Skills
    parts.extend(resume.get("skills", []))

    # Experience
    for exp in resume.get("experience", []):
        parts.append(exp.get("raw", ""))

    # Projects
    parts.extend(resume.get("projects", []))

    # Education
    for edu in resume.get("education", []):
        parts.append(edu.get("raw", ""))

    combined = " ".join(parts)

    return normalize(combined)



def classify_jd_skills(jd_text, skill_map):

    required = set()
    preferred = set()

    strong_indicators = [
        "must",
        "required",
        "strong experience",
        "proficient",
        "should have",
        "essential"
    ]

    soft_indicators = [
        "preferred",
        "nice to have",
        "plus",
        "advantageous",
        "exposure to"
    ]

    for canonical, variants in skill_map.items():

        for term in [canonical] + variants:

            if term in jd_text:

                index = jd_text.find(term)
                context = jd_text[max(0, index - 80): index + 80]

                if any(word in context for word in strong_indicators):
                    required.add(canonical)

                elif any(word in context for word in soft_indicators):
                    preferred.add(canonical)

                else:
                    required.add(canonical)

    return required, preferred


# ============================================================
# REQUIRED / PREFERRED DETECTION
# ============================================================

def extract_required_and_preferred(jd_text: str):

    required = set()
    preferred = set()

    jd_lower = normalize(jd_text)

    for skill, variants in SKILL_SYNONYMS.items():

        if any(term in jd_lower for term in [skill] + variants):

            # Detect preferred language
            if re.search(rf"{skill}.*(plus|advantage|nice to have)", jd_lower):
                preferred.add(skill)
            elif re.search(r"(required|must|looking for|we are hiring)", jd_lower):
                required.add(skill)
            else:
                required.add(skill)

    return required, preferred


# ============================================================
# SKILL DEPTH SCORING
# ============================================================

def score_skill_depth(resume: dict, skills: set):

    raw = normalize(resume.get("raw_text", ""))
    experience = resume.get("experience", [])

    total_score = 0

    for skill in skills:

        frequency = raw.count(skill)
        freq_weight = min(frequency * 0.1, 0.5)

        exp_weight = 0
        recency_weight = 0

        for exp in experience:
            exp_text = normalize(exp.get("raw", ""))

            if skill in exp_text:
                exp_weight += 0.3

                end_year = exp.get("end_year") or CURRENT_YEAR
                years_ago = CURRENT_YEAR - end_year

                if years_ago <= 2:
                    recency_weight += 0.2
                elif years_ago <= 5:
                    recency_weight += 0.1

        total_skill = min(freq_weight + exp_weight + recency_weight, 1)
        total_score += total_skill

    if not skills:
        return 0

    return min(total_score / len(skills), 1)


# ============================================================
# EXPERIENCE ALIGNMENT
# ============================================================

def score_experience_alignment(resume: dict, jd_text: str):

    jd_words = set(normalize(jd_text).split())
    resume_text = build_resume_analysis_text(resume)

    overlap = len(jd_words.intersection(set(resume_text.split())))

    similarity_score = min(overlap / 40, 1)

    return similarity_score


# ============================================================
# KNOCKOUT RULES
# ============================================================

def apply_knockout_rules(resume: dict, required_skills: set):

    resume_text = build_resume_analysis_text(resume)


    missing_required = [
        skill for skill in required_skills
        if skill not in resume_text
    ]

    if missing_required:
        return True, missing_required

    if not resume.get("experience"):
        return True, ["experience"]

    return False, []


# ============================================================
# MAIN MATCH FUNCTION
# ============================================================

def analyze_resume_match(resume: dict, job_description: str):

    jd_text = normalize(job_description)
    resume_text = build_resume_analysis_text(resume)


    required_skills, preferred_skills = classify_jd_skills(
    jd_text,
    SKILL_SYNONYMS
    )


    matched_required = [
        s for s in required_skills if s in resume_text
    ]

    missing_required = [
        s for s in required_skills if s not in resume_text
    ]

    matched_preferred = [
        s for s in preferred_skills if s in resume_text
    ]

    missing_preferred = [
        s for s in preferred_skills if s not in resume_text
    ]

    # ============================================================
    # REQUIRED SCORE (40)
    # ============================================================

    required_score = int(
       (len(matched_required) /
       max(len(required_skills), 1)) * 50
    )


    # ============================================================
    # PREFERRED SCORE (10)
    # ============================================================

    preferred_score = int(
        (len(matched_preferred) /
        max(len(preferred_skills), 1)) * 15
    ) if preferred_skills else 0


    # ============================================================
    # SKILL DEPTH (20)
    # ============================================================

    skill_depth_ratio = score_skill_depth(resume, set(matched_required))
    skills_score = int(skill_depth_ratio * 20)

    # ============================================================
    # EXPERIENCE ALIGNMENT (20)
    # ============================================================

    exp_ratio = score_experience_alignment(resume, job_description)
    experience_score = int(exp_ratio * 20)

    # ============================================================
    # FORMATTING (10)
    # ============================================================

    formatting_score = 0

    if resume.get("full_name"):
        formatting_score += 2
    if resume.get("email"):
        formatting_score += 2
    if resume.get("skills"):
        formatting_score += 2
    if resume.get("experience"):
        formatting_score += 2
    if resume.get("education"):
        formatting_score += 2

    # ============================================================
    # KNOCKOUT CHECK
    # ============================================================

    knockout, knockout_reasons = apply_knockout_rules(
        resume,
        required_skills
    )

    total_score = (
        required_score +
        preferred_score +
        skills_score +
        experience_score +
        formatting_score
    )

    if knockout:
        total_score = min(total_score, 60)

    total_score = min(total_score, 100)

    # ============================================================
    # SUGGESTIONS
    # ============================================================

    suggestions = []

    if missing_required:
        suggestions.append(
            "Critical required skills missing: "
            + ", ".join(missing_required)
        )

    if missing_preferred:
        suggestions.append(
            "Optional skills that could improve ranking: "
            + ", ".join(missing_preferred)
        )

    if skills_score < 10:
        suggestions.append(
            "Demonstrate skill usage inside experience bullets."
        )

    if experience_score < 10:
        suggestions.append(
            "Align job titles and project descriptions with the target role."
        )

    return {
        "ats_score": total_score,
        "breakdown": {
            "required_skills": required_score,
            "preferred_skills": preferred_score,
            "skills_depth": skills_score,
            "experience_alignment": experience_score,
            "formatting": formatting_score,
        },
        "matched_required": matched_required,
        "missing_required": missing_required,
        "matched_preferred": matched_preferred,
        "missing_preferred": missing_preferred,
        "knockout_triggered": knockout,
        "suggestions": suggestions,
    }
