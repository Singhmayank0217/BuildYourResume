from typing import Dict


class OccupationService:

    @staticmethod
    def generate_default_resume(occupation_title: str) -> Dict:
        """
        Stub logic – will be AI-driven later.
        """
        return {
            "title": f"{occupation_title} Resume",
            "summary": f"Professional {occupation_title} with relevant experience.",
            "skills": [],
            "experience": [],
            "education": [],
        }
