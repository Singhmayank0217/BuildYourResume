import pytest

from app.services.resume_parser.docx_parser import parse_docx
from app.services.resume_parser.pdf_parser import parse_pdf
from app.services.resume_parser.structured_parser import build_structured_resume


@pytest.mark.unit
@pytest.mark.asyncio
async def test_docx_parser_extracts_text(sample_docx_upload):
    text = await parse_docx(sample_docx_upload)
    assert "Alex Johnson" in text
    assert "FastAPI" in text


@pytest.mark.unit
@pytest.mark.asyncio
async def test_pdf_parser_extracts_text(sample_pdf_upload):
    text = await parse_pdf(sample_pdf_upload)
    assert "Alex Johnson" in text


@pytest.mark.unit
def test_structured_parser_extracts_core_fields():
    raw = """Alex Johnson
alex@example.com
Skills
Python FastAPI Docker
Experience
Backend Engineer 2022 2024
Education
B.Sc Computer Science 2020
"""
    structured = build_structured_resume(raw)

    assert structured["full_name"] == "Alex Johnson"
    assert structured["email"] == "alex@example.com"
    assert "python" in structured["skills"]
