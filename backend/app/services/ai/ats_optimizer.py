from app.services.ai.prompts import RESUME_OPTIMIZATION_PROMPT, ATS_ANALYSIS_PROMPT

class ATSOptimizer:

    @staticmethod
    def build_optimization_prompt(resume_text: str, job_description: str) -> str:
        return RESUME_OPTIMIZATION_PROMPT.format(
            resume_text=resume_text,
            job_description=job_description
        )

    @staticmethod
    def build_analysis_prompt(resume_text: str, job_description: str) -> str:
        return ATS_ANALYSIS_PROMPT.format(
            resume_text=resume_text,
            job_description=job_description
        )
