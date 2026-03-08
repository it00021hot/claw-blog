# Phase 1: 项目初始化与主题集成 - Research

**Researched:** 2026-03-08
**Domain:** Hugo 静态博客 / PaperMod 主题配置
**Confidence:** HIGH

## Summary

Phase 1 目标是搭建 Hugo 项目基础结构并集成 PaperMod 主题。这是整个博客项目的基石,正确配置可避免后续返工。基于官方文档和社区实践,推荐使用 Hugo Extended 版本(支持 SCSS)、通过 git submodule 安装 PaperMod、使用 hugo.yaml 配置文件。

**Primary recommendation:** 使用 `brew install hugo` 安装 Extended 版本,通过 git submodule 安装 PaperMod 主题,创建基础 hugo.yaml 配置并启用暗色/亮色主题切换功能。

## User Constraints (from CONTEXT.md)

### Locked Decisions
- 使用 Hugo Extended 版本 - 支持 SCSS 编译,PaperMod 主题需要
- 使用 hugo.yaml - 研究推荐,比 toml 更现代
- 使用 git submodule - 便于主题更新维护
- 基础目录结构: content/posts/, content/fiction/, layouts/, static/, assets/
- 暗色/亮色主题使用 PaperMod 原生支持,默认跟随系统设置,支持手动切换
- 代码高亮使用 Hugo 内置 Chroma,配色方案: monokai (暗色) / github (亮色)

### Claude's Discretion
- 本地开发服务器端口(默认 1313)
- 具体的 CSS 自定义样式
- 头像和 favicon 资源

### Deferred Ideas (OUT OF SCOPE)
- 短篇小说特殊排版 - Phase 2 内容分类时考虑
- 评论系统 - PROJECT.md 明确 Out of Scope

## Phase Requirements

| ID | Description | Research Support |
|----|-------------|-----------------|
| BASE-01 | Hugo 项目初始化,生成基础目录结构 | 使用 `hugo new site` 命令创建项目 |
| BASE-02 | PaperMod 主题正确集成 | 使用 git submodule 安装到 themes/PaperMod |
| BASE-03 | hugo.yaml 配置文件创建并基础配置 | 配置 theme、params、markup 等 |
| THEM-01 | 暗色/亮色主题切换功能 | PaperMod 原生支持,通过 defaultTheme 参数配置 |
| THEM-02 | 响应式布局适配 | PaperMod 内置响应式设计 |
| THEM-03 | 代码高亮样式 | Hugo Chroma 高亮,支持多配色方案 |

## Standard Stack

### Core

| Library | Version | Purpose | Why Standard |
|---------|---------|---------|--------------|
| Hugo Extended | latest (v0.157+) | 静态站点生成器 | 纯二进制、无运行时依赖、构建速度极快,Extended 支持 SCSS |
| PaperMod | v7.0+ | Hugo 主题 | 轻量(无 JS 依赖)、SEO 友好、暗亮色主题原生支持 |

### Supporting

| Library | Version | Purpose | When to Use |
|---------|---------|---------|-------------|
| Git | - | 版本控制和 submodule 管理 | 主题安装和更新必需 |

### Installation

```bash
# 安装 Hugo Extended (macOS)
brew install hugo

# 验证安装
hugo version

# 创建新站点
hugo new site claw-blog

# 进入站点目录
cd claw-blog

# 使用 git submodule 安装 PaperMod
git submodule add --depth=1 https://github.com/adityatelange/hugo-PaperMod.git themes/PaperMod

# 更新 submodule
git submodule update --init --recursive
```

## Architecture Patterns

### Recommended Project Structure

```
claw-blog/
├── assets/           # 资源管道 (CSS, JS, images)
├── content/          # 内容文件
│   ├── posts/        # 技术文章
│   └── fiction/     # 短篇小说
├── layouts/         # 自定义模板 (覆盖主题)
│   ├── _default/    # 默认模板
│   └── partials/    # 部分模板
├── static/          # 静态资源 (favicon, images)
├── themes/          # 主题目录
│   └── PaperMod/   # PaperMod 主题 (git submodule)
├── hugo.yaml        # 站点配置文件
└── config/          # 环境配置 (可选)
```

### Pattern 1: Hugo 配置覆盖机制
**What:** Hugo 使用"层叠"配置,项目根目录的配置优先级高于主题配置
**When to use:** 需要自定义主题默认行为时
**Example:**
```yaml
# hugo.yaml
baseURL: "https://example.org/"
languageCode: "zh-cn"
title: "我的技术博客"
theme: ["PaperMod"]

# 启用 JSON 输出 (搜索功能需要)
outputs:
  home:
    - HTML
    - RSS
    - JSON

# 主题参数
params:
  defaultTheme: auto
  ShowReadingTime: true
  ShowCodeCopyButtons: true
```

