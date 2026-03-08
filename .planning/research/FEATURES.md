# Feature Research

**Domain:** Hugo 静态博客
**Researched:** 2026-03-08
**Confidence:** MEDIUM

## Feature Landscape

### Table Stakes (Users Expect These)

基础功能是用户认为博客"理所当然应该有"的功能。缺少这些功能会让人觉得博客不完整或有问题。

| Feature | Why Expected | Complexity | Notes |
|---------|--------------|------------|-------|
| 文章列表页 | 用户浏览博文的入口，展示最新/所有文章 | LOW | PaperMod 原生支持 |
| 文章详情页 | 阅读文章内容的主要页面 | LOW | PaperMod 原生支持 |
| 分类 (Categories) | 组织内容的基本方式，用户按主题筛选 | LOW | Hugo 原生支持 |
| 标签 (Tags) | 更细粒度的内容组织 | LOW | Hugo 原生支持 |
| 暗色/亮色主题 | 现代网页标配，改善阅读体验 | LOW | PaperMod 内置支持 |
| SEO 元数据 | 搜索引擎收录必要信息 (title, description, og:image) | LOW | PaperMod 配置即可 |
| 响应式布局 | 移动端阅读必须 | LOW | PaperMod 主题自带 |
| RSS 订阅 | 读者获取更新的标准方式 | LOW | Hugo 原生生成 |
| 代码高亮 | 技术博客展示代码的必需功能 | LOW | Hugo 内置 Chroma |
| 图片/媒体支持 | 插入图片、视频等富媒体 | LOW | Hugo 原生支持 Markdown |

### Differentiators (Competitive Advantage)

差异化功能是项目的竞争优势来源，基于项目目标（技术文章 + 短篇小说双模式 + 广告变现）。

| Feature | Value Proposition | Complexity | Notes |
|---------|-------------------|------------|-------|
| 技术文章/短篇双分类 | 满足两类内容独立展示需求，PROJECT.md 明确需求 | LOW | 使用 Hugo sections 区分 |
| Google AdSense 广告 | 项目变现目标的核心功能 | MEDIUM | 需要广告位布局配置 |
| 首页精选文章 | 突出展示重要文章，提升阅读量 | LOW | 可通过 front matter 标记 |
| 阅读时间估算 | 帮助读者预估阅读时长 | LOW | Hugo 内置 .ReadingTime |
| 文章目录 (TOC) | 长文章导航，提升阅读体验 | LOW | PaperMod 支持 |
| 社交分享按钮 | 方便读者分享内容 | LOW | 可通过 shortcode 实现 |
| 相关文章推荐 | 增加页面浏览深度 | LOW | Hugo 内置 .Related |
| 面包屑导航 | 帮助用户理解当前位置 | LOW | PaperMod 支持 |

### Anti-Features (Commonly Requested, Often Problematic)

PROJECT.md 明确指出以下功能不在范围内，这些功能看起来有用但被刻意排除。

| Feature | Why Requested | Why Problematic | Alternative |
|---------|---------------|-----------------|-------------|
| 评论系统 | 用户互动、社交证明 | 需要后端服务（Disqus/Gitalk），增加复杂度，维护成本 | 留作未来考虑 |
| 搜索功能 | 用户快速找内容 | 静态站点搜索需要客户端 JS (Lunr/Fuse) 或服务端，增加复杂度 | 依赖分类/标签导航 |
| 访问统计 (Analytics) | 了解读者行为 | 需要第三方服务 (Google Analytics)，隐私合规问题 | 留作未来考虑 |

## Feature Dependencies

```
[暗色/亮色主题]
    └──无依赖──> [基础主题架构]

[文章列表/详情]
    └──依赖──> [分类/标签系统]
               └──依赖──> [内容组织结构]

[Google AdSense]
    └──依赖──> [SEO 元数据]
               └──依赖──> [主题基础]

[技术文章/短篇双分类]
    └──依赖──> [Hugo Sections 配置]
```

### Dependency Notes

