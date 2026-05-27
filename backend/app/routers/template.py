from fastapi import APIRouter
from app.services.template_service import TemplateService
from app.models.template import TemplateResponse
from typing import List

router = APIRouter()


@router.get("/", response_model=List[TemplateResponse])
def list_templates():
    return TemplateService.list_recommended_templates()
