from __future__ import annotations
import re
from typing import List, Set
from collections import Counter
from rapidfuzz import fuzz as rapidfuzz  # type: ignore


def tokenize(text: str) -> List[str]:
    """Split text into meaningful keyword tokens."""
    tokens = re.split(r"[，,。；;、\s\n/|]+", text)
    return [t.strip().lower() for t in tokens if len(t.strip()) >= 2]


def extract_keywords_simple(job_description: str) -> List[str]:
    """
    Fallback rule-based keyword extraction from job description.
    Extracts capitalized English terms, tech keywords, and longer phrases.
    """
    patterns = [
        r"[A-Z][a-zA-Z+#.]{2,}(?:\s?\+{2})?",
        r"[A-Za-z+#.]{3,}(?:\s?\+{2})?",
    ]
    keywords: Set[str] = set()
    for pat in patterns:
        for m in re.finditer(pat, job_description):
            kw = m.group(0).strip().lower()
            if len(kw) >= 3 and kw not in {
                "the", "and", "for", "are", "you", "can", "has", "our",
                "this", "that", "with", "from", "your", "will", "have",
                "been", "they", "them", "about", "which", "their",
            }:
                keywords.add(kw)
    tokens = tokenize(job_description)
    for t in tokens:
        if len(t) >= 3:
            keywords.add(t)
    return list(keywords)


def compute_skill_match(resume_skills: str, job_keywords: List[str]) -> float:
    """
    Compute a fuzzy skill match rate between resume skill text and job keywords.
    Returns a score between 0 and 1.
    """
    if not job_keywords:
        return 0.0
    resume_lower = resume_skills.lower()
    match_count = 0
    for kw in job_keywords:
        kw_lower = kw.lower().strip()
        if len(kw_lower) < 2:
            continue
        if kw_lower in resume_lower:
            match_count += 1
            continue
        for chunk in _chunkify(resume_lower, window=20):
            if rapidfuzz.partial_ratio(kw_lower, chunk) >= 85:
                match_count += 1
                break

    return round(match_count / len(job_keywords), 4)


def compute_experience_relevance(resume_projects: str, job_keywords: List[str]) -> float:
    """
    Estimate experience relevance by checking keyword overlap with project descriptions.
    Returns a score between 0 and 1.
    """
    if not job_keywords or not resume_projects.strip():
        return 0.0
    projects_lower = resume_projects.lower()
    match_count = 0
    for kw in job_keywords:
        kw_lower = kw.lower().strip()
        if len(kw_lower) < 2:
            continue
        if kw_lower in projects_lower:
            match_count += 1
            continue
        for chunk in _chunkify(projects_lower, window=20):
            if rapidfuzz.partial_ratio(kw_lower, chunk) >= 85:
                match_count += 1
                break
    return round(match_count / len(job_keywords), 4)


def compute_combined_score(skill_rate: float, exp_rel: float, ai_score: float | None = None) -> float:
    """
    Compute a weighted overall score.
    If AI score is available, weight: 40% skill + 30% experience + 30% AI.
    Otherwise: 60% skill + 40% experience.
    """
    if ai_score is not None and ai_score > 0:
        return round(skill_rate * 0.4 * 100 + exp_rel * 0.3 * 100 + ai_score * 0.3, 2)
    return round(skill_rate * 0.6 * 100 + exp_rel * 0.4 * 100, 2)


def _chunkify(text: str, window: int = 20) -> List[str]:
    words = text.split()
    if len(words) <= window:
        return [text]
    chunks = []
    for i in range(0, len(words) - window + 1, max(1, window // 2)):
        chunks.append(" ".join(words[i : i + window]))
    if len(words) % window != 0 and len(words) > window:
        chunks.append(" ".join(words[-window:]))
    return chunks
