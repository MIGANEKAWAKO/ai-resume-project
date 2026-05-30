import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "@/components/ui/table"
import { Button } from "@/components/ui/button"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import type { ResumeListItem } from "@/types"

interface Props {
  items: ResumeListItem[]
  loading: boolean
  error: string | null
  page: number
  pageSize: number
  total: number
  onPageChange: (page: number) => void
  onViewDetail: (id: string) => void
  onDelete: (id: string) => void
}

export function ResumeTable({
  items, loading, error, page, pageSize, total, onPageChange, onViewDetail, onDelete,
}: Props) {
  const totalPages = Math.max(1, Math.ceil(total / pageSize))

  return (
    <Card>
      <CardHeader>
        <CardTitle>简历列表</CardTitle>
      </CardHeader>
      <CardContent>
        {loading && (
          <div className="flex items-center justify-center gap-2 py-16 text-sm text-[var(--color-muted-foreground)]">
            <div className="w-5 h-5 border-2 border-[var(--color-primary)]/30 border-t-[var(--color-primary)] rounded-full animate-spin" />
            加载中...
          </div>
        )}

        {error && (
          <div className="p-3 rounded-md bg-[var(--color-destructive)]/10 text-[var(--color-destructive)] text-sm">
            {error}
          </div>
        )}

        {!loading && !error && items.length === 0 && (
          <div className="text-center py-16 text-[var(--color-muted-foreground)]">
            <p className="text-lg">暂无简历</p>
            <p className="text-sm mt-1">请先上传简历</p>
          </div>
        )}

        {!loading && !error && items.length > 0 && (
          <>
            <Table>
              <TableHeader>
                <TableRow>
                  <TableHead>姓名</TableHead>
                  <TableHead>电话</TableHead>
                  <TableHead>邮箱</TableHead>
                  <TableHead>求职意向</TableHead>
                  <TableHead>上传时间</TableHead>
                  <TableHead className="w-[120px]">操作</TableHead>
                </TableRow>
              </TableHeader>
              <TableBody>
                {items.map((r) => (
                  <TableRow key={r.id}>
                    <TableCell className="font-medium">{r.name || "-"}</TableCell>
                    <TableCell>{r.phone || "-"}</TableCell>
                    <TableCell>{r.email || "-"}</TableCell>
                    <TableCell>{r.job_intent || "-"}</TableCell>
                    <TableCell>{new Date(r.created_at).toLocaleDateString("zh-CN")}</TableCell>
                    <TableCell>
                      <div className="flex gap-2">
                        <Button variant="outline" size="sm" onClick={() => onViewDetail(r.id)}>
                          详情
                        </Button>
                        <Button variant="destructive" size="sm" onClick={() => onDelete(r.id)}>
                          删除
                        </Button>
                      </div>
                    </TableCell>
                  </TableRow>
                ))}
              </TableBody>
            </Table>

            {totalPages > 1 && (
              <div className="flex items-center justify-center gap-2 mt-4">
                <Button
                  variant="outline"
                  size="sm"
                  disabled={page <= 1}
                  onClick={() => onPageChange(page - 1)}
                >
                  上一页
                </Button>
                <span className="text-sm text-[var(--color-muted-foreground)]">
                  第 {page} / {totalPages} 页（共 {total} 条）
                </span>
                <Button
                  variant="outline"
                  size="sm"
                  disabled={page >= totalPages}
                  onClick={() => onPageChange(page + 1)}
                >
                  下一页
                </Button>
              </div>
            )}
          </>
        )}
      </CardContent>
    </Card>
  )
}
