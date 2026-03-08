---
phase: 6
slug: 内容抓取工具
status: draft
nyquist_compliant: false
wave_0_complete: false
created: 2026-03-08
---

# Phase 6 — Validation Strategy

> Per-phase validation contract for feedback sampling during execution.

---

## Test Infrastructure

| Property | Value |
|----------|-------|
| **Framework** | pytest 8.x |
| **Config file** | pytest.ini (or pyproject.toml) |
| **Quick run command** | `pytest tests/ -x -v` |
| **Full suite command** | `pytest tests/ --cov=scripts --cov-report=html` |
| **Estimated runtime** | ~30 seconds |

---

## Sampling Rate

- **After every task commit:** Run `pytest tests/ -x -v`
- **After every plan wave:** Run `pytest tests/ --cov=scripts`
- **Before `/gsd:verify-work`:** Full suite must be green
- **Max feedback latency:** 30 seconds

---

## Per-Task Verification Map

| Task ID | Plan | Wave | Requirement | Test Type | Automated Command | File Exists | Status |
|---------|------|------|-------------|-----------|-------------------|-------------|--------|
| 06-01-01 | 01 | 1 | FETCH-01 | unit + integration | `pytest tests/test_github_fetcher.py -x` | 需要创建 | ⬜ pending |
| 06-01-02 | 01 | 1 | FETCH-02 | unit | `pytest tests/test_blog_fetcher.py -x` | 需要创建 | ⬜ pending |
| 06-01-03 | 01 | 1 | FETCH-03 | unit (mock) | `pytest tests/test_formatter.py -x` | 需要创建 | ⬜ pending |
| 06-01-04 | 01 | 1 | FETCH-05 | unit | `pytest tests/test_url_store.py -x` | 需要创建 | ⬜ pending |
| 06-01-05 | 01 | 1 | FETCH-06 | integration | `pytest tests/test_cli.py -x` | 需要创建 | ⬜ pending |

*Status: ⬜ pending · ✅ green · ❌ red · ⚠️ flaky*

---

## Wave 0 Requirements

- [ ] `tests/test_github_fetcher.py` — 覆盖 FETCH-01
- [ ] `tests/test_blog_fetcher.py` — 覆盖 FETCH-02
- [ ] `tests/test_formatter.py` — 覆盖 FETCH-03
- [ ] `tests/test_url_store.py` — 覆盖 FETCH-05
- [ ] `tests/test_cli.py` — 覆盖 FETCH-06
- [ ] `pytest.ini` 或 `pyproject.toml` — pytest 配置

*If none: "Existing infrastructure covers all phase requirements."*

---

## Manual-Only Verifications

| Behavior | Requirement | Why Manual | Test Instructions |
|----------|-------------|------------|-------------------|
| GitHub Actions 定时触发 | FETCH-04 | 需要 CI 环境验证 | 手动检查 workflow 文件语法 + 本地测试 cron 表达式 |
| 输出文件格式正确 | FETCH-07 | 需要 Hugo 验证 | 运行 `hugo --quiet` 检查内容是否可解析 |

*If none: "All phase behaviors have automated verification."*

---

## Validation Sign-Off

- [ ] All tasks have `<automated>` verify or Wave 0 dependencies
- [ ] Sampling continuity: no 3 consecutive tasks without automated verify
- [ ] Wave 0 covers all MISSING references
- [ ] No watch-mode flags
- [ ] Feedback latency < 30s
- [ ] `nyquist_compliant: true` set in frontmatter

**Approval:** pending
