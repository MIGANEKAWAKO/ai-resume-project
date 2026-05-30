export function Header() {
  return (
    <header className="bg-gradient-to-r from-[var(--color-primary)] to-[var(--color-primary-light)] text-white py-8 mb-8">
      <div className="max-w-6xl mx-auto px-6">
        <h1 className="text-2xl font-bold">AI 简历智能筛选系统</h1>
        <p className="text-sm opacity-85 mt-1">
          上传简历、提取关键信息，通过 AI 模型实现岗位智能匹配
        </p>
      </div>
    </header>
  )
}
