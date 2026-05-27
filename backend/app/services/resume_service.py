import json
from typing import List, Dict, Optional
from app.database import db


class ResumeService:

    @staticmethod
    def create_resume(user_id: int, title: str, content: Dict, template_id: Optional[int] = None):
        query = """
            INSERT INTO resumes (user_id, title, content, template_id)
            VALUES (%s, %s, %s, %s)
            RETURNING id, user_id, title, content, ats_score, created_at, updated_at
        """
        result = db.execute_insert(
            query,
            (user_id, title, json.dumps(content), template_id),
        )
        result["content"] = json.loads(result["content"])
        return result

    @staticmethod
    def list_resumes(user_id: int) -> List[Dict]:
        query = """
            SELECT id, title, ats_score, created_at, updated_at
            FROM resumes
            WHERE user_id = %s
            ORDER BY created_at DESC
        """
        return db.execute_query(query, (user_id,))

    @staticmethod
    def get_resume(resume_id: int, user_id: int) -> Dict:
        query = """
            SELECT id, user_id, title, content, ats_score, created_at, updated_at
            FROM resumes
            WHERE id = %s AND user_id = %s
        """
        result = db.execute_query(query, (resume_id, user_id))
        if not result:
            return None
        resume = result[0]
        resume["content"] = json.loads(resume["content"])
        return resume

    @staticmethod
    def update_resume(
        resume_id: int,
        user_id: int,
        title: Optional[str] = None,
        content: Optional[Dict] = None,
        template_id: Optional[int] = None,
    ):
        updates = []
        params = []

        if title:
            updates.append("title = %s")
            params.append(title)

        if content:
            updates.append("content = %s")
            params.append(json.dumps(content))

        if template_id:
            updates.append("template_id = %s")
            params.append(template_id)

        if not updates:
            return None

        params.extend([resume_id, user_id])

        query = f"""
            UPDATE resumes
            SET {', '.join(updates)}, updated_at = CURRENT_TIMESTAMP
            WHERE id = %s AND user_id = %s
            RETURNING id, user_id, title, content, ats_score, created_at, updated_at
        """

        result = db.execute_query(query, params)
        if not result:
            return None

        resume = result[0]
        resume["content"] = json.loads(resume["content"])
        return resume

    @staticmethod
    def delete_resume(resume_id: int, user_id: int):
        query = "DELETE FROM resumes WHERE id = %s AND user_id = %s"
        db.execute_update(query, (resume_id, user_id))
