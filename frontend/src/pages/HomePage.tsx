import { useState, useEffect, useCallback } from "react"
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs"
import { UploadZone } from "@/components/UploadZone"
import { ResumeTable } from "@/components/ResumeTable"
import { ResumeDetailDialog } from "@/components/ResumeDetailDialog"
import { JobMatchForm } from "@/components/JobMatchForm"
import { MatchResultCard } from "@/components/MatchResultCard"
import { useResumes } from "@/hooks/use-resumes"
import { useMatch } from "@/hooks/use-match"
import { toast } from "sonner"

export function HomePage() {
  const [tab, setTab] = useState("resumes")
  const resumes = useResumes()
  const match = useMatch()
  const [detailId, setDetailId] = useState<string | null>(null)
  const [detailOpen, setDetailOpen] = useState(false)

  useEffect(() => {
    if (tab === "resumes") {
      resumes.load(resumes.page)
    }
  }, [tab])

  const handleDelete = useCallback(async (id: string) => {
    try {
      await resumes.remove(id)
      toast.success("简历已删除")
    } catch {
      toast.error("删除失败")
    }
  }, [resumes])

  return (
    <div className="max-w-6xl mx-auto px-6 pb-12">
      <Tabs value={tab} onValueChange={setTab}>
        <TabsList className="w-full max-w-md mx-auto mb-6">
          <TabsTrigger value="resumes" className="flex-1">简历列表</TabsTrigger>
          <TabsTrigger value="upload" className="flex-1">上传简历</TabsTrigger>
          <TabsTrigger value="match" className="flex-1">智能匹配</TabsTrigger>
        </TabsList>

        <TabsContent value="resumes">
          <ResumeTable
            items={resumes.items}
            loading={resumes.loading}
            error={resumes.error}
            page={resumes.page}
            pageSize={resumes.pageSize}
            total={resumes.total}
            onPageChange={(p) => resumes.load(p)}
            onViewDetail={(id) => { setDetailId(id); setDetailOpen(true) }}
            onDelete={handleDelete}
          />
          <ResumeDetailDialog
            resumeId={detailId}
            open={detailOpen}
            onClose={() => setDetailOpen(false)}
          />
        </TabsContent>

        <TabsContent value="upload">
          <UploadZone onSuccess={() => resumes.load(1)} />
        </TabsContent>

        <TabsContent value="match">
          <JobMatchForm onMatch={match.run} loading={match.loading} />
          {match.results.length > 0 || match.error ? (
            <MatchResultCard
              results={match.results}
              jobTitle={match.jobTitle}
              jobKeywords={match.jobKeywords}
              error={match.error}
            />
          ) : null}
        </TabsContent>
      </Tabs>
    </div>
  )
}
