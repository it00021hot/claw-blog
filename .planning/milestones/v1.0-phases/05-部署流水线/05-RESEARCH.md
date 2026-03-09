# Phase 5: 部署流水线 - Research

**Researched:** 2026-03-08
**Domain:** CI/CD 部署流水线, 域名配置, HTTPS
**Confidence:** HIGH

## Summary

本阶段研究 GitHub Actions 自动部署 Hugo 博客到 GitHub Pages，以及通过 Cloudflare 配置自定义域名和 HTTPS 证书。核心方案已通过官方文档验证：使用 peaceiris/actions-hugo 和 peaceiris/actions-gh-pages 实现自动化构建部署，Cloudflare 通过 CNAME 记录指向 GitHub Pages 并启用代理实现 HTTPS。

**Primary recommendation:** 创建 `.github/workflows/hugo.yaml` 工作流，更新 hugo.yaml 的 baseURL 为 HTTPS，配置 Cloudflare DNS 记录。

---

<user_constraints>
## User Constraints (from CONTEXT.md)

### Locked Decisions
- 使用 GitHub Actions 自动部署
- 部署平台: GitHub Pages
- 域名: gen-code.top
- HTTPS: 通过 Cloudflare 开启

### Claude's Discretion
- GitHub Actions 工作流的具体配置
- Cloudflare 的具体设置方式
- 部署触发条件（push 到 main 分支）

### Deferred Ideas (OUT OF SCOPE)
无
</user_constraints>

---

<phase_requirements>
## Phase Requirements

| ID | Description | Research Support |
|----|-------------|-----------------|
| DEPL-01 | GitHub Actions 工作流创建 | 使用 peaceiris/actions-hugo@v3 + actions-gh-pages@v3 标准方案 |
| DEPL-02 | GitHub Pages 自动部署配置 | 配置 repository settings + DNS 记录 |
| DEPL-03 | 部署后基础验证 | 验证域名解析和 HTTPS 证书 |
</phase_requirements>

---

## Standard Stack

### Core
| Library | Version | Purpose | Why Standard |
|---------|---------|---------|--------------|
| peaceiris/actions-hugo | v3 | Hugo 静态网站构建 | GitHub Marketplace 官方推荐，超 5K stars |
| peaceiris/actions-gh-pages | v3 | GitHub Pages 部署 | 标准部署方案，支持自定义域名 |
| GitHub Actions | - | CI/CD 平台 | 项目已锁定使用 |

### 配置变更
| File | Change | Reason |
|------|--------|--------|
| hugo.yaml | baseURL: https://gen-code.top | HTTPS 要求 |
| .github/workflows/hugo.yaml | 新建 | 自动化部署 |

### Alternatives Considered
| Instead of | Could Use | Tradeoff |
|------------|-----------|----------|
| actions-hugo | 手动安装 Hugo | 额外步骤，版本管理复杂 |
| actions-gh-pages | GitHub 上手动配置 | 不支持自动化触发 |

---

## Architecture Patterns

### Recommended Project Structure
```
.github/
└── workflows/
    └── hugo.yaml          # 部署工作流
```

### Pattern 1: Hugo + GitHub Pages CI/CD
**What:** 使用 GitHub Actions 自动构建并部署 Hugo 站点到 GitHub Pages

**When to use:** Hugo 博客项目，需要自动化部署

**Example:**
```yaml
# Source: https://github.com/marketplace/actions/hugo-setup
name: GitHub Pages

on:
  push:
    branches:
      - main
  pull_request:

jobs:
  deploy:
    runs-on: ubuntu-22.04
    concurrency:
      group: ${{ github.workflow }}-${{ github.ref }}
    steps:
      - uses: actions/checkout@v4
        with:
          submodules: true
          fetch-depth: 0

      - name: Setup Hugo
        uses: peaceiris/actions-hugo@v3
        with:
          hugo-version: '0.119.0'

      - name: Build
        run: hugo --minify

      - name: Deploy
        uses: peaceiris/actions-gh-pages@v3
        if: github.ref == 'refs/heads/main'
        with:
          github_token: ${{ secrets.GITHUB_TOKEN }}
          publish_dir: ./public
```

### Pattern 2: Cloudflare + GitHub Pages 域名配置
**What:** 配置 Cloudflare DNS 记录指向 GitHub Pages

**When to use:** 使用 Cloudflare 作为 DNS 提供商

**DNS Records:**
| Type | Name | Content | Proxy Status |
|------|------|---------|--------------|
| CNAME | www | it00021hot.github.io | Proxied |
| A | @ | 185.199.108.153 | Proxied |
| A | @ | 185.199.109.153 | Proxied |
| A | @ | 185.199.110.153 | Proxied |
| A | @ | 185.199.111.153 | Proxied |

