import io
import pdfplumber
from fastapi import UploadFile


async def parse_pdf(file: UploadFile) -> str:
    contents = await file.read()

    text = ""

    with pdfplumber.open(io.BytesIO(contents)) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"

    return text.strip()
