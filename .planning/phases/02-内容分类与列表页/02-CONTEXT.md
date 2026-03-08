# Phase 2: 内容分类与列表页 - Context

**Gathered:** 2026-03-08
**Status:** Ready for planning

<domain>
## Phase Boundary

技术文章和短篇小说两个独立分类目录，文章列表页支持双分类展示。用户可以：
- 访问 /tech/ 查看技术文章列表
- 访问 /fiction/ 查看短篇小说列表
- 首页同时展示两个分类的最新文章

</domain>

<decisions>
## Implementation Decisions

### 分类展示方式
- 独立路由：/tech/ 和 /fiction/ 两个独立分类页面
- 原因：用户可书签收藏，便于 SEO，便于分享特定分类

### 列表布局
- 卡片式布局（PaperMod 默认）
- 每张卡片显示：标题、日期、摘要、分类标签

### 内容密度
- 摘要预览模式：标题 + 日期 + 摘要（约100字）+ 分类标签

### 列表排序
- 按日期倒序（最新在前）
- 默认开启

### 分类命名
- 技术文章：tech
- 短篇小说：fiction

</decisions>

<specifics>
## Specific Ideas

- 短篇小说可能需要不同的排版（Phase 1 提到的 deferred idea）
- 分类标签需在文章列表和详情页都显示

</specifics>

<code_context>
## Existing Code Insights

### Reusable Assets
- content/posts/ - 技术文章目录（Phase 1 已创建）
- content/fiction/ - 短篇小说目录（Phase 1 已创建）
- PaperMod 原生支持 section 列表页

### Established Patterns
- Hugo sections 机制实现独立分类
- PaperMod 内置 section 模板
- 分类通过 front matter 中的 categories 字段

### Integration Points
- 首页需整合两个 section 的最新文章
- 导航栏添加分类链接
- 后续 SEO 阶段依赖分类元数据

</code_context>

<deferred>
## Deferred Ideas

- 短篇小说特殊排版（如分章节、字体大小）— 后续优化
- 评论系统 — PROJECT.md 明确 Out of Scope

</deferred>

---

*Phase: 02-内容分类与列表页*
*Context gathered: 2026-03-08*
