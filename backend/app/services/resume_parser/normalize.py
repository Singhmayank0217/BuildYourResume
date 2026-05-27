import re
from typing import Dict, List
from .skill_extractor import extract_skills


SECTION_HEADERS = {
    "experience": ["experience", "work experience", "employment"],
    "education": ["education", "academic"],
    "skills": ["skills", "technical skills"],
    "projects": ["projects"],
    "certifications": ["certifications", "certificates"],
}


# --------------------------------------------------
# SECTION SPLITTER
# --------------------------------------------------

def split_sections(raw_text: str) -> Dict[str, str]:
    sections = {}
    text = raw_text

    pattern = r"\n(?=(experience|education|skills|projects|certifications)\b)"
    parts = re.split(pattern, text, flags=re.IGNORECASE)

    current_section = None
    buffer = ""

    for part in parts:
        key = part.lower().strip()

        if key in SECTION_HEADERS:
            if current_section:
                sections[current_section] = buffer.strip()
            current_section = key
            buffer = ""
        else:
            buffer += part

    if current_section:
        sections[current_section] = buffer.strip()

    return sections


# --------------------------------------------------
# EXPERIENCE PARSER
# --------------------------------------------------

def extract_experience(text: str) -> List[Dict]:
    experience_list = []

    entries = re.split(r"\n(?=[A-Z][a-z])", text)

    for entry in entries:
        years = re.findall(r"(20\d{2})", entry)

        start_year = int(years[0]) if years else None
        end_year = int(years[-1]) if len(years) > 1 else start_year

        if len(entry.strip()) > 50:
            experience_list.append({
                "raw": entry.strip(),
                "start_year": start_year,
                "end_year": end_year
            })

    return experience_list


# --------------------------------------------------
# EDUCATION PARSER
# --------------------------------------------------

def extract_education(text: str) -> List[Dict]:
    lines = [line.strip() for line in text.split("\n") if line.strip()]
    return [{"raw": line} for line in lines if len(line) > 5]


# --------------------------------------------------
# MAIN EXTRACTION
# --------------------------------------------------

def extract_resume_fields(raw_text: str) -> Dict:

    text_lower = raw_text.lower()

    detected_sections: List[str] = []

    for section, keywords in SECTION_HEADERS.items():
        for kw in keywords:
            if re.search(rf"\b{kw}\b", text_lower):
                detected_sections.append(section)
                break

    # ---------------------------
    # Basic Contact Info
    # ---------------------------

    email_match = re.search(
        r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+",
        raw_text,
    )

    phone_match = re.search(
        r"(\+?\d{1,3}[\s\-]?)?\d{10}",
        raw_text,
    )

    # Full name = first non-empty line
    first_lines = [line.strip() for line in raw_text.split("\n") if line.strip()]
    full_name = first_lines[0] if first_lines else ""

    # ---------------------------
    # Split sections
    # ---------------------------

    section_blocks = split_sections(raw_text)

    # ---------------------------
    # Structured Extraction
    # ---------------------------

    skills = extract_skills(raw_text)

    experience = extract_experience(
        section_blocks.get("experience", "")
    )

    education = extract_education(
        section_blocks.get("education", "")
    )

    projects = [
        line.strip()
        for line in section_blocks.get("projects", "").split("\n")
        if len(line.strip()) > 10
    ]

    certifications = [
        line.strip()
        for line in section_blocks.get("certifications", "").split("\n")
        if len(line.strip()) > 5
    ]

    # ---------------------------
    # RETURN CLEAN STRUCTURE
    # ---------------------------

    return {
        "full_name": full_name,
        "email": email_match.group(0) if email_match else None,
        "phone": phone_match.group(0).strip() if phone_match else None,
        "skills": skills,
        "experience": experience,
        "education": education,
        "projects": projects,
        "certifications": certifications,
        "raw_text": raw_text,
        "detected_sections": sorted(set(detected_sections)),
    }
