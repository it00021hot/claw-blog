# Pitfalls Research

**Domain:** Hugo 静态博客
**Researched:** 2026-03-08
**Confidence:** MEDIUM

## Critical Pitfalls

### Pitfall 1: 直接修改主题文件

**What goes wrong:**
直接修改 `themes/PaperMod` 目录下的文件，导致主题更新后所有自定义修改丢失。维护成本急剧增加，最终不得不 fork 主题或放弃更新。

**Why it happens:**
- Hugo 主题系统的覆盖机制（`layouts/` 目录优先于主题）不被了解
- 初次使用时不知道可以在项目根目录创建同名文件来覆盖主题
- 图方便直接修改主题文件

**How to avoid:**
- 所有自定义内容放在项目根目录的 `layouts/` 目录
- 使用 `hugo server` 调试时确认覆盖生效
- 创建 `assets/` 目录存放自定义 CSS/JS，避免修改主题的 `static/` 目录

**Warning signs:**
- `themes/PaperMod/layouts/` 下的文件被修改
- 提交记录中频繁出现 `themes/` 目录的变更
- 不知道当前显示的布局来自主题还是自定义

**Phase to address:**
- 阶段 1：项目初始化与主题集成

---

### Pitfall 2: 分类体系设计混乱

**What goes wrong:**
- 同一篇文章使用了多个相似的分类维度（如 `categories` 和 `series` 混用）
- Taxonomy 配置与内容组织不匹配
- 分类页面无内容或内容稀疏

**Why it happens:**
- 开始写文章时随意添加分类，没有规划
- 不了解 Hugo 的 `categories`、`tags`、`series` 三种 taxonomy 的语义区别
- 没有预先定义内容组织策略

**How to avoid:**
- 明确三种 taxonomy 的用途：
  - `categories`: 大领域（如「技术」「文学」）
  - `tags`: 具体技术点（如「Hugo」「Go」）
  - `series`: 同一主题的系列文章
- 在 `config.yaml` 中明确配置所有 taxonomy
- 建立内容命名规范

**Warning signs:**
- `config.yaml` 中没有明确 taxonomy 配置
- 多篇文章使用相同但无意义的分类
- 分类页面 URL 访问 404

**Phase to address:**
- 阶段 2：内容分类与列表页

---

### Pitfall 3: SEO 配置不完整

**What goes wrong:**
- 搜索引擎收录不完整，文章无摘要或标题
- 社交媒体分享时显示默认占位符
- `robots.txt` 和 `sitemap.xml` 缺失或配置错误

**Why it happens:**
- 不熟悉 Hugo 的 `_index.md` Front Matter 模板
- 忽略了社交媒体元标签（Open Graph、Twitter Cards）
- 部署到 GitHub Pages 后未验证 robots 规则

**How to avoid:**
- 在 `config.yaml` 中配置完整的 SEO 参数：
  ```yaml
  params:
    description: "博客描述"
    author: "博主名"
  ```
- 每个页面设置 `title`、`description`、`keywords`
- 使用模板函数生成完整的 `<head>` 元标签
- 部署后使用 Google Search Console 验证

**Warning signs:**
- 分享链接到微信/Twitter 时显示不正确的缩略图
- `hugo --printI18nWarnings` 输出缺失翻译警告
- `sitemap.xml` 访问 404

**Phase to address:**
- 阶段 4：SEO 元数据配置

---

### Pitfall 4: 部署配置错误

**What goes wrong:**
- GitHub Actions 构建失败
- 部署后页面 404，尤其是子目录路径问题
- 主题 submodule 未正确初始化

**Why it happens:**
- Hugo 版本与 GitHub Actions 镜像版本不一致
- 忽略 `baseURL` 配置（GitHub Pages 子目录需要完整路径）
- 直接复制他人 workflow 而未理解每步作用

**How to avoid:**
- 明确 `baseURL` 配置（带或不带尾部斜杠）
- 使用 `actions/hugo-setup` 指定明确版本
- 添加 `.gitmodules` 管理主题或直接 clone
- 构建后本地预览 `hugo server --baseURL=https://username.github.io/`

**Warning signs:**
- GitHub Actions 日志显示 "Theme not found"
- 构建成功但页面资源 404
- CSS/JS 文件路径错误

**Phase to address:**
- 阶段 7：GitHub Pages 部署流水线配置

---

### Pitfall 5: 图片与资源路径问题

**What goes wrong:**
- 本地预览正常，部署后图片全挂
- 使用绝对路径 `/images/foo.jpg`，部署到子目录后路径错误
- 引用主题内的资源失败

**Why it happens:**
- 不理解 Hugo 的资源管道和路径解析规则
- 混用项目资源和主题资源
- 部署环境与本地环境的 baseURL 不同

**How to avoid:**
- 使用 Hugo 资源函数：`{{ $image := resources.Get "images/foo.jpg" }}`
- 使用相对路径或模板变量：`{{ .Permalink }}`、`{{ .RelPermalink }}`
- 在 `config.yaml` 中测试不同 `baseURL` 后再部署

