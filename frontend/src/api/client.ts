import type {
  ResumeResponse,
  ResumeListResponse,
  MatchRequest,
  MatchResponse,
} from "@/types"

const API = import.meta.env.VITE_API_BASE_URL || "http://localhost:8000/api/v1"

async function request<T>(url: string, options?: RequestInit): Promise<T> {
  const res = await fetch(`${API}${url}`, {
    headers: { "Content-Type": "application/json" },
    ...options,
  })
  if (!res.ok) {
    const body = await res.json().catch(() => ({}))
    throw new Error(body.detail || `请求失败 (${res.status})`)
  }
  if (res.status === 204) return undefined as T
  return res.json()
}

export const api = {
  uploadResume(file: File): Promise<ResumeResponse> {
    const form = new FormData()
    form.append("file", file)
    return request<ResumeResponse>("/resumes", {
      method: "POST",
      headers: {},
      body: form,
    })
  },

  getResumes(page = 1, size = 20): Promise<ResumeListResponse> {
    return request<ResumeListResponse>(`/resumes?page=${page}&size=${size}`)
  },

  getResumeDetail(id: string): Promise<ResumeResponse> {
    return request<ResumeResponse>(`/resumes/${id}`)
  },

  deleteResume(id: string): Promise<void> {
    return request<void>(`/resumes/${id}`, { method: "DELETE" })
  },

  runMatch(data: MatchRequest): Promise<MatchResponse> {
    return request<MatchResponse>("/match", {
      method: "POST",
      body: JSON.stringify(data),
    })
  },
}
