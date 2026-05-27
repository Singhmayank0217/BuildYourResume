from app.services.ai.prompts import RESUME_GENERATION_PROMPT

class ResumeGenerator:

    @staticmethod
    def build_prompt(user_data: dict, job_description: str) -> str:
        return RESUME_GENERATION_PROMPT.format(
            user_data=user_data,
            job_description=job_description
        )
