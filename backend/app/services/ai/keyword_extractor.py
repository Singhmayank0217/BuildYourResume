from app.services.ai.prompts import KEYWORD_EXTRACTION_PROMPT

class KeywordExtractor:

    @staticmethod
    def build_prompt(job_description: str) -> str:
        return KEYWORD_EXTRACTION_PROMPT.format(
            job_description=job_description
        )
