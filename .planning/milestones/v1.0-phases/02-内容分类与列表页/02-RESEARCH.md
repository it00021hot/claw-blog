# Phase 2: 内容分类与列表页 - Research

**Researched:** 2026-03-08
**Domain:** Hugo Sections + PaperMod Theme Configuration
**Confidence:** HIGH

## Summary

本阶段研究如何在 Hugo + PaperMod 博客中实现内容分类与列表页功能。基于用户决策（独立路由 /tech/ 和 /fiction/），需要创建两个独立的 Hugo sections，并在首页整合展示。

**核心发现：**
1. Hugo sections 是内容组织的核心机制，每个 section 目录自动生成对应的列表页
2. PaperMod 主题原生支持 section 列表页，无需自定义模板
3. 首页整合多 section 文章需要使用 Hugo 模板的 `where` 和 `union` 函数
4. 导航菜单通过 hugo.yaml 的 `menu` 配置项统一管理

**Primary recommendation:** 使用 Hugo 原生 sections 机制（content/tech/ 和 content/fiction/），配合 hugo.yaml 菜单配置实现独立路由，首页通过模板合并展示。

## User Constraints (from CONTEXT.md)

### Locked Decisions
- 独立路由：/tech/ 和 /fiction/ 两个独立分类页面
- 卡片式布局（PaperMod 默认）
- 摘要预览模式：标题 + 日期 + 摘要（约100字）+ 分类标签
- 按日期倒序（最新在前）
- 技术文章：tech，短篇小说：fiction

### Claude's Discretion
- 短篇小说可能需要不同的排版（Phase 1 提到的 deferred idea）
- 分类标签需在文章列表和详情页都显示

### Deferred Ideas (OUT OF SCOPE)
- 短篇小说特殊排版（如分章节、字体大小）— 后续优化
- 评论系统 — PROJECT.md 明确 Out of Scope

## Phase Requirements

| ID | Description | Research Support |
|----|-------------|------------------|
| CONT-01 | 技术文章分类目录创建 | Hugo sections 机制，每个目录自动生成列表页 |
| CONT-02 | 短篇小说独立分类目录创建 | 同上，使用不同目录名 |
| CONT-03 | 文章列表页支持双分类展示 | 首页模板使用 union 合并多 section |
| CONT-04 | 分类页面独立路由 | Section 目录自动生成对应路由 |

## Standard Stack

### Core
| Library | Version | Purpose | Why Standard |
|---------|---------|---------|--------------|
| Hugo | 0.120+ | 静态网站生成器 | 内容分类基于 Hugo sections 机制 |
| PaperMod | latest | Hugo 主题 | 原生支持 section 列表页、卡片布局 |

### 实现方式
| 功能 | 实现方法 | 配置位置 |
|------|----------|----------|
| Section 创建 | content/{section}/ 目录 | 目录结构 |
| Section 列表页 | 自动生成 | Hugo 原生 |
| 导航菜单 | menu 配置 | hugo.yaml |
| 分类标签 | front matter categories | 文章 Markdown |
| 首页多 section | union/where 函数 | layouts/index.html |

## Architecture Patterns

### Recommended Project Structure
```
content/
├── posts/              # 技术文章 section (已存在)
│   └── _index.md       # Section 配置
├── fiction/           # 短篇小说 section (已存在)
│   └── _index.md       # Section 配置
└── _index.md          # 首页配置

layouts/
└── index.html         # 首页模板（覆盖默认）

hugo.yaml              # 菜单配置
```

### Pattern 1: Hugo Section 创建
**What:** 创建顶级内容目录，每个目录自动成为独立的 section

**When to use:** 需要独立分类、独立列表页的 content

**Example:**
```bash
# 创建 tech section
content/tech/_index.md

# 创建 fiction section
content/fiction/_index.md
```

**_index.md 模板：**
```yaml
---
title: "技术文章"
description: "技术相关文章列表"
---
```

