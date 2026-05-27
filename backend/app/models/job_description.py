from pydantic import BaseModel
from typing import List


class JobDescriptionCreate(BaseModel):
    title: str
    description: str


class JobDescriptionResponse(BaseModel):
    id: int
    title: str
    description: str
    keywords: List[str]
