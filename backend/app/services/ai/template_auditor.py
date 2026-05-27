class TemplateAuditor:

    @staticmethod
    def audit(structure: dict) -> dict:
        required = ["summary", "experience", "education", "skills"]

        missing = [s for s in required if s not in structure]

        return {
            "is_ats_safe": len(missing) == 0,
            "missing_sections": missing,
            "recommendation": "approved" if not missing else "detail_only"
        }
