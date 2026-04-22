from pathlib import Path

from app.services.text_extractor import extract_uploaded_pdf_text


def extract_text(file_path: Path) -> str:
    """
    Extract cleaned text from an uploaded PDF file.

    This utility wrapper keeps the public import simple for API handlers.
    """
    return extract_uploaded_pdf_text(file_path)
