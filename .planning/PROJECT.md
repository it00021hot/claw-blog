# 技术博客

## What This Is

使用 Hugo 搭建的个人技术博客，支持技术文章和短篇小说双模式。采用 PaperMod 主题，具备暗色/亮色主题切换、SEO 优化、Google AdSense 广告接入，部署到 GitHub Pages。

## Core Value

一个简洁、高性能的个人博客，能够优雅地展示技术文章和短篇小说，并通过广告实现有限变现。

## Requirements

### Validated

(None yet — ship to validate)

### Active

- [ ] Hugo 项目初始化，基础目录结构搭建
- [ ] PaperMod 主题集成与配置
- [ ] 暗色/亮色主题支持
- [ ] 技术文章分类与列表页
- [ ] 短篇小说独立分类页面
- [ ] SEO 元数据配置
- [ ] Google AdSense 广告接入
- [ ] GitHub Pages 部署流水线配置

### Out of Scope

- 评论系统
- 搜索功能
- 统计Analytics

## Context

- Google AdSense ID: ca-pub-8708502478021488
- 部署平台: GitHub Pages
- 主题: PaperMod
- 内容类型: 技术文章 + 短篇小说

## Constraints

- **部署**: GitHub Pages — 免费托管，需要 GitHub Actions
- **主题**: PaperMod — 开源免费，社区活跃
- **SEO**: 本地 Hugo，无后端依赖

## Key Decisions

| Decision | Rationale | Outcome |
|----------|-----------|---------|
| PaperMod 主题 | 轻量、SEO友好、暗亮色支持 | — Pending |
| 技术文章 + 短篇双分类 | 满足两类内容独立展示需求 | — Pending |
| GitHub Actions 部署 | 免费 CI/CD，与 GitHub Pages 无缝集成 | — Pending |

---
*Last updated: 2026-03-08 after initialization*
