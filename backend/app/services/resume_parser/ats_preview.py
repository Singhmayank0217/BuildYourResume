from typing import Dict


def build_ats_preview(parsed: Dict) -> Dict:

    warnings = []
    detected_sections = []
    missing_sections = []

    # ----------------------------------
    # SECTION CHECK (STRUCTURED)
    # ----------------------------------

    section_map = {
        "skills": parsed.get("skills"),
        "experience": parsed.get("experience"),
        "education": parsed.get("education"),
    }

    for section, value in section_map.items():
        if value and len(value) > 0:
            detected_sections.append(section)
        else:
            missing_sections.append(section)
            warnings.append(f"Missing {section} section")

    # ----------------------------------
    # EMAIL & PHONE CHECK
    # ----------------------------------

    contact_score = 0
    if parsed.get("email"):
        contact_score += 0.1
    else:
        warnings.append("Email not detected.")

    if parsed.get("phone"):
        contact_score += 0.1
    else:
        warnings.append("Phone number not detected.")

    # ----------------------------------
    # EXPERIENCE QUALITY
    # ----------------------------------

    experience_quality = 0
    experience = parsed.get("experience", [])

    if experience:
        for exp in experience:
            if exp.get("start_year") and exp.get("end_year"):
                experience_quality = 0.2
                break
    else:
        warnings.append("Experience section lacks structured dates.")

    # ----------------------------------
    # FINAL CONFIDENCE
    # ----------------------------------

    section_score = len(detected_sections) / 3  # skills, exp, edu

    confidence = (
        contact_score +
        (section_score * 0.5) +
        experience_quality
    )

    confidence = round(min(confidence, 1.0), 2)

    return {
        "detected_sections": detected_sections,
        "missing_sections": missing_sections,
        "warnings": warnings,
        "parser_confidence": confidence,
    }