### Pattern 2: 模板覆盖机制
**What:** 在项目 layouts/ 目录中创建同名文件即可覆盖主题模板
**When to use:** 自定义主题组件而不修改主题源码
**Example:**
```
# 覆盖主题的 footer
layouts/partials/footer.html
```

### Pattern 3: 暗色/亮色主题切换
**What:** PaperMod 原生支持通过 CSS variables 和 JavaScript 切换主题
**When to use:** 用户需要手动切换或跟随系统设置
**Configuration:**
```yaml
params:
  defaultTheme: auto  # light, dark, 或 auto (跟随系统)
  # disableThemeToggle: true  # 禁用切换按钮
```

### Pattern 4: 代码高亮配置
**What:** Hugo 使用 Chroma 进行代码高亮,支持多种配色方案
**When to Use:** 技术博客需要代码展示
**Configuration:**
```yaml
markup:
  highlight:
    noClasses: false  # 启用外部 CSS 类
    style: monokai    # 默认暗色主题配色
```
**生成样式文件:**
```bash
# 生成暗色主题样式
hugo gen chromastyles --style=monokai > assets/css/syntax-dark.css

# 生成亮色主题样式
hugo gen chromastyles --style=github > assets/css/syntax-light.css
```

## Don't Hand-Roll

| Problem | Don't Build | Use Instead | Why |
|---------|-------------|-------------|-----|
| 主题安装 | 下载 zip 包 | git submodule | 便于后续主题更新,保留版本控制 |
| 代码高亮 | 手动实现高亮 | Hugo Chroma | 内置支持 100+ 语言,性能好 |
| 暗色主题 | 手写 CSS 变量 | PaperMod 原生支持 | 已实现主题切换逻辑 |
| RSS 订阅 | 手动创建 XML | Hugo 内置输出 | 自动生成,SEO 友好 |

**Key insight:** Hugo + PaperMod 是成熟的静态博客方案,主题和内置功能已解决大多数常见需求,不应重复造轮子。

## Common Pitfalls

### Pitfall 1: 直接修改主题源码
**What goes wrong:** 主题更新后所有自定义修改丢失
**Why it happens:** 将 PaperMod 主题文件当作自己代码的一部分修改
**How to avoid:** 所有自定义放在项目根目录的 layouts/ 目录,使用 Hugo 的覆盖机制
**Warning signs:** themes/PaperMod 目录中有你修改过的文件

### Pitfall 2: 配置文件格式错误
**What goes wrong:** Hugo 无法启动,提示配置解析错误
**Why it happens:** YAML 缩进错误、非法字符、参数名拼写错误
**How to avoid:** 使用 `hugo config` 命令验证配置,注意 YAML 缩进
**Warning signs:** `hugo server` 启动失败,错误信息包含 "failed to resolve"

### Pitfall 3: 资源路径问题
**What goes wrong:** 本地预览正常,部署后资源 404
**Why it happens:** 使用绝对路径或硬编码路径
**How to avoid:** 使用 Hugo 资源函数,相对路径引用
**Warning signs:** static/ 目录中的文件在本地可访问但部署后不可用

### Pitfall 4: 主题未正确加载
**What goes wrong:** 页面不显示主题样式,使用的是默认 HTML
**Why it happens:** 主题未在配置中声明或 submodule 未正确初始化
**How to avoid:** 确认 hugo.yaml 中有 `theme: ["PaperMod"]`,运行 `git submodule update --init`
**Warning signs:** 页面无样式,控制台无 CSS 加载

## Code Examples

### 基础 hugo.yaml 配置

```yaml
# Source: Hugo Official Documentation
baseURL: "https://yourusername.github.io/"
languageCode: "zh-cn"
title: "我的技术博客"
theme: ["PaperMod"]

# 启用 JSON 输出 (搜索功能需要)
outputs:
  home:
    - HTML
    - RSS
    - JSON

# 站点元数据
defaultContentLanguage: zh-cn
defaultContentLanguageInSubdir: false

# 分类配置
taxonomies:
  category: categories
  tag: tags
  series: series

# 主题参数
params:
  # 主题设置
  defaultTheme: auto
  # disableThemeToggle: true

  # 社交链接
  socialIcons:
    - name: github
      url: "https://github.com/yourusername"
    - name: twitter
      url: "https://twitter.com/yourusername"

  # 功能开关
  ShowReadingTime: true
  ShowCodeCopyButtons: true
  ShowShareButtons: true
  ShowBreadCrumbs: true
  ShowPostNavLinks: true

  # 文章编辑链接
  editPost:
    URL: "https://github.com/yourusername/claw-blog/content"
    Text: "编辑此页"
    appendFilePath: true

  # 封面图设置
  cover:
    responsiveImages: false
    linkFullImages: true

  # 搜索配置
  fuseOpts:
    isCaseSensitive: false
    shouldSort: true
    location: 0
    distance: 1000
    threshold: 0.4
    minMatchCharLength: 0
    keys: ["title", "permalink", "summary", "content"]

# 代码高亮配置
markup:
  highlight:
    noClasses: false
    style: monokai
  tableOfContents:
    level: [2, 3]
    ordered: false 快速```

