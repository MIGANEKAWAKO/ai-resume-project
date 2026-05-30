import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"
import { Progress } from "@/components/ui/progress"
import type { MatchResultItem } from "@/types"

interface Props {
  results: MatchResultItem[]
  jobTitle: string
  jobKeywords: string[]
  error: string | null
}

function scoreVariant(score: number): "success" | "warning" | "destructive" {
  if (score >= 70) return "success"
  if (score >= 40) return "warning"
  return "destructive"
}

function scoreLabel(score: number): string {
  if (score >= 70) return "强烈推荐"
  if (score >= 40) return "可考虑"
  return "暂不推荐"
}

export function MatchResultCard({ results, jobTitle, jobKeywords, error }: Props) {
  return (
    <Card className="mt-6">
      <CardHeader>
        <CardTitle>
          {jobTitle ? `匹配结果：${jobTitle}` : "匹配结果"}
        </CardTitle>
      </CardHeader>
      <CardContent>
        {error && (
          <div className="p-3 rounded-md bg-[var(--color-destructive)]/10 text-[var(--color-destructive)] text-sm mb-4">
            {error}
          </div>
        )}

        {jobKeywords.length > 0 && (
          <div className="mb-4">
            <span className="text-sm font-medium text-[var(--color-muted-foreground)] mr-2">
              岗位关键词：
            </span>
            {jobKeywords.map((kw, i) => (
              <Badge key={i} variant="secondary" className="mr-1 mb-1">
                {kw}
              </Badge>
            ))}
          </div>
        )}

        {results.length === 0 && !error && (
          <div className="text-center py-12 text-[var(--color-muted-foreground)]">
            暂无匹配结果
          </div>
        )}

        <div className="space-y-3">
          {results.map((r, i) => {
            const analysis = r.ai_analysis || {}
            return (
              <div
                key={r.resume_id}
                className="border rounded-lg p-4 hover:shadow-sm transition-shadow"
              >
                <div className="flex items-center justify-between mb-2">
                  <div className="flex items-center gap-2">
                    <Badge variant="default">#{i + 1}</Badge>
                    <span className="font-semibold text-sm">{r.resume_name}</span>
                  </div>
                  <div className="flex items-center gap-2">
                    <Badge variant={scoreVariant(r.score)}>{scoreLabel(r.score)}</Badge>
                    <span className="text-xl font-bold">{r.score.toFixed(1)}</span>
                  </div>
                </div>

                <Progress value={Math.min(r.score, 100)} className="mb-3" />

                <div className="flex gap-4 text-xs text-[var(--color-muted-foreground)] mb-3">
                  <span>技能匹配率：{(r.skill_match_rate * 100).toFixed(0)}%</span>
                  <span>经验相关性：{(r.experience_relevance * 100).toFixed(0)}%</span>
                </div>

                {analysis.advantage && (
                  <div className="text-xs mb-1">
                    <span className="font-medium text-[var(--color-success)]">优势：</span>
                    <span className="text-[var(--color-muted-foreground)]">{analysis.advantage}</span>
                  </div>
                )}
                {analysis.weakness && (
                  <div className="text-xs mb-1">
                    <span className="font-medium text-[var(--color-destructive)]">不足：</span>
                    <span className="text-[var(--color-muted-foreground)]">{analysis.weakness}</span>
                  </div>
                )}
                {analysis.recommendation && (
                  <div className="text-xs">
                    <span className="font-medium text-[var(--color-primary)]">建议：</span>
                    <span className="text-[var(--color-muted-foreground)]">{analysis.recommendation}</span>
                  </div>
                )}
              </div>
            )
          })}
        </div>
      </CardContent>
    </Card>
  )
}
