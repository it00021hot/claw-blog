---
phase: 5
slug: 部署流水线
status: draft
nyquist_compliant: false
wave_0_complete: true
created: 2026-03-08
---

# Phase 5 — Validation Strategy

> Per-phase validation contract for feedback sampling during execution.

---

## Test Infrastructure

| Property | Value |
|----------|-------|
| **Framework** | Hugo static build + GitHub Actions |
| **Config file** | .github/workflows/hugo.yaml |
| **Quick run command** | `hugo --buildDrafts` |
| **Full suite command** | `hugo --buildDrafts && echo "Build successful"` |
| **Estimated runtime** | ~5 seconds |

---

## Sampling Rate

- **After every task commit:** Run `hugo --buildDrafts`
- **After every plan wave:** Verify workflow syntax
- **Before `/gsd:verify-work`:** Full build must succeed
- **Max feedback latency:** 10 seconds

---

## Per-Task Verification Map

| Task ID | Plan | Wave | Requirement | Test Type | Automated Command | File Exists | Status |
|---------|------|------|-------------|-----------|-------------------|-------------|--------|
| 05-01-01 | 05-01 | 1 | DEPL-01 | build | `hugo --buildDrafts` | ✅ | ⬜ pending |
| 05-01-02 | 05-01 | 1 | DEPL-01 | file-check | `ls .github/workflows/hugo.yaml` | ✅ | ⬜ pending |
| 05-01-03 | 05-01 | 1 | DEPL-02 | config-verify | Check baseURL in hugo.yaml | ✅ | ⬜ pending |
| 05-02-01 | 05-02 | 2 | DEPL-02 | manual | Human action | N/A | ⬜ pending |
| 05-02-02 | 05-02 | 2 | DEPL-02 | manual | Human action | N/A | ⬜ pending |
| 05-02-03 | 05-02 | 2 | DEPL-03 | manual | Human verification | N/A | ⬜ pending |

*Status: ⬜ pending · ✅ green · ❌ red · ⚠️ flaky*

---

## Wave 0 Requirements

- Existing infrastructure covers all phase requirements.
- Hugo build is the primary verification method

---

## Manual-Only Verifications

| Behavior | Requirement | Why Manual | Test Instructions |
|----------|-------------|------------|-------------------|
| GitHub Pages 部署成功 | DEPL-02 | 需要 GitHub 账户操作 | 推送代码后检查 Actions 运行状态 |
| Cloudflare DNS 生效 | DEPL-03 | 需要 Cloudflare 账户操作 | 访问 https://gen-code.top 验证 |
| HTTPS 证书生效 | DEPL-03 | 需要浏览器验证 | 检查锁形图标 |

---

## Validation Sign-Off

- [ ] All tasks have `<automated>` verify or Wave 0 dependencies
- [ ] Manual verifications have clear test instructions
- [ ] Wave 0 complete (Hugo build works)
- [ ] `nyquist_compliant: true` set in frontmatter

**Approval:** pending