###
命令验证

```bash
# 启动本地开发服务器
hugo server -D

# 验证配置
hugo config

# 列出所有页面
hugo --quiet --printUnusedTemplates

# 构建站点
hugo --gc --minify
```

## State of the Art

| Old Approach | Current Approach | When Changed | Impact |
|--------------|------------------|--------------|--------|
| config.toml | hugo.yaml | Hugo v0.110+ | YAML 更易读,官方推荐 |
| 下载主题 zip | git submodule | 长期维护必备 | 简化主题更新流程 |
| Highlight.js | Hugo Chroma | Hugo 内置 | 无需 JS 依赖,构建速度更快 |
| 手动主题切换 | PaperMod 原生支持 | PaperMod v7.0 | 更可靠的主题切换 |

**Deprecated/outdated:**
- config.toml: 官方已转向 hugo.yaml,新项目应使用 YAML
- 手动下载主题: 无法便捷获取更新

## Open Questions

1. **本地服务器端口**
   - What we know: 默认 1313,可通过 `-p` 参数修改
   - What's unclear: 是否需要持久化配置
   - Recommendation: 使用 CLI 参数,无需配置

2. **头像和 favicon 资源**
   - What we know: 应放在 static/ 目录
   - What's unclear: 具体文件路径和尺寸规格
   - Recommendation: Phase 2 或 Phase 3 再添加,先确保基础功能正常

3. **CSS 自定义样式范围**
   - What we know: 可在 assets/ 创建 custom.css 覆盖
   - What's unclear: 需要何种程度的自定义
   - Recommendation: Phase 3 再处理,Phase 1 先确保主题正常工作

## Validation Architecture

> Skip this section entirely if workflow.nyquist_validation is explicitly set to false in .planning/config.json. If the key is absent, treat as enabled.

### Test Framework
| Property | Value |
|----------|-------|
| Framework | Hugo 内置验证 |
| Config file | hugo.yaml |
| Quick run command | `hugo server -D` |
| Full suite command | `hugo --gc --minify` |

### Phase Requirements -> Test Map
| Req ID | Behavior | Test Type | Automated Command | File Exists? |
|--------|----------|-----------|-------------------|-------------|
| BASE-01 | Hugo 项目初始化 | Manual | `hugo new site .` | ✅ |
| BASE-02 | PaperMod 主题集成 | Manual | `ls themes/PaperMod` | ✅ |
| BASE-03 | hugo.yaml 创建 | Manual | `hugo config` | ✅ |
| THEM-01 | 主题切换功能 | Manual | 浏览器测试 | ❌ |
| THEM-02 | 响应式布局 | Manual | 浏览器测试 | ❌ |
| THEM-03 | 代码高亮 | Manual | `hugo gen chromastyles` | ❌ |

### Sampling Rate
- **Per task commit:** `hugo server -D` 验证本地预览
- **Per wave merge:** `hugo --gc --minify` 验证构建
- **Phase gate:** Full build success before `/gsd:verify-work`

### Wave 0 Gaps
- [ ] 无 - Hugo 项目验证通过 CLI 完成,无需额外测试框架

*(Hugo 项目通过内置命令验证,无需额外的测试框架)*

## Sources

### Primary (HIGH confidence)
- [Hugo Official Documentation](https://gohugo.io/documentation/) - 官方文档,安装和配置的核心来源
- [Hugo Installation - macOS](https://gohugo.io/installation/macos/) - Extended 版本安装指南
- [PaperMod Wiki - Installation](https://github.com/adityatelange/hugo-PaperMod/wiki/Installation) - 主题安装指南
- [PaperMod Wiki - Features](https://github.com/adityatelange/hugo-PaperMod/wiki/Features) - 主题配置选项

### Secondary (MEDIUM confidence)
- [Hugo Syntax Highlighting](https://gohugo.io/content-management/syntax-highlighting/) - Chroma 代码高亮配置
- [PaperMod GitHub Repository](https://github.com/adityatelange/hugo-PaperMod) - 主题源码和 issues

### Tertiary (LOW confidence)
- 社区讨论和博客文章 - 补充参考,未逐一验证

## Metadata

**Confidence breakdown:**
- Standard stack: HIGH - 基于官方文档和社区共识
- Architecture: HIGH - Hugo 架构文档详尽,模式成熟
- Pitfalls: MEDIUM - 社区经验总结,部分为推断

**Research date:** 2026-03-08
**Valid until:** 90 天 (Hugo 和 PaperMod 都是成熟稳定的项目)
