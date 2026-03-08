---
phase: 4
slug: 广告变现接入
status: draft
nyquist_compliant: false
wave_0_complete: false
created: 2026-03-08
---

# Phase 4 — Validation Strategy

> Per-phase validation contract for feedback sampling during execution.

---

## Test Infrastructure

| Property | Value |
|----------|-------|
| **Framework** | Hugo Build + Server |
| Config file | hugo.yaml |
| Quick run command | `hugo -E && grep -r "googlesyndication" public/` |
| Full suite command | `hugo -E --quiet` |
| Estimated runtime | ~5 seconds |

---

## Sampling Rate

- **After every task commit:** Run `hugo -E` locally and verify AdSense script loads
- **After every plan wave:** Run `hugo -E --quiet` to verify build
- **Before `/gsd:verify-work`:** Full build must pass
- **Max feedback latency:** 10 seconds

---

## Per-Task Verification Map

| Task ID | Plan | Wave | Requirement | Test Type | Automated Command | File Exists | Status |
|---------|------|------|-------------|-----------|-------------------|-------------|--------|
| 04-01-01 | 01 | 1 | AD-01 | smoke | `grep -q "googlesyndication" public/index.html` | ✅ layouts/partials/extend_head.html | ⬜ pending |
| 04-01-02 | 01 | 1 | AD-02 | smoke | `grep -q "adsbygoogle" public/tech/hello-world/index.html` | ✅ layouts/partials/extend_head.html | ⬜ pending |
| 04-01-03 | 01 | 1 | AD-01 | smoke | `test -f static/ads.txt` | ✅ static/ads.txt | ⬜ pending |

*Status: ⬜ pending · ✅ green · ❌ red · ⚠️ flaky*

---

## Wave 0 Requirements

- [ ] `layouts/partials/extend_head.html` — AdSense 脚本注入
- [ ] `static/ads.txt` — AdSense 验证文件
- [ ] 验证广告脚本在页面中正确加载

---

## Manual-Only Verifications

| Behavior | Requirement | Why Manual | Test Instructions |
|----------|-------------|------------|-------------------|
| 广告实际展示 | AD-01, AD-02 | 需要浏览器渲染 | 访问网站确认广告显示正常 |
| 广告不影响阅读 | AD-02 | 视觉检查 | 确认广告不遮挡内容 |

---

## Validation Sign-Off

- [ ] All tasks have `<automated>` verify or Wave 0 dependencies
- [ ] Sampling continuity: no 3 consecutive tasks without automated verify
- [ ] Wave 0 covers all MISSING references
- [ ] No watch-mode flags
- [ ] Feedback latency < 10s
- [ ] `nyquist_compliant: true` set in frontmatter

**Approval:** pending
