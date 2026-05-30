import { useState, useRef, useCallback } from "react"
import { Upload, FileText } from "lucide-react"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Progress } from "@/components/ui/progress"
import type { ParsedResumeInfo } from "@/types"
import { api } from "@/api/client"

const FIELD_LABELS: Record<keyof ParsedResumeInfo, string> = {
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

export function UploadZone({ onSuccess }: { onSuccess: () => void }) {
  const [dragOver, setDragOver] = useState(false)
  const [uploading, setUploading] = useState(false)
  const [result, setResult] = useState<ParsedResumeInfo | null>(null)
  const [error, setError] = useState<string | null>(null)
  const inputRef = useRef<HTMLInputElement>(null)

  const handleFile = useCallback(async (file: File) => {
    if (!file.name.toLowerCase().endsWith(".pdf")) {
      setError("仅支持 PDF 格式文件")
      return
    }
    setError(null)
    setResult(null)
    setUploading(true)
    try {
      const data = await api.uploadResume(file)
      setResult(data.parsed_info)
      onSuccess()
    } catch (e) {
      setError((e as Error).message)
    } finally {
      setUploading(false)
    }
  }, [onSuccess])

  return (
    <Card>
      <CardHeader>
        <CardTitle>上传简历</CardTitle>
      </CardHeader>
      <CardContent className="space-y-4">
        <div
          className={`border-2 border-dashed rounded-xl p-12 text-center cursor-pointer transition-colors ${
            dragOver
              ? "border-[var(--color-primary)] bg-[var(--color-primary)]/5"
              : "border-[var(--color-border)] hover:border-[var(--color-primary-light)]"
          }`}
          onDragOver={(e) => { e.preventDefault(); setDragOver(true) }}
          onDragLeave={() => setDragOver(false)}
          onDrop={(e) => {
            e.preventDefault()
            setDragOver(false)
            const file = e.dataTransfer.files[0]
            if (file) handleFile(file)
          }}
          onClick={() => inputRef.current?.click()}
        >
          <Upload className="w-12 h-12 mx-auto mb-3 text-[var(--color-primary)]" />
          <p className="text-sm font-medium">点击或拖拽 PDF 简历到此处</p>
          <p className="text-xs text-[var(--color-muted-foreground)] mt-1">
            仅支持 PDF 格式，最大 10MB
          </p>
          <input
            ref={inputRef}
            type="file"
            accept=".pdf"
            className="hidden"
            onChange={(e) => {
              const file = e.target.files?.[0]
              if (file) handleFile(file)
              e.target.value = ""
            }}
          />
        </div>

        {uploading && (
          <div className="flex items-center gap-3 text-sm text-[var(--color-muted-foreground)]">
            <Progress value={undefined} className="flex-1" />
            <span>AI 正在解析简历...</span>
          </div>
        )}

        {error && (
          <div className="p-3 rounded-md bg-[var(--color-destructive)]/10 text-[var(--color-destructive)] text-sm font-medium">
            {error}
          </div>
        )}

        {result && (
          <div className="space-y-3">
            <div className="flex items-center gap-2 text-sm font-semibold text-[var(--color-success)]">
              <FileText className="w-4 h-4" />
              解析成功
            </div>
            <div className="grid grid-cols-2 md:grid-cols-3 gap-3">
              {(Object.keys(FIELD_LABELS) as Array<keyof ParsedResumeInfo>).map((key) => (
                <div key={key}>
                  <div className="text-xs text-[var(--color-muted-foreground)]">
                    {FIELD_LABELS[key]}
                  </div>
                  <div className="text-sm font-medium mt-0.5 break-all">
                    {result[key] || "-"}
                  </div>
                </div>
              ))}
            </div>
            <Button variant="outline" size="sm" onClick={() => setResult(null)}>
              继续上传
            </Button>
          </div>
        )}
      </CardContent>
    </Card>
  )
}
