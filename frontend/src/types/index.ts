export interface ParsedResumeInfo {
  name: string
  phone: string
  email: string
  address: string
  job_intent: string
  expected_salary: string
  work_years: string
  education: string
  projects: string
}

export interface ResumeResponse {
  id: string
  original_filename: string
  raw_text: string
  parsed_info: ParsedResumeInfo
  created_at: string
}

export interface ResumeListItem {
  id: string
  original_filename: string
  name: string
  phone: string
  email: string
  job_intent: string
  created_at: string
}

export interface ResumeListResponse {
  total: number
  page: number
  size: number
  items: ResumeListItem[]
}

export interface MatchRequest {
  title: string
  description: string
  resume_ids?: string[]
}

export interface MatchResultItem {
  resume_id: string
  resume_name: string
  score: number
  skill_match_rate: number
  experience_relevance: number
  ai_analysis: Record<string, string>
}

export interface MatchResponse {
  job_id: string
  job_title: string
  job_keywords: string[]
  results: MatchResultItem[]
}

export interface MatchDetailResponse {
  id: string
  resume_id: string
  job_id: string
  score: number
  skill_match_rate: number
  experience_relevance: number
  ai_analysis: Record<string, string>
  created_at: string
}
