from __future__ import annotations
import json
from typing import Optional
from openai import AsyncOpenAI

from app.config import settings
from app.models.schemas import ParsedResumeInfo

SYSTEM_PROMPT = """你是一位专业的简历解析专家。你的任务是从简历文本中提取以下结构化的关键信息。
请严格按照要求的 JSON 格式输出，不要额外添加解释或 markdown 标记。

对于缺失的信息，将对应字段值设为空字符串 ""。

提取字段说明：
- name: 姓名
- phone: 联系电话
- email: 电子邮箱
- address: 地址（城市即可）
- job_intent: 求职意向（期望职位/方向）
- expected_salary: 期望薪资
- work_years: 工作年限
- education: 学历背景（最高学历+学校+专业）
- projects: 项目经历摘要（取最核心的1-3个项目，简述项目名、技术栈、个人职责，用分号分隔）
"""


class InfoExtractionError(Exception):
    pass


class InfoExtractor:
    def __init__(self):
        self.client = AsyncOpenAI(
            api_key=settings.deepseek_api_key,
            base_url=settings.deepseek_base_url,
        )

    async def extract(self, resume_text: str) -> ParsedResumeInfo:
        try:
            response = await self.client.chat.completions.create(
                model=settings.deepseek_model,
                messages=[
                    {"role": "system", "content": SYSTEM_PROMPT},
                    {"role": "user", "content": resume_text},
                ],
                temperature=0.1,
                max_tokens=2000,
                response_format={"type": "json_object"},
            )
            content = response.choices[0].message.content
            if not content:
                raise InfoExtractionError("Empty response from AI model")
            data = json.loads(content)
            return ParsedResumeInfo(**data)
        except json.JSONDecodeError as e:
            raise InfoExtractionError(f"Failed to parse AI response as JSON: {e}")
        except InfoExtractionError:
            raise
        except Exception as e:
            raise InfoExtractionError(f"AI extraction failed: {e}")

    async def extract_keywords(self, job_description: str) -> list[str]:
        """Extract keywords from a job description for matching purposes."""
        try:
            response = await self.client.chat.completions.create(
                model=settings.deepseek_model,
                messages=[
                    {
                        "role": "system",
                        "content": (
                            "你是一位专业的招聘需求分析专家。请从以下岗位描述中提取核心关键词（技能、技术栈、经验要求等），"
                            "以便用于简历匹配。以 JSON 数组形式输出关键词列表，例如：[\"Python\", \"Flask\", \"3年经验\"]"
                        ),
                    },
                    {"role": "user", "content": job_description},
                ],
                temperature=0.1,
                max_tokens=500,
                response_format={"type": "json_object"},
            )
            content = response.choices[0].message.content
            if not content:
                return []
            data = json.loads(content)
            if isinstance(data, list):
                return data
            if isinstance(data, dict):
                for v in data.values():
                    if isinstance(v, list):
                        return v
                return list(data.values())
            return []
        except Exception:
            return []

    async def score_with_ai(
        self, resume_text: str, job_description: str, extracted_info: ParsedResumeInfo
    ) -> dict:
        """Use AI to produce a detailed match analysis between a resume and a job description."""
        resume_summary = json.dumps(extracted_info.model_dump(), ensure_ascii=False, indent=2)
        prompt = f"""请根据以下简历信息和岗位需求进行匹配度分析。

岗位需求：
{job_description}

简历信息（已结构化提取）：
{resume_summary}

简历原文：
{resume_text[:3000]}

请从以下维度评估，并以 JSON 格式返回：
- overall_score: 综合匹配度评分 (0-100)
- skill_match_detail: 技能匹配分析（哪些技能匹配，哪些缺失）
- experience_analysis: 工作经验与岗位要求的相关性分析
- advantage: 候选人相对于该岗位的核心优势（简练，1-2句）
- weakness: 候选人相对于该岗位的不足或风险点（简练，1-2句）
- recommendation: 是否推荐进入下一轮面试及理由（简练，1-2句）
"""
        try:
            response = await self.client.chat.completions.create(
                model=settings.deepseek_model,
                messages=[
                    {"role": "system", "content": "你是一位资深的招聘顾问，擅长评估候选人与岗位的匹配度。"},
                    {"role": "user", "content": prompt},
                ],
                temperature=0.3,
                max_tokens=2000,
                response_format={"type": "json_object"},
            )
            content = response.choices[0].message.content
            if not content:
                return _default_ai_analysis()
            return json.loads(content)
        except Exception:
            return _default_ai_analysis()


def _default_ai_analysis() -> dict:
    return {
        "overall_score": 0,
        "skill_match_detail": "AI评估暂不可用",
        "experience_analysis": "AI评估暂不可用",
        "advantage": "",
        "weakness": "",
        "recommendation": "",
    }
