import re
from collections import defaultdict

# --------------------------------------------------
# MASTER SKILL DICTIONARY
# --------------------------------------------------

SKILL_MAP = {
    # Core Languages
    "python": ["python3"],
    "java": [],
    "javascript": ["js"],
    "c++": ["cpp", "c plus plus"],

    # Backend
    "fastapi": [],
    "flask": [],
    "django": [],
    "node": ["nodejs", "node.js"],
    "express": ["expressjs", "express.js"],
    "rest api": ["restful api", "api development"],

    # Frontend
    "react": ["reactjs", "react.js"],
    "nextjs": ["next.js"],
    "html": ["html5"],
    "css": ["css3"],
    "tailwind": ["tailwind css"],
    "bootstrap": [],
    "framer motion": [],

    # Databases
    "sql": ["postgresql", "mysql", "sqlite"],
    "mongodb": [],
    "postgresql": [],
    "mysql": [],

    # DevOps
    "git": [],
    "github": [],
    "docker": [],
    "kubernetes": ["k8s"],
    "jenkins": [],
    "ci/cd": ["continuous integration", "continuous deployment"],
    "vercel": [],
    "netlify": [],

    # AI / ML
    "machine learning": ["ml"],
    "deep learning": ["dl"],
    "llm": ["large language models", "llms"],
    "pytorch": [],
    "tensorflow": [],
    "numpy": [],
    "pandas": [],

    # Tools
    "postman": [],
    "powerbi": [],
    "selenium": [],
}

# --------------------------------------------------
# TEXT NORMALIZATION
# --------------------------------------------------

def normalize(text: str) -> str:
    text = text.lower()
    text = re.sub(r"[^a-z0-9\s]", " ", text)
    return re.sub(r"\s+", " ", text)


# --------------------------------------------------
# SKILL EXTRACTION ENGINE
# --------------------------------------------------

def extract_skills(raw_text: str) -> list:
    text = normalize(raw_text)

    detected_skills = set()
    skill_frequency = defaultdict(int)

    for canonical, variants in SKILL_MAP.items():
        terms = [canonical] + variants

        for term in terms:
            term_norm = normalize(term)

            # Exact word boundary match
            pattern = rf"\b{re.escape(term_norm)}\b"

            matches = re.findall(pattern, text)

            if matches:
                detected_skills.add(canonical)
                skill_frequency[canonical] += len(matches)

    # Optional: filter out low-frequency noise
    final_skills = [
        skill for skill in detected_skills
        if skill_frequency[skill] >= 1
    ]

    return sorted(final_skills)
