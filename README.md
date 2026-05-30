# AI 简历智能筛选系统

上传简历、提取关键信息，通过 AI 模型实现岗位与候选人的智能匹配。

## 项目架构

```
ai-resume/
├── .github/workflows/
│   └── deploy-frontend.yml    # 前端 GitHub Pages 自动部署
├── frontend/                   # React SPA 前端
│   └── src/
│       ├── api/client.ts       # API 请求封装
│       ├── components/         # 业务组件
│       ├── components/ui/      # shadcn/ui 基础组件
│       ├── hooks/              # 自定义 Hooks
│       ├── pages/              # 页面组件
│       └── types/              # TypeScript 类型定义
├── backend/                    # Python FastAPI 后端
│   └── app/
│       ├── main.py             # 应用入口
│       ├── config.py           # 环境配置
│       ├── models/             # 数据库模型 & API Schema
│       ├── routers/            # RESTful 路由
│       ├── services/           # 核心业务逻辑
│       ├── core/               # 数据库引擎 & 异常处理
│       └── utils/              # 工具函数
└── README.md
```

## 技术选型

| 层 | 技术 | 说明 |
|---|------|------|
| **前端框架** | React 19 + TypeScript | SPA 单页应用 |
| **UI 组件库** | shadcn/ui + Radix UI | 无样式组件原语 |
| **CSS** | Tailwind CSS v4 | 原子化 CSS |
| **构建工具** | Vite 8 | 前端构建 |
| **后端框架** | FastAPI (Python 3.12) | 异步 Web 框架 |
| **ORM** | SQLAlchemy 2.0 (async) | 异步数据库操作 |
| **数据库** | SQLite + aiosqlite | 本地开发数据库 |
| **PDF 解析** | pdfplumber | 支持多页简历 |
| **AI 模型** | DeepSeek Chat API | 简历信息提取 & 匹配评分 |
| **模糊匹配** | rapidfuzz | 关键词相似度计算 |
| **通知** | sonner | Toast 通知 |

## API 端点

| Method | Path | 说明 |
|--------|------|------|
| `GET` | `/` | 服务信息 |
| `GET` | `/api/health` | 健康检查 |
| `GET` | `/docs` | Swagger 文档 |
| `POST` | `/api/v1/resumes` | 上传 PDF 简历并解析 |
| `GET` | `/api/v1/resumes` | 分页获取简历列表 |
| `GET` | `/api/v1/resumes/{id}` | 获取简历详情 |
| `DELETE` | `/api/v1/resumes/{id}` | 删除简历 |
| `POST` | `/api/v1/match` | 提交岗位描述并返回匹配结果 |
| `GET` | `/api/v1/match/{id}` | 查看匹配结果详情 |

## 前端页面功能

- **简历列表** — 查看所有已上传简历，支持分页、详情弹窗、删除
- **上传简历** — 拖拽或点击上传 PDF，AI 自动解析并展示结构化信息
- **智能匹配** — 输入岗位描述，AI 对全部简历进行评分排序，展示技能匹配率、优势、不足、推荐意见

## 部署方式

### 前端 → GitHub Pages

1. GitHub 仓库 Settings → Pages → Source 选 "GitHub Actions"
2. Settings → Secrets and variables → Actions → Variables 添加 `VITE_API_BASE_URL`（后端 URL）
3. Push 到 `main` 分支自动触发部署

### 后端 → 阿里云函数计算

1. 在阿里云 FC 控制台创建 FastAPI Web 应用，绑定 GitHub 仓库
2. 将 `backend/` 目录下的代码放入仓库的 `code/` 文件夹
3. 在 FC 控制台配置环境变量：`DEEPSEEK_API_KEY`、`DATABASE_URL`、`UPLOAD_DIR`
4. 推送代码自动部署

## 本地开发

### 后端

```bash
cd backend
python -m venv venv
source venv/Scripts/activate   # Windows
pip install -r requirements.txt
cp .env.example .env           # 编辑 .env 填入 DeepSeek API Key
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

### 前端

```bash
cd frontend
npm install
echo "VITE_API_BASE_URL=http://localhost:8000/api/v1" > .env
npm run dev
```

打开 http://localhost:5173 即可本地调试。
