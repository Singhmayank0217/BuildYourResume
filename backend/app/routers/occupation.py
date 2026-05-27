from fastapi import APIRouter
from app.models.resume import ResumeContent, Header, ExperienceItem, EducationItem

router = APIRouter()



@router.get("/{occupation}/resume-template")
def generate_resume_template(occupation: str):
    occupation = occupation.lower()

    if occupation == "software engineer":
        return ResumeContent(
            header=Header(
                full_name="",
                email="",
                phone="",
                location="",
                linkedin=""
            ),
            summary="Results-driven Software Engineer with experience building scalable web applications and APIs.",
            experience=[
                ExperienceItem(
                    job_title="Software Engineer",
                    company="",
                    location="",
                    start_date="",
                    end_date="",
                    bullets=[
                        "Developed REST APIs using FastAPI and Python",
                        "Optimized database queries to improve performance",
                        "Collaborated with cross-functional teams to deliver features"
                    ]
                )
            ],
            education=[],
            skills=["Python", "FastAPI", "SQL", "REST APIs", "Git"]
        )

    return {
        "error": "Occupation not supported yet"
    }
