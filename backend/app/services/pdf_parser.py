from __future__ import annotations
from pathlib import Path
from typing import List
import pdfplumber

from app.utils.text_cleaner import clean_text, merge_broken_lines


class PDFParseError(Exception):
    pass


def extract_text_from_pdf(file_path: str | Path) -> str:
    """Extract text from a PDF file. Compatible with multi-page resumes."""
    try:
        pages: List[str] = []
        with pdfplumber.open(file_path) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    pages.append(page_text)
        if not pages:
            raise PDFParseError("No extractable text found in PDF")
        raw = "\n".join(pages)
        raw = clean_text(raw)
        raw = merge_broken_lines(raw)
        return raw
    except PDFParseError:
        raise
    except Exception as e:
        raise PDFParseError(f"Failed to parse PDF: {e}")
