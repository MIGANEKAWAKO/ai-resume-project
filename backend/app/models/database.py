import uuid
from datetime import datetime, timezone
from sqlalchemy import Column, String, Float, Text, JSON, DateTime, ForeignKey
from sqlalchemy.dialects.sqlite import TEXT as SQLiteText
from app.core.database import Base


def _uuid() -> str:
    return uuid.uuid4().hex[:16]


def _utcnow() -> datetime:
    return datetime.now(timezone.utc)


class Resume(Base):
    __tablename__ = "resumes"

    id = Column(String(16), primary_key=True, default=_uuid)
    original_filename = Column(String(255), nullable=False)
    raw_text = Column(Text, nullable=False, default="")
    parsed_info = Column(JSON, nullable=False, default=dict)
    created_at = Column(DateTime(timezone=True), default=_utcnow)


class JobDescription(Base):
    __tablename__ = "job_descriptions"

    id = Column(String(16), primary_key=True, default=_uuid)
    title = Column(String(255), nullable=False, default="")
    description = Column(Text, nullable=False, default="")
    keywords = Column(JSON, nullable=False, default=list)
    created_at = Column(DateTime(timezone=True), default=_utcnow)


class MatchResult(Base):
    __tablename__ = "match_results"

    id = Column(String(16), primary_key=True, default=_uuid)
    resume_id = Column(String(16), ForeignKey("resumes.id", ondelete="CASCADE"), nullable=False)
    job_id = Column(String(16), ForeignKey("job_descriptions.id", ondelete="CASCADE"), nullable=False)
    score = Column(Float, nullable=False, default=0.0)
    skill_match_rate = Column(Float, nullable=False, default=0.0)
    experience_relevance = Column(Float, nullable=False, default=0.0)
    ai_analysis = Column(JSON, nullable=False, default=dict)
    created_at = Column(DateTime(timezone=True), default=_utcnow)
