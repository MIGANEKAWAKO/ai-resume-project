from __future__ import annotations
from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, Field


# ── Resume schemas ───────────────────────────────────────────

class ParsedResumeInfo(BaseModel):
    name: str = ""
    phone: str = ""
    email: str = ""
    address: str = ""
    job_intent: str = Field(default="", description="求职意向")
    expected_salary: str = Field(default="", description="期望薪资")
    work_years: str = Field(default="", description="工作年限")
    education: str = Field(default="", description="学历背景")
    projects: str = Field(default="", description="项目经历")


class ResumeResponse(BaseModel):
    id: str
    original_filename: str
    raw_text: str
    parsed_info: ParsedResumeInfo
    created_at: datetime

    model_config = {"from_attributes": True}


class ResumeListItem(BaseModel):
    id: str
    original_filename: str
    name: str = ""
    phone: str = ""
    email: str = ""
    job_intent: str = ""
    created_at: datetime

    model_config = {"from_attributes": True}


class ResumeListResponse(BaseModel):
    total: int
    page: int
    size: int
    items: List[ResumeListItem]


# ── Job Description schemas ──────────────────────────────────

class JobDescriptionRequest(BaseModel):
    title: str = ""
    description: str = Field(..., min_length=1, description="岗位需求描述文本")


class JobDescriptionResponse(BaseModel):
    id: str
    title: str
    description: str
    keywords: List[str]
    created_at: datetime

    model_config = {"from_attributes": True}


# ── Match schemas ────────────────────────────────────────────

class MatchRequest(BaseModel):
    title: str = ""
    description: str = Field(..., min_length=1, description="岗位需求描述文本")
    resume_ids: Optional[List[str]] = Field(default=None, description="指定简历ID列表，不传则匹配全部")


class MatchResultItem(BaseModel):
    resume_id: str
    resume_name: str
    score: float
    skill_match_rate: float
    experience_relevance: float
    ai_analysis: dict = Field(default_factory=dict)


class MatchResponse(BaseModel):
    job_id: str
    job_title: str
    job_keywords: List[str]
    results: List[MatchResultItem]


class MatchDetailResponse(BaseModel):
    id: str
    resume_id: str
    job_id: str
    score: float
    skill_match_rate: float
    experience_relevance: float
    ai_analysis: dict
    created_at: datetime

    model_config = {"from_attributes": True}


# ── Common ───────────────────────────────────────────────────

class ErrorResponse(BaseModel):
    detail: str
