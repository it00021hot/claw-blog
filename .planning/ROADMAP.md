# Roadmap: 技术博客

## Overview

从零搭建一个支持技术文章和短篇小说双模式展示的 Hugo 静态博客，具备暗色/亮色主题切换、SEO 优化、Google AdSense 广告变现能力，最终通过 GitHub Actions 自动部署到 GitHub Pages。

## Phases

- [x] **Phase 1: 项目初始化与主题集成** - Hugo 项目搭建，PaperMod 主题配置，暗色/亮色主题支持 (completed 2026-03-08)
- [ ] **Phase 2: 内容分类与列表页** - 技术文章和短篇小说双分类目录
- [ ] **Phase 3: SEO 配置** - Meta 标签、Open Graph、Twitter Card、sitemap、robots.txt
- [ ] **Phase 4: 广告变现接入** - Google AdSense 脚本注入与广告位布局
- [ ] **Phase 5: 部署流水线** - GitHub Actions 工作流与自动部署

## Phase Details

### Phase 1: 项目初始化与主题集成

**Goal**: Hugo 项目基础结构搭建，PaperMod 主题集成，暗色/亮色主题支持

**Depends on**: Nothing (first phase)

**Requirements**: BASE-01, BASE-02, BASE-03, THEM-01, THEM-02, THEM-03

**Success Criteria** (what must be TRUE):
  1. 运行 `hugo server` 可以启动本地服务器并访问博客首页
  2. 暗色/亮色主题可以通过切换按钮正常切换
  3. 响应式布局在移动端（375px）正常显示，无横向滚动
  4. 代码块有正确的语法高亮显示

**Plans**: 1 plan (COMPLETED)

Plans:
- [x] 01-01-PLAN.md — 创建 Hugo 项目结构、安装 PaperMod 主题、配置 hugo.yaml

### Phase 2: 内容分类与列表页

**Goal**: 技术文章和短篇小说两个独立分类目录，文章列表页支持双分类展示

**Depends on**: Phase 1

**Requirements**: CONT-01, CONT-02, CONT-03, CONT-04

**Success Criteria** (what must be TRUE):
  1. 访问 /tech/ 路由可以查看技术文章列表
  2. 访问 /fiction/ 路由可以查看短篇小说列表
  3. 首页文章列表同时展示两个分类的文章
  4. 点击分类标签可以跳转到对应的分类页面

**Plans**: TBD

### Phase 3: SEO 配置

**Goal**: 完整的 SEO 元数据配置，支持社交分享和搜索引擎收录

**Depends on**: Phase 2

**Requirements**: SEO-01, SEO-02, SEO-03, SEO-04, SEO-05

**Success Criteria** (what must be TRUE):
  1. 每篇文章的 `<head>` 中包含正确的 title、description、keywords meta 标签
  2. 社交分享时（复制链接到微信/QQ）显示正确的标题、描述和预览图
  3. Twitter 分享时显示正确的 Twitter Card
  4. 访问 /sitemap.xml 返回有效的 XML sitemap
  5. 访问 /robots.txt 返回有效的 robots 规则

**Plans**: TBD

### Phase 4: 广告变现接入

**Goal**: Google AdSense 广告脚本注入与广告位布局适配

**Depends on**: Phase 3

**Requirements**: AD-01, AD-02

**Success Criteria** (what must be TRUE):
  1. Google AdSense 脚本正确注入到页面 `<head>` 中
  2. 广告位在文章内容区域合理展示，不影响阅读体验

**Plans**: TBD

### Phase 5: 部署流水线

**Goal**: GitHub Actions 工作流创建，实现自动部署到 GitHub Pages

**Depends on**: Phase 4

**Requirements**: DEPL-01, DEPL-02, DEPL-03

**Success Criteria** (what must be TRUE):
  1. GitHub Actions 工作流文件存在于 .github/workflows/
  2. 推送代码到 main 分支触发自动构建部署
  3. 部署完成后访问 GitHub Pages URL 可以正常浏览网站

**Plans**: TBD

## Progress

| Phase | Plans Complete | Status | Completed |
|-------|----------------|--------|-----------|
| 1. 项目初始化与主题集成 | 1/1 | Complete    | 2026-03-08 |
| 2. 内容分类与列表页 | 0/0 | Not started | - |
| 3. SEO 配置 | 0/0 | Not started | - |
| 4. 广告变现接入 | 0/0 | Not started | - |
| 5. 部署流水线 | 0/0 | Not started | - |