**Source:** [Hugo Sections Documentation](https://gohugo.io/content-management/sections/)

### Pattern 2: PaperMod 导航菜单配置
**What:** 在 hugo.yaml 中配置顶部导航菜单项

**When to use:** 添加分类页面链接到导航栏

**Example:**
```yaml
menu:
  main:
    - name: 技术文章
      url: /tech/
      weight: 10
    - name: 短篇小说
      url: /fiction/
      weight: 20
    - name: 首页
      url: /
      weight: 5
```

**Source:** [Hugo Configuration - Menu](https://gohugo.io/configuration/menu/)

### Pattern 3: 首页合并多 Section 文章
**What:** 在首页模板中使用 Hugo 模板函数合并多个 section 的文章

**When to use:** 首页需要同时展示技术文章和短篇小说的最新文章

**Example:**
```html
{{/* layouts/index.html */}}
{{/* 合并 posts 和 fiction 两个 section 的文章，按日期倒序 */}}
{{ $posts := where site.RegularPages "Section" "posts" }}
{{ $fiction := where site.RegularPages "Section" "fiction" }}
{{ $all := union $posts $fiction | first 10 }}

{{ range $all }}
  <article class="post-entry">
    <h2><a href="{{ .RelPermalink }}">{{ .Title }}</a></h2>
    <time>{{ .Date.Format "2006-01-02" }}</time>
    <p>{{ .Summary }}</p>
    {{ with .Params.categories }}
      <div class="post-tags">
        {{ range . }}
          <a href="{{ "categories" | relURL }}/{{ . | urlize }}/">{{ . }}</a>
        {{ end }}
      </div>
    {{ end }}
  </article>
{{ end }}
```

**Source:** [Hugo Lists Templates](https://gohugo.io/templates/lists/)

### Pattern 4: Section 列表页显示分类标签
**What:** 在文章卡片中显示分类标签，点击后跳转到分类页面

**When to use:** 需要在列表页显示文章所属分类

**Example:**
```html
{{/* layouts/_default/list.html 或使用 PaperMod 默认 */}}
{{ with .Params.categories }}
  <span class="post-category">
    {{ range $i, $cat := . }}
      {{ if $i }}, {{ end }}
      <a href="{{ "categories" | relURL }}/{{ $cat | urlize }}/">{{ $cat }}</a>
    {{ end }}
  </span>
{{ end }}
```

### Anti-Patterns to Avoid

1. **不要手动创建分类页面**: Hugo 的 taxonomies 会自动生成 /categories/ 页面，不需要手动创建

2. **不要混淆 Section 和 Taxonomy**:
   - Section: 内容目录结构（如 /tech/），用于组织内容
   - Taxonomy: 内容属性分类（如 categories, tags），用于关联内容

3. **不要忘记 _index.md**: 每个 section 需要 _index.md 来定义标题和描述，否则列表页会显示空标题

## Don't Hand-Roll

| Problem | Don't Build | Use Instead | Why |
|---------|-------------|-------------|-----|
| Section 列表页 | 自定义模板 | PaperMod 默认模板 | PaperMod 已内置美观的卡片式列表页 |
| 分类页面 | 手动创建 | Hugo Taxonomies | 自动生成且支持 SEO |
| 日期排序 | 手动实现 | `sort by:"Date" reverse:true` | Hugo 内置且性能更好 |

**Key insight:** Hugo sections 机制是经过大量验证的内容组织方式，PaperMod 主题已针对 section 列表页做了优化设计。

## Common Pitfalls

### Pitfall 1: Section 名称与路由不匹配
**What goes wrong:** 访问 /tech/ 返回 404 或内容为空

**Why it happens:** 目录名称决定 URL，如果 content/tech/ 不存在或为空，Hugo 不会生成对应页面

**How to avoid:**
1. 确保目录名与 URL 一致（tech -> /tech/）
2. 确保目录中有内容文件或 _index.md
3. 运行 `hugo server` 本地预览验证

**Warning signs:** `hugo server` 输出中看不到新创建的 section

### Pitfall 2: 首页只显示一个 Section
**What goes wrong:** 首页只显示技术文章或短篇小说，而不是两者

**Why it happens:** 默认模板只渲染 `site.RegularPages`，会包含所有页面，但没有按需求筛选

**How to avoid:**
1. 覆盖 layouts/index.html 模板
2. 使用 `union` 函数合并多个 section
3. 指定排序方式（日期倒序）

### Pitfall 3: 分类标签链接错误
**What goes wrong:** 点击分类标签跳转到 404 页面

**Why it happens:** 分类页面默认路径是 /categories/{name}/，如果 hugo.yaml 中修改了 taxonomies 配置，路径会变化

**How to avoid:**
1. 保持默认 taxonomies 配置（categories）
2. 或在模板中使用 `relURL` 生成正确路径

### Pitfall 4: Section 列表页样式不一致
**What goes wrong:** /tech/ 和 /fiction/ 页面样式与首页或其他页面不同

**Why it happens:** PaperMod 对 section 列表页使用特定模板，可能与首页模板不同

**How to avoid:**
1. 使用 PaperMod 默认的 section 模板（已内置）
2. 如需自定义，创建 layouts/_default/list.html

## Code Examples

### 示例 1: content/tech/_index.md
```yaml
---
title: "技术文章"
description: "技术相关文章与教程"
---
```

### 示例 2: content/fiction/_index.md
```yaml
---
title: "短篇小说"
description: "原创短篇小说作品"
---
```

### 示例 3: hugo.yaml 菜单配置
```yaml
menu:
  main:
    - name: 首页
      url: /
      weight: 1
    - name: 技术文章
      url: /tech/
      weight: 2
    - name: 短篇小说
      url: /fiction/
      weight: 3
```

### 示例 4: 文章 front matter (示例文章)
```yaml
---
title: "我的第一篇文章"
date: 2026-03-08
categories:
  - 技术文章
tags:
  - Hugo
  - PaperMod
description: "文章摘要..."
---
```

### 示例 5: layouts/index.html (首页多 Section 合并)
```html
{{- define "main" -}}
<main class="post-list">
  {{ $paginator := .Paginate (union (where site.RegularPages "Section" "posts") (where site.RegularPages "Section" "fiction")).ByDate.Reverse }}
  {{ range $paginator.Pages }}
    {{ .Render "post_entry" }}
  {{ end }}
  {{ template "partials/pagination.html" . }}
</main>
{{- end -}}
```

## State of the Art

| Old Approach | Current Approach | When Changed | Impact |
|--------------|------------------|--------------|--------|
| 手动创建分类页面 | Hugo Taxonomies 自动生成 | Hugo 早期版本 | 无需维护额外文件 |
| 单一列表页模板 | Section 列表页原生支持 | PaperMod 内置 | 开箱即用 |
| 静态 HTML 分类页 | 动态合并多 section | Hugo 模板函数 | 灵活配置 |

**Deprecated/outdated:**
- 手动创建分类目录 - 使用 Hugo Taxonomies 代替
- 硬编码导航链接 - 使用 hugo.yaml menu 配置代替

## Open Questions

1. **首页是否需要分页？**
   - 当前方案：使用 `first 10` 限制显示数量
   - 需要确认：当文章数量增多时，是否需要分页功能

2. **分类标签是否需要链接到独立页面？**
   - 当前方案：点击跳转到 /categories/{name}/
   - 备选：点击跳转到 /tech/ 或 /fiction/
   - 建议：保持 Hugo 默认行为，后续可优化

## Validation Architecture

### Test Framework
| Property | Value |
|----------|-------|
| Framework | Hugo Build + Server |
| Config file | hugo.yaml |
| Quick run command | `hugo server -D` |
| Full suite command | `hugo server -D --disableFastRender` |

### Phase Requirements -> Test Map
| Req ID | Behavior | Test Type | Automated Command | File Exists? |
|--------|----------|-----------|-------------------|-------------|
| CONT-01 | 访问 /tech/ 显示技术文章列表 | Smoke | `curl -s http://localhost:1313/tech/ \| grep -q "技术文章"` | N/A (Hugo 自动生成) |
| CONT-02 | 访问 /fiction/ 显示短篇小说列表 | Smoke | `curl -s http://localhost:1313/fiction/ \| grep -q "短篇小说"` | N/A |
| CONT-03 | 首页同时展示两个分类文章 | Smoke | `hugo --quiet && grep -c "tech\\|fiction" public/index.html` | ✅ layouts/index.html |
| CONT-04 | 分类标签链接正确 | Smoke | `curl -s http://localhost:1313/tech/ \| grep -q "/categories/"` | ✅ content/*/_index.md |

### Sampling Rate
- **Per task commit:** `hugo server -D` 本地预览验证
- **Per wave merge:** `hugo --quiet` 构建验证
- **Phase gate:** 本地预览正常 + 构建无警告

### Wave 0 Gaps
- [ ] `content/tech/_index.md` — 定义 tech section
- [ ] `content/fiction/_index.md` — 定义 fiction section
- [ ] `layouts/index.html` — 自定义首页模板合并多 section
- [ ] `hugo.yaml` — 添加导航菜单配置

*(当前 content/posts 和 content/fiction 目录已存在，但 _index.md 文件需要创建)*

## Sources

### Primary (HIGH confidence)
- [Hugo Sections Documentation](https://gohugo.io/content-management/sections/) - Hugo sections 机制官方文档
- [Hugo Lists Templates](https://gohugo.io/templates/lists/) - 列表页模板官方文档
- [Hugo Taxonomies](https://gohugo.io/content-management/taxonomies/) - 分类系统官方文档
- [PaperMod Wiki - Variables](https://github.com/adityatelange/hugo-PaperMod/wiki/Variables) - PaperMod 主题变量

### Secondary (MEDIUM confidence)
- [PaperMod Theme Demo](https://adityatelange.github.io/hugo-PaperMod/) - 主题演示站点

## Metadata

**Confidence breakdown:**
- Standard stack: HIGH - Hugo sections 机制成熟稳定，文档清晰
- Architecture: HIGH - 项目结构符合 Hugo 最佳实践
- Pitfalls: MEDIUM - 基于官方文档和社区经验，部分为推测

**Research date:** 2026-03-08
**Valid until:** 2026-06-08 (Hugo 和 PaperMod 为成熟项目，稳定性高)
