# Project Research Summary

**Project:** Hugo 静态博客 (claw-blog)
**Domain:** 静态博客 / 个人网站
**Researched:** 2026-03-08
**Confidence:** HIGH

## Executive Summary

这是一个技术博客项目，旨在搭建一个支持技术文章和短篇小说双模式展示的静态博客系统，并具备广告变现能力。基于对 Hugo 静态站点生成器生态的深入研究，推荐采用 **Hugo + PaperMod 主题 + GitHub Pages** 的技术栈，这是目前最成熟、社区支持最完善的静态博客方案。

**核心发现：**
- Hugo 是静态博客的事实标准，纯二进制、无运行时依赖、构建速度极快
- PaperMod 主题轻量、SEO 友好、暗亮色主题原生支持
- GitHub Pages + Actions 提供免费托管和自动化部署

**主要风险与缓解：**
- 直接修改主题源码会导致更新丢失 —— 必须使用 layouts/ 覆盖机制
- 分类体系设计需要提前规划 —— 明确 categories/tags/series 的语义区别
- 部署配置涉及 baseURL、submodule 等细节 —— 需严格按文档配置

## Key Findings

### Recommended Stack

基于官方文档和社区共识，推荐以下技术栈：

**Core technologies:**
- **Hugo v0.157.0+** — 静态站点生成器，纯二进制、无运行时依赖、构建速度极快
- **PaperMod v7.0+** — Hugo 主题，轻量(无 JS 依赖)、SEO 友好、暗亮色主题原生支持
- **GitHub Pages** — 静态网站托管，免费、无带宽限制、与 GitHub Actions 无缝集成
- **GitHub Actions** — CI/CD 流水线，免费额度充足、自动化构建部署

**Development Tools:**
- Git (版本控制，用于主题 submodule 和部署)
- 任意编辑器 (推荐 VS Code + Markdown 插件)

### Expected Features

**Must have (table stakes):**
- 文章列表页 / 详情页 — 博客核心功能
- 分类 (Categories) / 标签 (Tags) — 内容组织基础
- 暗色/亮色主题 — 现代网页标配
- SEO 元数据 — 搜索引擎收录必要信息
- RSS 订阅 — 读者获取更新的标准方式
- 代码高亮 — 技术博客必需功能
- 响应式布局 — 移动端阅读必须

**Should have (competitive):**
- 技术文章/短篇小说双分类 — 项目差异化需求，使用 Hugo Sections 区分
- Google AdSense 广告 — 项目变现目标的核心功能
- 首页精选文章 — 突出展示重要文章
- 阅读时间估算 — 提升阅读体验

**Defer (v2+):**
- 评论系统 — 需要后端服务，增加维护成本
- 搜索功能 — 静态站点搜索增加复杂度
- 访问统计 — 隐私合规问题

### Architecture Approach

Hugo 架构围绕"内容→模板→输出"的单向数据流构建，系统层次结构清晰：

**Major components:**
1. **Content Layer** — 存放 Markdown 内容文件，按类型/日期组织目录
2. **Configuration Layer** — hugo.yaml 配置文件，控制站点行为
3. **Theme Layer** — 主题模板 (PaperMod)，控制页面渲染
4. **Build Layer** — Hugo Engine，解析→渲染→输出
5. **Output Layer** — public/ 目录，最终静态文件

**核心架构模式：**
- 模板继承：使用 `{{ define }}` 和 `{{ template }}` 实现模板复用
- 短代码：在 Markdown 中调用的可复用组件
- 资源管道：处理 CSS/JS/Images 的构建流程
- 数据模板：使用 data/ 目录驱动内容

### Critical Pitfalls

**必须避免的 5 个关键陷阱：**

1. **直接修改主题源码** — 主题更新后所有自定义修改丢失
   - 缓解：所有自定义放在项目根目录的 layouts/ 目录，使用覆盖机制

2. **分类体系设计混乱** — categories/tags/series 混用导致内容组织无序
   - 缓解：明确 taxonomy 语义，categories 用于大领域，tags 用于具体技术点，series 用于系列文章

3. **SEO 配置不完整** — 搜索引擎收录不完整，社交分享显示默认占位符
   - 缓解：配置完整的 SEO 参数，验证 social meta tags

4. **部署配置错误** — GitHub Actions 构建失败，子目录路径问题
   - 缓解：明确 baseURL 配置，使用 actions-hugo 指定明确版本，正确管理 submodule

5. **图片与资源路径问题** — 本地预览正常，部署后资源 404
   - 缓解：使用 Hugo 资源函数 `resources.Get`，避免硬编码路径

