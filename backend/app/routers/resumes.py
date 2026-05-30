from __future__ import annotations
import uuid
from pathlib import Path
from fastapi import APIRouter, UploadFile, File, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, desc

from app.core.database import get_db
from app.core.exceptions import (
    ResumeParseError,
    FileTooLargeError,
    InvalidFileTypeError,
    ResumeNotFoundError,
    AIExtractionError,
)
from app.config import settings
from app.models.database import Resume
from app.models.schemas import (
    ResumeResponse,
    ResumeListResponse,
    ResumeListItem,
    ParsedResumeInfo,
)
from app.services.pdf_parser import extract_text_from_pdf, PDFParseError
from app.services.info_extractor import InfoExtractor, InfoExtractionError

router = APIRouter(prefix="/api/v1/resumes", tags=["resumes"])
extractor = InfoExtractor()


def _validate_pdf(filename: str, size: int) -> None:
    if not filename.lower().endswith(".pdf"):
        raise InvalidFileTypeError()
    max_bytes = settings.max_upload_size_mb * 1024 * 1024
    if size > max_bytes:
        raise FileTooLargeError(max_mb=settings.max_upload_size_mb)


def _map_to_list_item(r: Resume) -> ResumeListItem:
    info = r.parsed_info or {}
    return ResumeListItem(
        id=r.id,
        original_filename=r.original_filename,
        name=info.get("name", ""),
        phone=info.get("phone", ""),
        email=info.get("email", ""),
        job_intent=info.get("job_intent", ""),
        created_at=r.created_at,
    )


@router.post("", response_model=ResumeResponse, status_code=201)
async def upload_resume(
    file: UploadFile = File(...),
    db: AsyncSession = Depends(get_db),
):
    """Upload a PDF resume, parse it, and extract structured information."""
    if not file.filename:
        raise InvalidFileTypeError()
    content = await file.read()
    _validate_pdf(file.filename, len(content))

    safe_name = f"{uuid.uuid4().hex}_{file.filename}"
    upload_path = Path(settings.upload_dir) / safe_name
    upload_path.parent.mkdir(parents=True, exist_ok=True)
    upload_path.write_bytes(content)

    try:
        raw_text = extract_text_from_pdf(upload_path)
    except PDFParseError as e:
        upload_path.unlink(missing_ok=True)
        raise ResumeParseError(detail=str(e))

    try:
        parsed_info = await extractor.extract(raw_text)
    except InfoExtractionError as e:
        upload_path.unlink(missing_ok=True)
        raise AIExtractionError(detail=str(e))

    resume = Resume(
        original_filename=file.filename,
        raw_text=raw_text,
        parsed_info=parsed_info.model_dump(),
    )
    db.add(resume)
    await db.commit()
    await db.refresh(resume)

    return ResumeResponse(
        id=resume.id,
        original_filename=resume.original_filename,
        raw_text=resume.raw_text,
        parsed_info=parsed_info,
        created_at=resume.created_at,
    )


@router.get("", response_model=ResumeListResponse)
async def list_resumes(
    page: int = Query(default=1, ge=1),
    size: int = Query(default=20, ge=1, le=100),
    db: AsyncSession = Depends(get_db),
):
    """Get a paginated list of all parsed resumes."""
    count_q = select(func.count(Resume.id))
    total = (await db.execute(count_q)).scalar() or 0

    offset = (page - 1) * size
    q = select(Resume).order_by(desc(Resume.created_at)).offset(offset).limit(size)
    rows = (await db.execute(q)).scalars().all()

    return ResumeListResponse(
        total=total,
        page=page,
        size=size,
        items=[_map_to_list_item(r) for r in rows],
    )


@router.get("/{resume_id}", response_model=ResumeResponse)
async def get_resume(resume_id: str, db: AsyncSession = Depends(get_db)):
    """Get a single resume with full parsed details."""
    q = select(Resume).where(Resume.id == resume_id)
    row = (await db.execute(q)).scalar_one_or_none()
    if not row:
        raise ResumeNotFoundError()
    return ResumeResponse(
        id=row.id,
        original_filename=row.original_filename,
        raw_text=row.raw_text,
        parsed_info=ParsedResumeInfo(**row.parsed_info),
        created_at=row.created_at,
    )


@router.delete("/{resume_id}", status_code=204)
async def delete_resume(resume_id: str, db: AsyncSession = Depends(get_db)):
    """Delete a resume record."""
    q = select(Resume).where(Resume.id == resume_id)
    row = (await db.execute(q)).scalar_one_or_none()
    if not row:
        raise ResumeNotFoundError()
    await db.delete(row)
    await db.commit()
