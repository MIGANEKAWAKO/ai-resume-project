from __future__ import annotations
import re
from typing import List


def clean_text(text: str) -> str:
    """Remove redundant whitespace and non-printable characters while preserving paragraph structure."""
    text = re.sub(r"[\x00-\x08\x0b\x0c\x0e-\x1f\x7f-\x9f]", "", text)
    text = re.sub(r"[ \t]{2,}", " ", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    text = text.strip()
    return text


def merge_broken_lines(text: str) -> str:
    """Merge single newlines into spaces so each paragraph stays on one logical line."""
    lines = text.split("\n")
    out: List[str] = []
    buf: List[str] = []
    for line in lines:
        stripped = line.strip()
        if stripped == "":
            if buf:
                out.append(" ".join(buf))
                buf.clear()
            out.append("")
        else:
            buf.append(stripped)
    if buf:
        out.append(" ".join(buf))
    return "\n".join(out)


def split_paragraphs(text: str) -> List[str]:
    """Split cleaned text into non-empty paragraphs."""
    return [p.strip() for p in text.split("\n\n") if p.strip()]
