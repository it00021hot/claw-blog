# Phase 6: 内容抓取工具 - Context

**Gathered:** 2026-03-08
**Status:** Ready for planning

<domain>
## Phase Boundary

创建一个文章抓取工具，从 GitHub 仓库和技术博客抓取优质内容，使用 OpenAI API 格式化后转换为 Hugo Markdown 文件（带 Front Matter），并通过 AI 自动分类（Categories/Tags）。支持手动运行和 GitHub Actions 定时自动抓取。

</domain>

<decisions>
## Implementation Decisions

### 触发方式
- 混合模式：支持手动运行 + GitHub Actions 定时任务
- 默认定时：每天 8:00 UTC 自动运行
- GitHub Actions：独立 workflow（与部署 workflow 分离）
- 手动触发：直接运行 python 脚本 或 make fetch

### 输出格式
- 输出目录：同时输出到 content/tech/ 和 content/fiction/
- Front Matter：由 AI 自动判断需要哪些字段
- 文件命名：使用标题 slug 形式（如 openclaw-install-guide.md）
- 冲突处理：覆盖已存在的文件

### 去重策略
- 去重依据：基于 URL 判断是否已抓取
- 存储方式：JSON 文件记录已抓取的 URL
- 已存在处理：跳过，不重复抓取

### 抓取来源
- GitHub 仓库 (Issues、PR、README)
- 技术博客 URL

### AI 格式化
- 使用 OpenAI API (GPT-4) 进行内容处理
- 将内容转换为带 Front Matter 的 Hugo Markdown

### 分类方式
- 使用 AI 自动分析内容主题进行分类
- Categories: 安装、进阶、常见问题、教程、源码解析
- Tags: 从内容中提取关键词

### Claude's Discretion
- 具体的 Python 依赖库选择
- JSON 文件的具体格式和路径
- 定时任务的具体 cron 表达式
- 错误处理和日志策略

</decisions>

<specifics>
## Specific Ideas

- 输出到 content/tech/ 和 content/fiction/ 目录
- 文件命名规范化：标题 slug
- GitHub Actions 独立 workflow：.github/workflows/fetch-articles.yaml
- 支持增量更新（URL 去重）

</specifics>

<deferred>
## Deferred Ideas

- **多平台内容抓取** — 抓取抖音、小红书等社交媒体平台内容（未来阶段）
- GitHub Actions 集成 — 已在当前阶段考虑

</deferred>

---

*Phase: 06-内容抓取工具*
*Context gathered: 2026-03-08*