**Warning signs:**
- 开发环境图片显示，部署后不显示
- 路径包含重复的目录名
- 资源文件引用使用 `../../` 相对路径

**Phase to address:**
- 阶段 1：项目初始化（资源组织）

---

## Technical Debt Patterns

| Shortcut | Immediate Benefit | Long-term Cost | When Acceptable |
|----------|-------------------|----------------|-----------------|
| 直接修改主题 CSS | 快速看到效果 | 主题更新后样式丢失 | 仅在 MVP 阶段验证布局 |
| 使用外部 CDN 加载资源 | 减少构建时间 | 依赖第三方可用性，中国访问慢 | 明确知晓风险时 |
| 不使用 Git Submodule | 简化 clone 流程 | 主题更新需手动拉取 | 仅单次使用时 |
| 跳过 RSS feed | 减少配置复杂度 | 读者无法订阅 | 永远不应该 |

---

## Integration Gotchas

| Integration | Common Mistake | Correct Approach |
|-------------|----------------|------------------|
| Google AdSense | 广告单元 ID 硬编码在模板中 | 使用 config 参数或环境变量 |
| GitHub Pages | 忽略 .nojekyll 文件 | Hugo 自动处理，确保无冲突 |
| 自定义域名 | HTTPS 未正确配置 | 使用 GitHub Pages 内置 HTTPS |

---

## Performance Traps

| Trap | Symptoms | Prevention | When It Breaks |
|------|----------|------------|----------------|
| 大量图片未优化 | 构建缓慢，页面加载慢 | 使用 Hugo 图像处理管道 | 图片 > 50 张时 |
| 复杂 Shortcode | 构建时间增加 | 减少嵌套，避免过度抽象 | 短代码 > 20 个时 |
| 未使用资源缓存 | 每次构建重新处理资源 | 配置 resource cache | 大量资源文件时 |

---

## Security Mistakes

| Mistake | Risk | Prevention |
|---------|------|------------|
| 暴露 Google AdSense ID | 被恶意点击导致封号 | 使用环境变量，不提交到仓库 |
| 部署 workflow 权限过大 | 潜在供应链攻击 | 最小化 token 权限 |
| 外部链接无安全检查 | 链接到恶意网站 | 验证外链安全性 |

---

## UX Pitfalls

| Pitfall | User Impact | Better Approach |
|---------|-------------|-----------------|
| 无暗色主题 | 夜间阅读刺眼 | PaperMod 原生支持，确保配置生效 |
| 导航层级过深 | 用户迷失 | 保持两级导航，分类页入口清晰 |
| 字体太小/对比度低 | 阅读疲劳 | 遵循 WCAG 可访问性标准 |

---

## "Looks Done But Isn't" Checklist

- [ ] **SEO:** 配置了 title/description，但 social meta tags 未验证
- [ ] **分类:** 在 front matter 添加了 categories，但 taxonomy 页面未创建
- [ ] **主题:** 覆盖了布局，但未验证实际生效（主题 vs 自定义）
- [ ] **部署:** GitHub Actions 绿色通过，但本地 `hugo --printI18nWarnings` 有警告
- [ ] **暗色主题:** config 中配置了 darkMode，但切换按钮未显示
- [ ] **RSS:** 有 feed.xml，但 URL 提交到 RSS 订阅器后内容为空

---

## Recovery Strategies

| Pitfall | Recovery Cost | Recovery Steps |
|---------|---------------|----------------|
| 主题修改丢失 | HIGH | 建立 layouts/ 覆盖，逐一迁移修改 |
| 分类重建 | MEDIUM | 重新规划 taxonomy，迁移所有 front matter |
| 部署失败 | LOW | 检查 workflow 语法，确认 Hugo 版本 |
| SEO 重做 | MEDIUM | 使用爬虫工具审计所有页面，逐页修复 |

---

## Pitfall-to-Phase Mapping

| Pitfall | Prevention Phase | Verification |
|---------|------------------|--------------|
| 直接修改主题文件 | 阶段 1：项目初始化与主题集成 | 确认 `themes/` 目录无修改 |
| 分类体系设计混乱 | 阶段 2：内容分类与列表页 | 访问各 taxonomy 页面 |
| SEO 配置不完整 | 阶段 4：SEO 元数据配置 | 使用 SEO 检查工具 |
| 部署配置错误 | 阶段 7：GitHub Pages 部署 | 验证线上页面资源加载 |
| 图片路径问题 | 阶段 1：项目初始化 | 本地预览 + baseURL 测试 |

---

## Sources

- Hugo 官方文档：https://gohugo.io/documentation/
- PaperMod 主题文档：https://adityatelange.hugopapermod.io/
- GitHub Pages 部署最佳实践
- Hugo 社区常见问题汇总

---

*Pitfalls research for: Hugo 博客项目*
*Researched: 2026-03-08*
