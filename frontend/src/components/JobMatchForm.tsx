import { useState } from "react"
import { Search } from "lucide-react"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Input } from "@/components/ui/input"
import { Textarea } from "@/components/ui/textarea"
import { Button } from "@/components/ui/button"

interface Props {
  onMatch: (title: string, description: string) => void
  loading: boolean
}

export function JobMatchForm({ onMatch, loading }: Props) {
  const [title, setTitle] = useState("")
  const [description, setDescription] = useState("")

  const handleSubmit = () => {
    if (!description.trim()) return
    onMatch(title.trim(), description.trim())
  }

  return (
    <Card>
      <CardHeader>
        <CardTitle>岗位描述</CardTitle>
      </CardHeader>
      <CardContent className="space-y-4">
        <div className="space-y-1.5">
          <label className="text-sm font-medium text-[var(--color-muted-foreground)]">
            岗位名称（选填）
          </label>
          <Input
            placeholder="例如：高级 Python 开发工程师"
            value={title}
            onChange={(e) => setTitle(e.target.value)}
          />
        </div>
        <div className="space-y-1.5">
          <label className="text-sm font-medium text-[var(--color-muted-foreground)]">
            岗位需求描述 *
          </label>
          <Textarea
            placeholder="请粘贴完整的岗位需求描述，包括技能要求、经验要求、岗位职责等..."
            rows={6}
            value={description}
            onChange={(e) => setDescription(e.target.value)}
          />
        </div>
        <div className="flex items-center gap-3">
          <Button onClick={handleSubmit} disabled={loading || !description.trim()}>
            {loading ? (
              <>
                <div className="w-4 h-4 border-2 border-white/30 border-t-white rounded-full animate-spin" />
                AI 匹配中...
              </>
            ) : (
              <>
                <Search className="w-4 h-4" />
                开始匹配
              </>
            )}
          </Button>
          {loading && (
            <span className="text-xs text-[var(--color-muted-foreground)]">
              正在调用 AI 模型对简历进行评分和排序...
            </span>
          )}
        </div>
      </CardContent>
    </Card>
  )
}
