from __future__ import annotations
import hashlib
from typing import Dict, List, Optional, Tuple
from app.models.schemas import ParsedResumeInfo, MatchResultItem
from app.services.keyword_engine import (
    compute_skill_match,
    compute_experience_relevance,
    compute_combined_score,
)
from app.services.info_extractor import InfoExtractor

_cache: Dict[str, dict] = {}


def _cache_key(resume_text: str, job_desc: str) -> str:
    raw = f"{resume_text[:500]}|||{job_desc[:500]}"
    return hashlib.sha256(raw.encode()).hexdigest()


async def score_single(
    resume_id: str,
    resume_name: str,
    resume_text: str,
    extracted_info: ParsedResumeInfo,
    job_description: str,
    job_keywords: List[str],
    extractor: InfoExtractor,
    use_ai: bool = True,
) -> MatchResultItem:
    """Score a single resume against a job description."""
    cache_key = _cache_key(resume_text, job_description)
    if cache_key in _cache:
        cached = _cache[cache_key]
        return MatchResultItem(
            resume_id=resume_id,
            resume_name=resume_name,
            score=cached["score"],
            skill_match_rate=cached["skill_match_rate"],
            experience_relevance=cached["experience_relevance"],
            ai_analysis=cached["ai_analysis"],
        )

    resume_skills = (
        f"{extracted_info.job_intent} {extracted_info.education} {extracted_info.projects}"
    )
    skill_rate = compute_skill_match(resume_skills, job_keywords)
    exp_rel = compute_experience_relevance(extracted_info.projects, job_keywords)

    ai_analysis: dict = {}
    if use_ai:
        ai_analysis = await extractor.score_with_ai(resume_text, job_description, extracted_info)

    ai_score = ai_analysis.get("overall_score", None)
    combined = compute_combined_score(skill_rate, exp_rel, ai_score)

    result = MatchResultItem(
        resume_id=resume_id,
        resume_name=resume_name,
        score=combined,
        skill_match_rate=skill_rate,
        experience_relevance=exp_rel,
        ai_analysis=ai_analysis,
    )

    _cache[cache_key] = {
        "score": combined,
        "skill_match_rate": skill_rate,
        "experience_relevance": exp_rel,
        "ai_analysis": ai_analysis,
    }
    return result


async def score_batch(
    resumes: List[Tuple[str, str, str, ParsedResumeInfo]],
    job_description: str,
    job_keywords: List[str],
    extractor: InfoExtractor,
    use_ai: bool = True,
) -> List[MatchResultItem]:
    """Score multiple resumes and return results sorted by score descending."""
    results: List[MatchResultItem] = []
    for resume_id, resume_name, resume_text, extracted_info in resumes:
        item = await score_single(
            resume_id, resume_name, resume_text, extracted_info,
            job_description, job_keywords, extractor, use_ai,
        )
        results.append(item)
    results.sort(key=lambda r: r.score, reverse=True)
    return results
