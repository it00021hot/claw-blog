# Phase 3: SEO 配置 - Research

**Researched:** 2026-03-08
**Domain:** Hugo + PaperMod SEO 配置
**Confidence:** HIGH

## Summary

Hugo + PaperMod 主题提供了开箱即用的 SEO 支持，PaperMod 主题内置了完整的 Open Graph、Twitter Card 和 Schema.org JSON-LD 支持。SEO 标签仅在生产环境（`hugo.IsProduction` 或 `env: production`）下渲染。

**Primary recommendation:** 通过在 hugo.yaml 中配置 `enableRobotsTXT: true` 启用 robots.txt，配置 `sitemap` 参数调整 sitemap.xml，文章 front matter 中添加 title、description、keywords 即可完成 SEO 配置。

## Phase Requirements

| ID | Description | Research Support |
|----|-------------|-----------------|
| SEO-01 | Meta 标签配置（title, description, keywords） | PaperMod head.html 内置支持，需在 front matter 中配置 |
| SEO-02 | Open Graph 社交分享元数据 | PaperMod 内置 opengraph.html 模板，需配置 cover image |
| SEO-03 | Twitter Card 元数据 | PaperMod 内置 twitter_cards.html 模板，需配置 cover image |
| SEO-04 | sitemap.xml 自动生成 | Hugo 原生支持，hugo.yaml 配置 |
| SEO-05 | robots.txt 配置 | Hugo 原生支持，enableRobotsTXT 配置 |

## Standard Stack

### Core Configuration

| Item | Configuration | Purpose |
|------|---------------|---------|
| Hugo | v0.157.0+extended | 静态网站生成器 |
| PaperMod | latest | Hugo 主题，内置 SEO 支持 |

### SEO 相关配置项

| 配置项 | 位置 | 说明 |
|--------|------|------|
| `enableRobotsTXT` | hugo.yaml | 启用自动生成 robots.txt |
| `sitemap` | hugo.yaml | sitemap.xml 配置 |
| `params.keywords` | hugo.yaml | 全站关键词 |
| `params.description` | hugo.yaml | 全站描述 |
| `params.social` | hugo.yaml | 社交媒体账号（Twitter、Facebook） |
| `params.assets.favicon` | hugo.yaml | Favicon 配置 |

**hugo.yaml 基础 SEO 配置示例：**
```yaml
baseURL: "https://your-domain.com/"
languageCode: "zh-cn"
title: "你的博客标题"
enableRobotsTXT: true

sitemap:
  changeFreq: "weekly"
  priority: 0.5

params:
  description: "博客描述"
  keywords: ["技术", "博客", "编程"]
  social:
    twitter: "@yourhandle"
  assets:
    favicon: "favicon.ico"
    favicon32x32: "favicon-32x32.png"
    favicon16x16: "favicon-16x16.png"
    apple_touch_icon: "apple-touch-icon.png"
    theme_color: "#ffffff"
```

## Architecture Patterns

### Article Front Matter Pattern

每篇文章的 front matter 应包含：

```yaml
---
title: "文章标题"
description: "文章描述（用于 SEO 和社交分享）"
keywords: ["关键词1", "关键词2"]
cover:
  image: "cover.jpg"  # 用于 Open Graph 和 Twitter Card
  alt: "封面图描述"
  caption: "封面图来源"
  relative: false
date: 2026-03-08
tags: ["标签1", "标签2"]
categories: ["分类1"]
---
```

### SEO 标签渲染逻辑

根据 PaperMod 模板（`layouts/partials/head.html`）：

1. **仅生产环境渲染：** Open Graph、Twitter Cards、Schema JSON 仅在 `hugo.IsProduction` 或 `env: production` 时渲染
2. **Meta 标签自动生成：**
   - title: 从 front matter 或页面标题获取
   - description: 优先使用 front matter，其次使用摘要
   - keywords: 优先使用 front matter keywords，其次使用 tags
   - author: 从 partial "author.html" 获取
3. **robots meta:** 生产环境为 `index, follow`，其他环境为 `noindex, nofollow`

## Don't Hand-Roll

