import { useState, useCallback } from "react"
import type { ResumeListItem } from "@/types"
import { api } from "@/api/client"

export function useResumes() {
  const [items, setItems] = useState<ResumeListItem[]>([])
  const [total, setTotal] = useState(0)
  const [page, setPage] = useState(1)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)
  const pageSize = 20

  const load = useCallback(async (p = 1) => {
    setLoading(true)
    setError(null)
    try {
      const data = await api.getResumes(p, pageSize)
      setItems(data.items)
      setTotal(data.total)
      setPage(data.page)
    } catch (e) {
      setError((e as Error).message)
    } finally {
      setLoading(false)
    }
  }, [])

  const remove = useCallback(async (id: string) => {
    await api.deleteResume(id)
    setItems(prev => prev.filter(i => i.id !== id))
    setTotal(prev => prev - 1)
  }, [])

  return { items, total, page, pageSize, loading, error, load, remove }
}