- **暗色/亮色主题**：PaperMod 内置支持，无额外依赖
- **文章列表/详情**依赖分类/标签系统：这是内容导航的基础
- **Google AdSense** 依赖 SEO 元数据：广告展示需要页面有正确元数据
- **技术文章/短篇双分类** 依赖 Hugo Sections：需要正确配置 content 目录结构

## MVP Definition

### Launch With (v1)

首批发布必须包含的功能，基于 PROJECT.md 的 Active 需求。

- [x] Hugo 项目初始化，基础目录结构 — 项目基础
- [x] PaperMod 主题集成与配置 — 视觉和功能基础
- [x] 暗色/亮色主题支持 — 用户体验标配
- [x] 技术文章分类与列表页 — 核心内容类型
- [x] 短篇小说独立分类页面 — 第二个内容类型
- [x] SEO 元数据配置 — 搜索引擎可见性
- [x] Google AdSense 广告接入 — 项目变现目标
- [x] GitHub Pages 部署流水线 — 部署需求

### Add After Validation (v1.x)

核心验证后考虑添加的功能。

- [ ] 社交分享按钮 — 用户反馈需要时添加
- [ ] 相关文章推荐 — 增加页面浏览深度
- [ ] 文章目录 (TOC) 折叠展开 — 长文章导航

### Future Consideration (v2+)

产品市场匹配后考虑的功能。

- [ ] 评论系统 — 需要评估维护成本
- [ ] 搜索功能 — 内容增多后的需求
- [ ] 访问统计 — 了解读者行为
- [ ] 更多变现方式 (Affiliate, 付费内容)

## Feature Prioritization Matrix

| Feature | User Value | Implementation Cost | Priority |
|---------|------------|---------------------|----------|
| Hugo 项目初始化 | HIGH | LOW | P1 |
| PaperMod 主题 | HIGH | LOW | P1 |
| 暗色/亮色主题 | HIGH | LOW | P1 |
| 技术文章/短篇分类 | HIGH | LOW | P1 |
| SEO 元数据 | HIGH | LOW | P1 |
| Google AdSense | HIGH | MEDIUM | P1 |
| GitHub Pages 部署 | HIGH | LOW | P1 |
| RSS 订阅 | MEDIUM | LOW | P2 |
| 代码高亮 | MEDIUM | LOW | P2 |
| 社交分享 | LOW | LOW | P3 |
| 相关文章推荐 | LOW | LOW | P3 |
| 评论系统 | MEDIUM | HIGH | P3 (未来) |
| 搜索功能 | MEDIUM | MEDIUM | P3 (未来) |
| 访问统计 | LOW | MEDIUM | P3 (未来) |

**Priority key:**
- P1: Must have for launch
- P2: Should have, add when possible
- P3: Nice to have, future consideration

## Competitor Feature Analysis

| Feature | 主流 Hugo 博客 | 商业博客平台 (Medium) | Our Approach |
|---------|----------------|---------------------|--------------|
| 文章展示 | ✅ 原生支持 | ✅ | 同主流 |
| 分类/标签 | ✅ 原生支持 | ✅ | 同主流 |
| 暗色主题 | ✅ 主题支持 | ✅ | 同主流 |
| 广告变现 | ⚠️ 需自行接入 | ✅ 平台提供 | 自行接入 AdSense |
| 评论系统 | ⚠️ 需第三方 | ✅ 平台提供 | 排除 (维护成本) |
| 搜索功能 | ⚠️ 需额外配置 | ✅ 平台提供 | 排除 (复杂度) |
| 数据分析 | ⚠️ 需第三方 | ✅ 平台提供 | 排除 (隐私合规) |

**分析结论：**
- Hugo 博客在内容展示、分类、主题方面与商业平台持平
- 差异在于需要自行接入第三方服务（广告、统计）
- 选择排除评论、搜索、统计是合理取舍，聚焦核心内容展示

## Sources

- Hugo 官方文档: https://gohugo.io/
- PaperMod 主题: https://github.com/adityatelange/hugo-PaperMod
- 项目需求: PROJECT.md

---
*Feature research for: Hugo 静态博客*
*Researched: 2026-03-08*
