import io
from fastapi import UploadFile
from docx import Document


async def parse_docx(file: UploadFile) -> str:
    contents = await file.read()

    doc = Document(io.BytesIO(contents))

    text = "\n".join([para.text for para in doc.paragraphs])

    return text.strip()
