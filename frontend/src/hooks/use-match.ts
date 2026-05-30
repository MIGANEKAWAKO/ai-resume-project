import { useState } from "react"
import type { MatchResultItem } from "@/types"
import { api } from "@/api/client"

export function useMatch() {
  const [results, setResults] = useState<MatchResultItem[]>([])
  const [jobTitle, setJobTitle] = useState("")
  const [jobKeywords, setJobKeywords] = useState<string[]>([])
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)

  const run = async (title: string, description: string) => {
    setLoading(true)
    setError(null)
    setResults([])
    setJobKeywords([])
    setJobTitle(title)
    try {
      const data = await api.runMatch({ title, description })
      setResults(data.results)
      setJobKeywords(data.job_keywords)
    } catch (e) {
      setError((e as Error).message)
    } finally {
      setLoading(false)
    }
  }

  const reset = () => {
    setResults([])
    setJobKeywords([])
    setJobTitle("")
    setError(null)
  }

  return { results, jobTitle, jobKeywords, loading, error, run, reset }
}
