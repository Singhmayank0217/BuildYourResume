from fastapi import UploadFile
from .pdf_parser import parse_pdf
from .docx_parser import parse_docx
from .structured_parser import build_structured_resume
from .ats_preview import build_ats_preview


async def parse_resume(file: UploadFile):
    filename = file.filename.lower()

    if filename.endswith(".pdf"):
        raw_text = await parse_pdf(file)
    elif filename.endswith(".docx"):
        raw_text = await parse_docx(file)
    else:
        raise ValueError("Unsupported file type")

    structured = build_structured_resume(raw_text)
    ats_preview = build_ats_preview(structured)

    return {
        **structured,
        "ats_preview": ats_preview
    }
