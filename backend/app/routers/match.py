from __future__ import annotations
from fastapi import APIRouter, Depends, Query
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.core.exceptions import ResumeNotFoundError
from app.models.database import Resume, JobDescription, MatchResult
from app.models.schemas import (
    MatchRequest,
    MatchResponse,
    MatchResultItem,
    MatchDetailResponse,
    ParsedResumeInfo,
)
from app.services.info_extractor import InfoExtractor
from app.services.keyword_engine import extract_keywords_simple
from app.services.scorer import score_batch

router = APIRouter(prefix="/api/v1/match", tags=["match"])
extractor = InfoExtractor()


async def _get_keywords(job_description: str) -> list[str]:
    ai_kw = await extractor.extract_keywords(job_description)
    if ai_kw:
        return ai_kw
    return extract_keywords_simple(job_description)


@router.post("", response_model=MatchResponse)
async def match_resumes(req: MatchRequest, db: AsyncSession = Depends(get_db)):
    """Submit a job description and get ranked match results against resumes."""
    job_keywords = await _get_keywords(req.description)

    job = JobDescription(
        title=req.title or "未命名岗位",
        description=req.description,
        keywords=job_keywords,
    )
    db.add(job)

    if req.resume_ids:
        q = select(Resume).where(Resume.id.in_(req.resume_ids))
    else:
        q = select(Resume).order_by(Resume.created_at.desc())
    resumes = (await db.execute(q)).scalars().all()

    batch = [
        (r.id, r.original_filename, r.raw_text, ParsedResumeInfo(**(r.parsed_info or {})))
        for r in resumes
    ]

    results = await score_batch(
        batch, req.description, job_keywords, extractor, use_ai=True,
    )

    for item in results:
        mr = MatchResult(
            resume_id=item.resume_id,
            job_id=job.id,
            score=item.score,
            skill_match_rate=item.skill_match_rate,
            experience_relevance=item.experience_relevance,
            ai_analysis=item.ai_analysis,
        )
        db.add(mr)
    await db.commit()

    return MatchResponse(
        job_id=job.id,
        job_title=job.title,
        job_keywords=job_keywords,
        results=results,
    )


@router.get("/{match_id}", response_model=MatchDetailResponse)
async def get_match_detail(match_id: str, db: AsyncSession = Depends(get_db)):
    """Get a single match result detail."""
    q = select(MatchResult).where(MatchResult.id == match_id)
    row = (await db.execute(q)).scalar_one_or_none()
    if not row:
        raise ResumeNotFoundError()
    return MatchDetailResponse(
        id=row.id,
        resume_id=row.resume_id,
        job_id=row.job_id,
        score=row.score,
        skill_match_rate=row.skill_match_rate,
        experience_relevance=row.experience_relevance,
        ai_analysis=row.ai_analysis,
        created_at=row.created_at,
    )
