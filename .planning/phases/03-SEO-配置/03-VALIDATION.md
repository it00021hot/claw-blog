---
phase: 3
slug: SEO-配置
status: draft
nyquist_compliant: false
wave_0_complete: false
created: 2026-03-08
---

# Phase 3 — Validation Strategy

> Per-phase validation contract for feedback sampling during execution.

---

## Test Infrastructure

| Property | Value |
|----------|-------|
| **Framework** | Hugo Build + Server |
| Config file | hugo.yaml |
| Quick run command | `hugo -E && grep -r "meta" public/` |
| Full suite command | `hugo -E --quiet` |
| Estimated runtime | ~5 seconds |

---

## Sampling Rate

- **After every task commit:** Run `hugo -E` locally and verify SEO tags render
- **After every plan wave:** Run `hugo -E --quiet` to verify build
- **Before `/gsd:verify-work`:** Full build must pass
- **Max feedback latency:** 10 seconds

---

## Per-Task Verification Map

| Task ID | Plan | Wave | Requirement | Test Type | Automated Command | File Exists | Status |
|---------|------|------|-------------|-----------|-------------------|-------------|--------|
| 03-01-01 | 01 | 1 | SEO-01 | smoke | `curl -s http://localhost:1313/tech/hello-world/ \| grep -q "meta"` | ✅ hugo.yaml | ⬜ pending |
| 03-01-02 | 01 | 1 | SEO-02 | smoke | `grep -q "og:" public/tech/hello-world/index.html` | ✅ hugo.yaml | ⬜ pending |
| 03-01-03 | 01 | 1 | SEO-03 | smoke | `grep -q "twitter:" public/tech/hello-world/index.html` | ✅ hugo.yaml | ⬜ pending |
| 03-01-04 | 01 | 1 | SEO-04 | smoke | `test -f public/sitemap.xml` | ✅ hugo.yaml | ⬜ pending |
| 03-01-05 | 01 | 1 | SEO-05 | smoke | `test -f public/robots.txt` | ✅ hugo.yaml | ⬜ pending |

*Status: ⬜ pending · ✅ green · ❌ red · ⚠️ flaky*

---

## Wave 0 Requirements

- [ ] `hugo.yaml` — 添加 SEO 相关配置（enableRobotsTXT, sitemap, params）
- [ ] 更新示例文章 front matter — 添加 description, keywords, cover image
- [ ] 验证 SEO 标签在生产环境渲染

---

## Manual-Only Verifications

| Behavior | Requirement | Why Manual | Test Instructions |
|----------|-------------|------------|-------------------|
| 社交分享预览 | SEO-02 | 需要实际分享到微信/QQ 验证 | 使用 https://socialsharepreview.com/ 测试 |
| Twitter Card 预览 | SEO-03 | 需要实际分享到 Twitter 验证 | 使用 https://cards-dev.twitter.com/validator 测试 |

---

## Validation Sign-Off

- [ ] All tasks have `<automated>` verify or Wave 0 dependencies
- [ ] Sampling continuity: no 3 consecutive tasks without automated verify
- [ ] Wave 0 covers all MISSING references
- [ ] No watch-mode flags
- [ ] Feedback latency < 10s
- [ ] `nyquist_compliant: true` set in frontmatter

**Approval:** pending