| Problem | Don't Build | Use Instead | Why |
|---------|-------------|-------------|-----|
| sitemap.xml 生成 | 自定义 XML 模板 | Hugo 原生 sitemap | Hugo 自动处理，符合 sitemap 协议 v0.9 |
| robots.txt 生成 | 手动创建 static/robots.txt | hugo.yaml enableRobotsTXT | 自动生成，支持配置 |
| Open Graph 标签 | 自定义 head 模板 | PaperMod 内置模板 | 完整支持图片、视频、音频 |
| Twitter Card | 自定义模板 | PaperMod 内置模板 | 自动适配 summary_large_image |
| Schema.org | 自定义 JSON-LD | PaperMod 内置 schema_json | 支持 Article、Website 等类型 |

## Common Pitfalls

### Pitfall 1: SEO 标签在本地开发环境不显示
**What goes wrong:** `hugo server` 本地预览时看不到 Open Graph、Twitter Card 标签
**Why it happens:** PaperMod 仅在生产环境渲染这些标签
**How to avoid:** 使用 `hugo server -E` 或设置 `env: production` 参数
**Warning signs:** 本地测试社交分享卡片显示失败

### Pitfall 2: 社交分享时无预览图
**What goes wrong:** 复制链接到微信/QQ 显示无图片
**Why it happens:** 未配置 cover image 或 front matter 中的 images 列表
**How to avoid:**
1. 在文章 front matter 中添加 `cover.image`
2. 或在 Page Bundle 中添加 feature.jpg/cover.jpg
3. 确保 baseURL 配置正确（绝对 URL）
**Warning signs:** og:image 标签为空

### Pitfall 3: Twitter Card 显示 summary 而非 summary_large_image
**What goes wrong:** Twitter 分享卡片图片较小
**Why it happens:** 未配置 cover image，Twitter Cards 降级为 summary
**How to avoid:** 为每篇文章添加 cover image
**Warning signs:** `<meta name="twitter:card" content="summary">`

### Pitfall 4: sitemap.xml 包含不需要的页面
**What goes wrong:** sitemap 包含 404、tag 页面等
**Why it happens:** 未配置 `disableKinds` 排除不需要的页面类型
**How to avoid:** 在 hugo.yaml 中配置：
```yaml
disableKinds:
  - taxonomy
  - term
  - RSS
  - sitemap
```
**Warning signs:** sitemap 包含过多页面，收录不相关页面

### Pitfall 5: 百度无法收录
**What goes wrong:** 百度爬虫被 robots.txt 阻止
**Why it happens:** 默认 robots.txt 禁止所有爬虫
**How to avoid:** 自定义 robots.txt 允许百度爬虫：
```
User-agent: BaiduSpider
Allow: /

User-agent: *
Disallow:
```

## Code Examples

### 完整 hugo.yaml SEO 配置

```yaml
baseURL: "https://your-domain.com/"
languageCode: "zh-cn"
title: "你的博客标题"
enableRobotsTXT: true

# Sitemap 配置
sitemap:
  changefreq: "weekly"
  priority: 0.5
  filename: "sitemap.xml"

# 禁用不需要的页面类型
disableKinds:
  - taxonomy
  - term
  - RSS

params:
  # 站点描述和关键词
  description: "技术博客 - 分享编程知识和生活思考"
  keywords: ["技术博客", "编程", "Hugo", "PaperMod"]

  # 社交媒体
  social:
    twitter: "@yourhandle"
    # facebook_app_id: "your-facebook-app-id"

  # Favicon 配置
  assets:
    favicon: "favicon.ico"
    favicon32x32: "favicon-32x32.png"
    favicon16x16: "favicon-16x16.png"
    apple_touch_icon: "apple-touch-icon.png"
    theme_color: "#ffffff"

  # Google Search Console 验证
  # analytics:
  #   google:
  #     SiteVerificationTag: "your-google-verification-code"
```

### 自定义 robots.txt 模板

在 `layouts/robots.txt` 创建自定义模板：

```
User-agent: *
Allow: /

Sitemap: {{ "sitemap.xml" | absURL }}

# 百度爬虫
User-agent: BaiduSpider
Allow: /

# 禁止爬取私有内容
Disallow: /search/
Disallow: /tags/
```

### 文章 Front Matter 示例

