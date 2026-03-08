# Stack Research

**Domain:** 静态博客 / 个人网站
**Researched:** 2026-03-08
**Confidence:** HIGH

## Recommended Stack

### Core Technologies

| Technology | Version | Purpose | Why Recommended |
|------------|---------|---------|-----------------|
| Hugo | v0.157.0+ | 静态站点生成器 | 纯二进制、无运行时依赖、构建速度极快、社区活跃的事实标准 |
| PaperMod | v7.0+ | Hugo 主题 | 轻量(无 JS 依赖)、SEO 友好、开源活跃、暗亮色主题原生支持 |
| GitHub Pages | - | 静态网站托管 | 免费、无带宽限制、与 GitHub Actions 无缝集成 |
| GitHub Actions | - | CI/CD 流水线 | 免费额度充足、自动构建部署、社区工作流模板成熟 |

### Development Tools

| Tool | Purpose | Notes |
|------|---------|-------|
| Git | 版本控制 | Hugo 项目必需，用于主题 submodule 和部署 |
| VS Code / 任意编辑器 | 内容编辑 | 推荐配合 Markdown 插件 |

### Hugo 扩展功能（如需要）

| Extension | Purpose | When to Use |
|-----------|---------|-------------|
| Hugo Extended | SCSS 转译、图像处理 | 需要自定义样式或图像优化管道时 |

## Installation

```bash
# macOS
brew install hugo

# Linux (Ubuntu/Debian)
sudo apt install hugo

# Windows
choco install hugo-extended -confirm

# 验证安装
hugo version

# 创建新站点
hugo new site my-blog

# 添加 PaperMod 主题 (两种方式)
# 方式 1: Git Submodule (推荐)
git submodule add --depth=1 https://github.com/adityatelange/hugo-PaperMod.git themes/PaperMod

# 方式 2: Hugo Module (需要 Go 1.12+)
hugo mod init github.com/username/my-blog
hugo mod get -u github.com/adityatelange/hugo-PaperMod
```

### 初始化项目结构

```bash
# 目录结构
my-blog/
├── content/          # 文章内容
│   ├── posts/        # 技术文章
│   └── stories/      # 短篇小说
├── layouts/          # 自定义模板
├── static/           # 静态资源 (图片、favicon)
├── themes/           # 主题
│   └── PaperMod/
├── hugo.yaml         # 配置文件 (推荐 YAML)
└── config/_default/  # 默认配置目录
```

## Hugo 配置示例 (hugo.yaml)

```yaml
baseURL: "https://yourdomain.com/"
title: "Your Blog Title"
theme: ["PaperMod"]

defaultContentLanguage: zh-cn
languageCode: zh-cn

params:
  ShowReadingTime: true
  ShowShareButtons: true
  ShowBreadCrumbs: true
  ShowWordCount: true
  ShowCodeCopyButtons: true
  defaultTheme: auto        # auto/dark/light
  disableThemeToggle: false
  profileMode:
    enabled: false
  homeInfoParams:
    Title: "欢迎"
    Content: "技术文章与短篇小说"

menu:
  main:
    - identifier: posts
      name: 文章
      url: /posts/
    - identifier: categories
      name: 分类
      url: /categories/
    - identifier: tags
      name: 标签
      url: /tags/

outputs:
  home:
    - HTML
    - RSS

taxonomies:
  category: categories
  tag: tags
  series: series
```

## GitHub Actions 部署配置

在 `.github/workflows/hugo.yaml` 创建：

```yaml
name: Deploy Hugo Site

on:
  push:
    branches:
      - main

permissions:
  contents: read
  pages: write
  id-token: write

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
        with:
          submodules: true
          fetch-depth: 0

      - name: Setup Hugo
        uses: peaceiris/actions-hugo@v2
        with:
          hugo-version: '0.157.0'
          extended: true

      - name: Build
        run: hugo --minify --baseURL "${{ steps.pages.outputs.base_url }}/"

      - name: Upload artifact
        uses: actions/upload-pages-artifact@v3
        with:
          path: ./public

  deploy:
    needs: build
    runs-on: ubuntu-latest
    environment:
      name: github-pages
      url: ${{ steps.deploy.outputs.page_url }}
    steps:
      - name: Deploy to GitHub Pages
        id: deploy
        uses: actions/deploy-pages@v4
```

## Alternatives Considered

| Recommended | Alternative | When to Use Alternative |
|-------------|-------------|-------------------------|
| Hugo | Jekyll | 已有 Jekyll 项目、Ruby 生态偏好 |
| Hugo | Eleventy (11ty) | 更喜欢 JavaScript/Node.js 生态 |
| PaperMod | LoveIt | 需要更现代化 UI、愿意接受更多 JS 依赖 |
| PaperMod | Terminal | 极简主义者、只需要基础功能 |
| GitHub Pages | Vercel/Netlify | 需要 CDN 全球加速、需要 Serverless Functions |
| GitHub Actions | 手动构建推送 | 简单站点、不需要自动部署 |

## What NOT to Use

| Avoid | Why | Use Instead |
|-------|-----|-------------|
| WordPress | 需要 PHP/MySQL、频繁安全更新、托管成本 | Hugo (纯静态、无维护) |
| Hexo | 主题生态不如 Hugo、更新频率较低 | Hugo |
| 自行搭建评论系统 | 增加复杂度、需要后端存储 | 项目明确 out of scope |
| 第三方搜索服务 (Algolia) | 增加成本、需要维护索引 | 项目明确 out of scope |
| 旧版 Hugo (< 0.120) | 安全漏洞、新功能缺失 | v0.157.0+ |

## Google AdSense 集成

**方法：通过 Hugo partials 注入广告代码**

1. 在 `layouts/partials/` 创建 `adsense.html`：
```html
<script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-8708502478021488"
     crossorigin="anonymous"></script>
<ins class="adsbygoogle"
     style="display:block"
     data-ad-client="ca-pub-8708502478021488"
     data-ad-slot="XXXXXXXXX"
     data-ad-format="auto"
     data-full-width-responsive="true"></ins>
<script>
     (adsbygoogle = window.adsbygoogle || []).push({});
</script>
```

2. 在 `layouts/_default/single.html` 或 `layouts/partials/post_meta.html` 中引入：
```html
{{ partial "adsense.html" . }}
```

## Version Compatibility

| Package | Compatible With | Notes |
|---------|-----------------|-------|
| Hugo Extended | v0.120+ | 推荐使用 Extended 版本以支持 SCSS |
| PaperMod | Hugo v0.120+ | 检查主题 GitHub releases 获取最新兼容版本 |
| actions-hugo | v2+ | 稳定版本 |
| actions/deploy-pages | v3/v4 | v4 推荐 |

## Sources

- [Hugo Official Installation Guide](https://gohugo.io/installation/) — HIGH (官方文档)
- [Hugo GitHub Pages Deployment](https://gohugo.io/hosting-and-deployment/hosting-on-github/) — HIGH (官方文档)
- [PaperMod Theme Documentation](https://adityatelange.github.io/hugo-PaperMod/) — HIGH (官方文档)
- [PaperMod Installation Guide](https://adityatelange.github.io/hugo-PaperMod/posts/papermod/papermod-installation/) — HIGH (官方文档)

---
*Stack research for: Hugo 静态博客搭建*
*Researched: 2026-03-08*
