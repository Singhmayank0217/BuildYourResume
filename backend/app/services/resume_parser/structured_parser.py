import re
from datetime import datetime

CURRENT_YEAR = datetime.now().year


# ---------------------------------------------------
# HELPERS
# ---------------------------------------------------

def clean_text(text: str) -> str:
    return re.sub(r"\s+", " ", text).strip()


def extract_years(text: str):
    years = re.findall(r"(20\d{2})", text)
    if len(years) >= 2:
        return int(years[0]), int(years[1])
    elif len(years) == 1:
        return int(years[0]), CURRENT_YEAR
    return None, None


# ---------------------------------------------------
# SECTION SPLITTER
# ---------------------------------------------------

def split_sections(raw_text: str):
    sections = {}
    current_section = "other"
    sections[current_section] = []

    for line in raw_text.split("\n"):
        line_clean = line.strip().lower()

        if "experience" in line_clean:
            current_section = "experience"
            sections[current_section] = []
            continue
        elif "education" in line_clean:
            current_section = "education"
            sections[current_section] = []
            continue
        elif "project" in line_clean:
            current_section = "projects"
            sections[current_section] = []
            continue
        elif "skill" in line_clean:
            current_section = "skills"
            sections[current_section] = []
            continue
        elif "certification" in line_clean:
            current_section = "certifications"
            sections[current_section] = []
            continue

        sections.setdefault(current_section, []).append(line)

    return sections


# ---------------------------------------------------
# SKILL EXTRACTION
# ---------------------------------------------------

COMMON_SKILLS = [
    "python", "java", "javascript", "react", "fastapi",
    "node", "sql", "postgresql", "mysql", "mongodb",
    "docker", "aws", "git", "machine learning",
    "deep learning", "pytorch", "tensorflow"
]


def extract_skills(text: str):
    found = []
    text_lower = text.lower()

    for skill in COMMON_SKILLS:
        if skill in text_lower:
            found.append(skill)

    return sorted(list(set(found)))


# ---------------------------------------------------
# EXPERIENCE PARSER
# ---------------------------------------------------

def extract_experience(section_lines):
    experiences = []
    buffer = []

    for line in section_lines:
        if re.search(r"(20\d{2})", line):
            if buffer:
                experiences.append(" ".join(buffer))
                buffer = []
        buffer.append(line)

    if buffer:
        experiences.append(" ".join(buffer))

    structured = []

    for block in experiences:
        start_year, end_year = extract_years(block)

        structured.append({
            "raw": clean_text(block),
            "start_year": start_year,
            "end_year": end_year,
        })

    return structured


# ---------------------------------------------------
# EDUCATION PARSER
# ---------------------------------------------------

def extract_education(section_lines):
    education = []
    buffer = []

    for line in section_lines:
        if re.search(r"(20\d{2})", line):
            if buffer:
                education.append(" ".join(buffer))
                buffer = []
        buffer.append(line)

    if buffer:
        education.append(" ".join(buffer))

    return [{"raw": clean_text(e)} for e in education]


# ---------------------------------------------------
# MAIN STRUCTURED PARSER
# ---------------------------------------------------

def build_structured_resume(raw_text: str):

    sections = split_sections(raw_text)

    structured = {
        "full_name": raw_text.split("\n")[0].strip(),
        "email": re.findall(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}", raw_text),
        "phone": re.findall(r"\+?\d[\d\s]{8,15}", raw_text),
        "skills": extract_skills(raw_text),
        "experience": extract_experience(sections.get("experience", [])),
        "education": extract_education(sections.get("education", [])),
        "projects": sections.get("projects", []),
        "certifications": sections.get("certifications", []),
        "raw_text": raw_text,
    }

    structured["email"] = structured["email"][0] if structured["email"] else None
    structured["phone"] = structured["phone"][0] if structured["phone"] else None

    return structured
