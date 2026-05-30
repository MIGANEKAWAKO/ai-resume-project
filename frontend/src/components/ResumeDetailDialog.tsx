import { useState, useEffect } from "react"
import {
  Dialog,
  DialogContent,
  DialogHeader,
  DialogTitle,
} from "@/components/ui/dialog"
import type { ResumeResponse } from "@/types"
import { api } from "@/api/client"

const FIELD_LABELS: Record<string, string> = {
  name: "姓名",
  phone: "电话",
  email: "邮箱",
  address: "地址",
  job_intent: "求职意向",
  expected_salary: "期望薪资",
  work_years: "工作年限",
  education: "学历背景",
  projects: "项目经历",
}

interface Props {
  resumeId: string | null
  open: boolean
  onClose: () => void
}

export function ResumeDetailDialog({ resumeId, open, onClose }: Props) {
  const [data, setData] = useState<ResumeResponse | null>(null)
  const [loading, setLoading] = useState(false)

  useEffect(() => {
    if (resumeId && open) {
      setLoading(true)
      api.getResumeDetail(resumeId)
        .then(setData)
        .finally(() => setLoading(false))
    } else {
      setData(null)
    }
  }, [resumeId, open])

  return (
    <Dialog open={open} onOpenChange={(o) => { if (!o) onClose() }}>
      <DialogContent>
        <DialogHeader>
          <DialogTitle>{data?.original_filename || "简历详情"}</DialogTitle>
        </DialogHeader>

        {loading && (
          <div className="flex items-center justify-center gap-2 py-12 text-sm text-[var(--color-muted-foreground)]">
            <div className="w-5 h-5 border-2 border-[var(--color-primary)]/30 border-t-[var(--color-primary)] rounded-full animate-spin" />
            加载中...
          </div>
        )}

        {data && (
          <div className="px-6 pb-6 space-y-6">
            <div className="grid grid-cols-2 md:grid-cols-3 gap-4">
              {Object.entries(FIELD_LABELS).map(([key, label]) => (
                <div key={key}>
                  <div className="text-xs text-[var(--color-muted-foreground)]">{label}</div>
                  <div className="text-sm font-medium mt-0.5 break-all">
                    {data.parsed_info[key as keyof typeof data.parsed_info] || "-"}
                  </div>
                </div>
              ))}
            </div>

            <div>
              <h4 className="text-sm font-semibold text-[var(--color-muted-foreground)] mb-2">
                简历原文
              </h4>
              <pre className="text-xs text-[var(--color-muted-foreground)] bg-[var(--color-muted)] p-4 rounded-lg max-h-64 overflow-y-auto whitespace-pre-wrap">
                {data.raw_text}
              </pre>
            </div>
          </div>
        )}
      </DialogContent>
    </Dialog>
  )
}