```yaml
---
title: "Hugo PaperMod SEO 配置指南"
description: "详细介绍如何在 Hugo PaperMod 博客中配置完整的 SEO 元数据，包括 meta 标签、Open Graph、Twitter Card 等。"
keywords: ["Hugo", "PaperMod", "SEO", "静态博客"]
cover:
  image: "images/cover.jpg"
  alt: "SEO 配置封面图"
  caption: "Photo by Unsplash"
  relative: false
date: 2026-03-08
lastmod: 2026-03-08
publishDate: 2026-03-08
tags: ["Hugo", "SEO"]
categories: ["技术教程"]
---
```

## State of the Art

| Old Approach | Current Approach | When Changed | Impact |
|--------------|------------------|--------------|--------|
| 手动创建 SEO 标签 | Hugo 内置 + PaperMod 模板 | Hugo 0.55+ | 自动生成，减少配置工作 |
| 静态 robots.txt | enableRobotsTXT 自动生成 | Hugo 0.65+ | 支持动态配置 |
| 自定义 sitemap.xml | Hugo 原生 sitemap | 一直支持 | 符合标准协议 |

**Deprecated/outdated:**
- 无

## Open Questions

1. **是否需要为每个分类单独配置 SEO？**
   - What we know: Hugo 会自动为每个 section 生成对应的 SEO 标签
   - What's unclear: 是否需要针对 /tech/ 和 /fiction/ 单独配置不同的 meta 描述
   - Recommendation: 在各分类的 _index.md 中配置不同的 description 和 keywords

2. **如何验证 SEO 配置是否正确？**
   - What we know: 可以使用 Google Rich Results Test、Twitter Card Validator
   - What's unclear: 本地开发环境如何验证
   - Recommendation: 使用 `hugo -E` 构建生产版本进行本地测试

3. **是否需要配置百度 sitemap 提交？**
   - What we know: 百度支持 sitemap 提交
   - What's unclear: 是否需要在 robots.txt 中额外配置
   - Recommendation: 保持标准 sitemap.xml，百度会正常抓取

## Validation Architecture

### Test Framework
| Property | Value |
|----------|-------|
| Framework | Hugo built-in |
| Config file | hugo.yaml |
| Quick run command | `hugo -E` (production build) |
| Full suite command | `hugo` (default) |

### Phase Requirements Test Map

| Req ID | Behavior | Test Type | Automated Command | File Exists? |
|--------|----------|-----------|-------------------|-------------|
| SEO-01 | Meta 标签存在于 <head> | Build verification | `hugo -E && grep -r "meta name=\"description\"" public/` | N/A |
| SEO-02 | Open Graph 标签存在 | Build verification | `grep "og:" public/tech/*/index.html | head -5` | N/A |
| SEO-03 | Twitter Card 存在 | Build verification | `grep "twitter:card" public/tech/*/index.html` | N/A |
| SEO-04 | sitemap.xml 存在 | File check | `test -f public/sitemap.xml` | N/A |
| SEO-05 | robots.txt 存在 | File check | `test -f public/robots.txt` | N/A |

### Wave 0 Gaps

- 无 — Hugo 原生支持，无需额外测试基础设施

## Sources

### Primary (HIGH confidence)
- PaperMod Wiki: https://github.com/adityatelange/hugo-PaperMod/wiki/Features - SEO 功能说明
- PaperMod head.html: 模板分析 - Meta 标签生成逻辑
- PaperMod opengraph.html: 模板分析 - Open Graph 标签生成
- PaperMod twitter_cards.html: 模板分析 - Twitter Card 标签生成

### Secondary (MEDIUM confidence)
- Hugo Sitemap 配置: https://gohugo.io/configuration/sitemap/ - sitemap.xml 配置选项
- Hugo Robots.txt: https://gohugo.io/templates/robots/ - robots.txt 配置

## Metadata

**Confidence breakdown:**
- Standard stack: HIGH - Hugo + PaperMod 官方文档确认
- Architecture: HIGH - 模板代码分析确认
- Pitfalls: MEDIUM - 基于社区常见问题总结

**Research date:** 2026-03-08
**Valid until:** 2026-06-08 (PaperMod 和 Hugo 版本稳定)