## Implications for Roadmap

基于研究，建议以下阶段划分：

### Phase 1: 项目初始化与主题集成
**Rationale:** 这是所有后续工作的基础，必须正确配置才能避免后续返工
**Delivers:** 可运行的 Hugo 项目，本地预览正常
**Addresses:**
- Hugo 项目初始化，基础目录结构
- PaperMod 主题安装与基础配置
- 暗色/亮色主题支持
**Avoids:** 直接修改主题源码陷阱、资源路径问题

### Phase 2: 内容分类与列表页
**Rationale:** 建立内容组织结构，为内容创作打基础
**Delivers:** 技术文章和短篇小说两个独立分类
**Addresses:**
- 技术文章/短篇双分类 (Hugo Sections)
- 分类 (Categories) / 标签 (Tags) 系统
- 文章列表页
**Avoids:** 分类体系设计混乱陷阱

### Phase 3: 主题定制与样式
**Rationale:** 在基础内容结构完成后进行视觉定制
**Delivers:** 自定义 CSS 和部分模板覆盖
**Addresses:**
- 自定义样式覆盖
- layouts/ 目录模板覆盖
**Uses:** Hugo 资源管道 (assets/)
**Implements:** 模板继承模式

### Phase 4: SEO 与功能完善
**Rationale:** SEO 是变现（AdSense）的前提，需要在内容丰富前完成配置
**Delivers:** 完整的 SEO 元数据和社交分享支持
**Addresses:**
- SEO 元数据配置 (title, description, og:image)
- RSS 订阅
- 代码高亮
- 面包屑导航
**Avoids:** SEO 配置不完整陷阱

### Phase 5: 广告变现接入
**Rationale:** 项目核心目标，在 SEO 完善后接入
**Delivers:** Google AdSense 广告位
**Addresses:**
- Google AdSense 广告接入
- 广告位布局配置
**Implements:** 通过 Hugo partials 注入广告代码

### Phase 6: 部署流水线
**Rationale:** 所有功能开发完成后配置
**Delivers:** 自动化部署到 GitHub Pages
**Addresses:**
- GitHub Actions 工作流配置
- 部署验证
**Avoids:** 部署配置错误陷阱

### Phase Ordering Rationale

- **基础先行：** Phase 1-2 建立项目基础和内容结构，确保后续工作在稳固地基上开展
- **内容优先于定制：** 先完成内容分类(Phase 2)，再进行主题定制(Phase 3)，避免样式与内容脱节
- **SEO 先于变现：** Phase 4 先完成 SEO 配置，因为 AdSense 需要正确的页面元数据
- **功能先于部署：** Phase 5 完成功能开发，Phase 6 才配置部署，避免部署后发现功能问题

### Research Flags

Phases likely needing deeper research during planning:
- **Phase 5 (广告变现):** Google AdSense 具体的广告位布局和效果优化可能需要更多研究
- **Phase 3 (主题定制):** 自定义 CSS 的范围和深度需要根据实际需求确定

Phases with standard patterns (skip research-phase):
- **Phase 1 (项目初始化):** Hugo 官方文档详尽，标准模式明确
- **Phase 6 (部署):** GitHub Pages + Hugo 部署有成熟的工作流模板

## Confidence Assessment

| Area | Confidence | Notes |
|------|------------|-------|
| Stack | HIGH | 基于 Hugo/PaperMod 官方文档 |
| Features | HIGH | 项目需求明确，功能边界清晰 |
| Architecture | HIGH | Hugo 架构文档详尽，模式成熟 |
| Pitfalls | MEDIUM | 社区经验总结，部分为推断 |

**Overall confidence:** HIGH

### Gaps to Address

- **AdSense 效果验证：** 广告位的具体布局和位置对变现效果的影响需要上线后实际数据验证
- **自定义域名：** 如果后续使用自定义域名，HTTPS 配置需要额外研究

## Sources

### Primary (HIGH confidence)
- [Hugo Official Documentation](https://gohugo.io/documentation/) — 官方文档，堆栈和架构信息的核心来源
- [Hugo GitHub Pages Deployment](https://gohugo.io/hosting-and-deployment/hosting-on-github/) — 官方部署指南
- [PaperMod Theme Documentation](https://adityatelange.github.io/hugo-PaperMod/) — 官方主题文档

### Secondary (MEDIUM confidence)
- [PaperMod GitHub Repository](https://github.com/adityatelange/hugo-PaperMod) — 主题源码和 issues
- Hugo 社区常见问题 — Pitfalls 的部分来源

---

*Research completed: 2026-03-08*
*Ready for roadmap: yes*
