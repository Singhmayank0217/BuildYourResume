import json
from typing import Dict
from app.database import db


class JobDescriptionService:

    @staticmethod
    def create_job_description(user_id: int, title: str, description: str, keywords: list):
        query = """
            INSERT INTO job_descriptions (user_id, title, description, keywords)
            VALUES (%s, %s, %s, %s)
            RETURNING id, title, description, keywords
        """
        result = db.execute_insert(
            query,
            (user_id, title, description, json.dumps(keywords)),
        )
        result["keywords"] = json.loads(result["keywords"])
        return result
