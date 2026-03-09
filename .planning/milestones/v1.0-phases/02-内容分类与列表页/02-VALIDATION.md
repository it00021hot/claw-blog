---
phase: 2
slug: 内容分类与列表页
status: draft
nyquist_compliant: false
wave_0_complete: false
created: 2026-03-08
---

# Phase 2 — Validation Strategy

> Per-phase validation contract for feedback sampling during execution.

---

## Test Infrastructure

| Property | Value |
|----------|-------|
| **Framework** | Hugo Build + Server |
| Config file | hugo.yaml |
| Quick run command | `hugo server -D` |
| Full suite command | `hugo server -D --disableFastRender` |
| Estimated runtime | ~5 seconds |

---

## Sampling Rate

- **After every task commit:** Run `hugo server -D` locally and verify pages load
- **After every plan wave:** Run `hugo --quiet` to verify build
- **Before `/gsd:verify-work`:** Full build must pass
- **Max feedback latency:** 10 seconds

---

## Per-Task Verification Map

| Task ID | Plan | Wave | Requirement | Test Type | Automated Command | File Exists | Status |
|---------|------|------|-------------|-----------|-------------------|-------------|--------|
| 02-01-01 | 01 | 1 | CONT-01 | smoke | `curl -s http://localhost:1313/tech/ \| grep -q "技术文章"` | ✅ content/tech/_index.md | ⬜ pending |
| 02-01-02 | 01 | 1 | CONT-02 | smoke | `curl -s http://localhost:1313/fiction/ \| grep -q "短篇小说"` | ✅ content/fiction/_index.md | ⬜ pending |
| 02-01-03 | 01 | 1 | CONT-03 | smoke | `hugo --quiet && grep -c "tech\|fiction" public/index.html` | ✅ layouts/index.html | ⬜ pending |
| 02-01-04 | 01 | 1 | CONT-04 | smoke | `curl -s http://localhost:1313/tech/ \| grep -q "/categories/"` | ✅ hugo.yaml menu | ⬜ pending |

*Status: ⬜ pending · ✅ green · ❌ red · ⚠️ flaky*

---

## Wave 0 Requirements

- [ ] `content/tech/_index.md` — 定义 tech section 标题和描述
- [ ] `content/fiction/_index.md` — 定义 fiction section 标题和描述
- [ ] `layouts/index.html` — 自定义首页模板合并多 section
- [ ] `hugo.yaml` — 添加导航菜单配置

*Note: content/posts/ 和 content/fiction/ 目录已存在（Phase 1），但 _index.md 文件需要创建*

---

## Manual-Only Verifications

| Behavior | Requirement | Why Manual | Test Instructions |
|----------|-------------|------------|-------------------|
| 页面布局美观 | CONT-01, CONT-02 | 视觉检查无法自动化 | 访问 /tech/ 和 /fiction/ 确认卡片式布局显示正确 |
| 分类标签可点击 | CONT-04 | 链接点击测试 | 点击分类标签确认跳转到正确页面 |

---

## Validation Sign-Off

- [ ] All tasks have `<automated>` verify or Wave 0 dependencies
- [ ] Sampling continuity: no 3 consecutive tasks without automated verify
- [ ] Wave 0 covers all MISSING references
- [ ] No watch-mode flags
- [ ] Feedback latency < 10s
- [ ] `nyquist_compliant: true` set in frontmatter

**Approval:** pending
