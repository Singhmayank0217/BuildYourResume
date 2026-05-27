import json
from typing import List, Dict
from app.database import db


class TemplateService:

    @staticmethod
    def list_recommended_templates() -> List[Dict]:
        query = """
            SELECT id, name, description, structure, ats_safe, is_recommended
            FROM templates
            WHERE is_recommended = TRUE
        """
        results = db.execute_query(query)
        for t in results:
            t["structure"] = json.loads(t["structure"])
        return results

    @staticmethod
    def audit_template(structure: Dict) -> bool:
        """
        Returns True if ATS-safe, False otherwise.
        Future AI will enhance this.
        """
        required_sections = {"summary", "experience", "education", "skills"}
        return required_sections.issubset(structure.keys())
