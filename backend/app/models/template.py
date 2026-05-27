from pydantic import BaseModel
from typing import Dict


class TemplateResponse(BaseModel):
    id: int
    name: str
    description: str
    structure: Dict
    ats_safe: bool
    is_recommended: bool
