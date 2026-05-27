# app/services/ats_matcher.py

import re
import json
from collections import defaultdict
from difflib import SequenceMatcher
from datetime import datetime

CURRENT_YEAR = datetime.now().year


def normalize(text: str) -> str:
    return re.sub(r"[^a-z0-9 ]", " ", text.lower())


def similarity(a: str, b: str) -> float:
    return SequenceMatcher(None, a, b).ratio()

def extract_skills_from_text(text: str):
    skills_found = set()
    for canonical, variants in SKILL_SYNONYMS.items():
        if any(term in text for term in [canonical] + variants):
            skills_found.add(canonical)
    return list(skills_found)


def extract_experience_from_text(text: str):
    roles = []
    for line in text.split("\n"):
        if re.search(r"(engineer|developer|intern|analyst)", line):
            roles.append({"title": line})
    return roles



SKILL_SYNONYMS = {

    # -------------------------
    # PYTHON
    # -------------------------
    "python": [
        "python3", "cpython",
        "python programming",
        "scripting in python",
        "data processing in python"
    ],

    # -------------------------
    # REACT
    # -------------------------
    "react": [
        "reactjs", "react.js",
        "frontend react",
        "react frontend",
        "react components",
        "react hooks",
        "jsx"
    ],

    # -------------------------
    # MACHINE LEARNING
    # -------------------------
    "machine learning": [
        "ml", "machine-learning",
        "predictive modeling",
        "supervised learning",
        "unsupervised learning",
        "reinforcement learning",
        "classification",
        "regression",
        "model training"
    ],

    # -------------------------
    # DEEP LEARNING
    # -------------------------
    "deep learning": [
        "neural networks",
        "artificial neural networks",
        "deep neural networks",
        "cnn", "convolutional neural networks",
        "rnn", "recurrent neural networks",
        "lstm", "gru",
        "transformer models",
        "pytorch", "tensorflow", "keras"
    ],

    # -------------------------
    # SQL & DATABASES
    # -------------------------
    "sql": [
        "structured query language",
        "mysql", "postgresql", "sqlite",
        "sql server", "oracle sql",
        "database querying",
        "relational databases"
    ],

    # -------------------------
    # DOCKER
    # -------------------------
    "docker": [
        "containerization",
        "docker containers",
        "docker images",
        "docker compose"
    ],

    # -------------------------
    # AWS / CLOUD
    # -------------------------
    "aws": [
        "amazon web services",
        "aws cloud",
        "ec2", "s3", "rds", "lambda",
        "cloud infrastructure",
        "cloud deployment"
    ],
}


def analyze_resume_match(parsed_resume: dict, job_description: str) -> dict:
    resume_text = normalize(parsed_resume["raw_text"])
    jd_text = normalize(job_description)

    # ----------------------------
    # A. Keyword / Concept Match
    # ----------------------------
    matched = set()
    missing = set()

    for canonical, variants in SKILL_SYNONYMS.items():
        jd_requires = any(t in jd_text for t in [canonical] + variants)
        if not jd_requires:
            continue

        resume_has = any(t in resume_text for t in [canonical] + variants)
        if resume_has:
            matched.add(canonical)
        else:
            missing.add(canonical)

    keyword_score = int(
        (len(matched) / max(len(matched) + len(missing), 1)) * 35
    )

    # ----------------------------
    # B. Skill Depth & Recency
    # ----------------------------
    resume_text = normalize(parsed_resume["raw_text"])

    skills = parsed_resume.get("skills")
    if not skills:
        skills = extract_skills_from_text(resume_text)

    experience = parsed_resume.get("experience")
    if not experience:
        experience = extract_experience_from_text(resume_text)

    

    usage = defaultdict(int)
    recency = defaultdict(int)

    for exp in experience:
        exp_text = normalize(json.dumps(exp))
        end_year = exp.get("end_year", CURRENT_YEAR)

        for skill in skills:
            if skill.lower() in exp_text:
                usage[skill] += 1
                recency[skill] = max(recency[skill], end_year)

    skill_scores = []
    for skill in skills:
        u = usage.get(skill, 0)
        r = recency.get(skill, 0)

        depth = min(1.0, u / 3) if u else 0.25
        recent = (
            1.0 if CURRENT_YEAR - r <= 2 else
            0.7 if CURRENT_YEAR - r <= 5 else
            0.4
        )

        skill_scores.append(depth * recent)

    skills_score = int(
        (sum(skill_scores) / max(len(skill_scores), 1)) * 25
    )

    # ----------------------------
    # C. Experience Alignment
    # ----------------------------
    titles = [
        normalize(exp.get("title", "")) for exp in experience
    ]
    jd_words = jd_text.split()

    title_similarity = max(
        (similarity(jd, title) for jd in jd_words for title in titles),
        default=0
    )

    years_exp = len(experience) * 1.5

    experience_score = min(
        25,
        int((title_similarity * 15) + min(years_exp, 10))
    )

    # ----------------------------
    # D. Formatting Safety
    # ----------------------------
    formatting_score = 0
    for field in ["email", "phone", "skills", "experience"]:
        if parsed_resume.get(field):
            formatting_score += 3

    formatting_score = min(formatting_score, 15)

    ats_score = min(
        100,
        keyword_score +
        skills_score +
        experience_score +
        formatting_score
    )

    return {
        "ats_score": ats_score,
        "breakdown": {
            "keyword_relevance": keyword_score,
            "skills_depth": skills_score,
            "experience_alignment": experience_score,
            "formatting": formatting_score,
        },
        "matched_keywords": sorted(matched),
        "missing_keywords": sorted(list(missing))[:10],
        "suggestions": build_suggestions(missing, skills_score),
    }


def build_suggestions(missing, skills_score):
    suggestions = []

    if missing:
        suggestions.append(
            "Add job-relevant skills such as: " +
            ", ".join(list(missing)[:5])
        )

    if skills_score < 15:
        suggestions.append(
            "Show skill usage inside experience bullets, not only skills list."
        )

    return suggestions
