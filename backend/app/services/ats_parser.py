import re
from datetime import datetime

CURRENT_YEAR = datetime.now().year


class ATSParser:
    def parse(self, resume: dict):
        parsed = {}

        # ----------------------------
        # BASIC FIELDS
        # ----------------------------
        parsed["parsed_name"] = resume.get("full_name")
        parsed["parsed_email"] = resume.get("email")
        parsed["parsed_phone"] = resume.get("phone")

        # ----------------------------
        # SKILLS
        # ----------------------------
        skills = resume.get("skills", [])
        parsed["parsed_skills"] = list(
            {skill.lower() for skill in skills}
        )

        # ----------------------------
        # ROLES / TITLES
        # ----------------------------
        experience = resume.get("experience", [])
        parsed["parsed_roles"] = [
            exp.get("title").lower()
            for exp in experience
            if exp.get("title")
        ]

        # ----------------------------
        # EXPERIENCE YEARS
        # ----------------------------
        total_years = 0.0
        for exp in experience:
            start = exp.get("start_year")
            end = exp.get("end_year", CURRENT_YEAR)

            if start and isinstance(start, int):
                total_years += max(end - start, 0)

        parsed["estimated_experience_years"] = round(total_years, 1)

        # ----------------------------
        # SECTION DETECTION
        # ----------------------------
        sections = []
        for key in ["summary", "experience", "skills", "education"]:
            if resume.get(key):
                sections.append(key)

        parsed["sections_detected"] = sections

        return parsed


ats_parser = ATSParser()