**Source:** [GitHub Docs - Custom Domain](https://docs.github.com/en/pages/configuring-a-custom-domain-for-your-github-pages-site/managing-a-custom-domain-for-your-github-pages-site)

### Anti-Patterns to Avoid
- **未配置 submodules:** PaperMod 主题使用 git submodule 管理，必须设置 `submodules: true`
- **使用 http:// baseURL:** GitHub Pages HTTPS 强制时需要 https://
- **未设置 concurrency:** 并发部署可能导致部署冲突

---

## Don't Hand-Roll

| Problem | Don't Build | Use Instead | Why |
|---------|-------------|-------------|-----|
| Hugo 安装 | 手动下载安装 | peaceiris/actions-hugo | 版本管理、缓存优化 |
| Pages 部署 | 手动 git push | actions-gh-pages | 自动触发、token 管理 |
| DNS 验证 | 自己测试解析 | GitHub 自动验证 | 更可靠 |

**Key insight:** GitHub 官方维护的 Actions 方案已处理版本兼容、缓存、权限等复杂问题，自行实现性价比极低。

---

## Common Pitfalls

### Pitfall 1: Submodule 未正确获取
**What goes wrong:** 构建时找不到 PaperMod 主题，hugo 命令失败
**Why it happens:** 主题通过 git submodule 安装，但工作流未配置 submodules: true
**How to avoid:** 在 checkout action 中添加 `submodules: true`
**Warning signs:** `Error: unable to locate theme directory`

### Pitfall 2: HTTPS 证书问题
**What goes wrong:** 域名访问提示证书无效或安全警告
**Why it happens:** baseURL 使用 http:// 但启用了强制 HTTPS，或 Cloudflare 代理未正确配置
**How to避免:**
1. 更新 hugo.yaml baseURL 为 https://gen-code.top
2. 在 GitHub Pages 设置中启用 "Enforce HTTPS"（等待 24 小时）
3. Cloudflare Proxy 状态设为 "Proxied"

### Pitfall 3: 部署权限问题
**What goes wrong:** Deploy 步骤失败，提示权限不足
**Why it happens:** 未在 workflow 中配置 permissions
**How to avoid:** actions-gh-pages@v3 会自动处理 GITHUB_TOKEN 权限

### Pitfall 4: DNS 解析延迟
**What goes wrong:** 配置完成后域名无法访问
**Why it happens:** DNS 传播需要最多 24 小时
**How to avoid:** 使用 `dig gen-code.top +noall +answer` 验证解析结果

---

## Code Examples

### 更新 hugo.yaml baseURL
```yaml
# 旧
baseURL: "http://gen-code.top"

# 新
baseURL: "https://gen-code.top"
```

### GitHub Pages 自定义域名设置（repository settings）
1. 进入仓库 Settings → Pages
2. 在 "Custom domain" 输入 gen-code.top
3. 勾选 "Enforce HTTPS"
4. 等待证书自动生成（可能需要 24 小时）

### Cloudflare DNS 配置
1. 登录 Cloudflare 控制台
2. 选择对应域名
3. 进入 DNS 设置
4. 添加以下记录：
   - CNAME: www → it00021hot.github.io (Proxied)
   - A: @ → 185.199.108.153 (Proxied)
   - A: @ → 185.199.109.153 (Proxied)
   - A: @ → 185.199.110.153 (Proxied)
   - A: @ → 185.199.111.153 (Proxied)

---

## State of the Art

| Old Approach | Current Approach | When Changed | Impact |
|--------------|------------------|--------------|--------|
| 手动部署 | GitHub Actions 自动化 | 标准实践 | 零手动操作 |
| HTTP | HTTPS 强制 | 2024 年后 | 安全必需 |
| 直接解析 | Cloudflare 代理 | 现代实践 | DDoS 防护 + CDN |

**Deprecated/outdated:**
- peaceiris/actions-hugo@v2: 已弃用，使用 v3

---

## Open Questions

1. **GitHub Pages 仓库权限**
   - What we know: 需要在仓库 Settings 中启用 Pages
   - What's unclear: 用户是否已有 GitHub 仓库
   - Recommendation: 首次创建工作流后指导用户配置仓库

2. **Cloudflare 域名接入**
   - What we know: 域名 gen-code.top 需要转入或 NS 指向 Cloudflare
   - What's unclear: 域名当前注册商
   - Recommendation: 询问用户域名当前状态，或提供 Cloudflare 接入指引

---

## Validation Architecture

### Test Framework
| Property | Value |
|----------|-------|
| Framework | GitHub Actions (CI) |
| Config file | .github/workflows/hugo.yaml |
| Quick run command | `git push origin main` 触发 |
| Full suite command | 同上（全自动） |

### Phase Requirements → Test Map
| Req ID | Behavior | Test Type | Automated Command | File Exists? |
|--------|----------|-----------|-------------------|-------------|
| DEPL-01 | GitHub Actions 工作流 | CI | push 触发 | 需要创建 |
| DEPL-02 | Pages 部署配置 | Manual | 访问域名验证 | - |
| DEPL-03 | HTTPS 证书 | Manual | 浏览器检查 | - |

### Wave 0 Gaps
- `.github/workflows/hugo.yaml` — 创建工作流文件
- `.github` 目录 — 如果不存在需要创建

---

## Sources

### Primary (HIGH confidence)
- [peaceiris/actions-hugo](https://github.com/marketplace/actions/hugo-setup) - Hugo 官方推荐安装方案
- [peaceiris/actions-gh-pages](https://github.com/marketplace/actions/deploy-to-github-pages) - Pages 部署标准方案
- [GitHub Docs - Custom Domain](https://docs.github.com/en/pages/configuring-a-custom-domain-for-your-github-pages-site/managing-a-custom-domain-for-your-github-pages-site) - 域名配置权威指南

### Secondary (MEDIUM confidence)
- [Cloudflare DNS 文档](https://developers.cloudflare.com/dns/) - DNS 配置参考

---

## Metadata

**Confidence breakdown:**
- Standard Stack: HIGH - 官方维护方案，广泛使用
- Architecture: HIGH - 成熟模式，无变化
- Pitfalls: HIGH - 常见问题已记录

**Research date:** 2026-03-08
**Valid until:** 2026-09-08 (6个月，CI/CD 方案稳定)
