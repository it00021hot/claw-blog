---
phase: 7
slug: https-github-com-mengjian-github-openclaw101
status: draft
nyquist_compliant: false
wave_0_complete: false
created: 2026-03-09
---

# Phase 7 — Validation Strategy

> Per-phase validation contract for feedback sampling during execution.

---

## Test Infrastructure

| Property | Value |
|----------|-------|
| **Framework** | pytest 8.x |
| **Config file** | pytest.ini (or pyproject.toml) |
| **Quick run command** | `pytest tests/ -x -v` |
| **Full suite command** | `pytest tests/ --cov=scripts --cov-report=html` |
| **Estimated runtime** | ~60 seconds |

---

## Sampling Rate

- **After every task commit:** Run `pytest tests/ -x -v`
- **After every plan wave:** Run `pytest tests/ --cov=scripts`
- **Before `/gsd:verify-work`:** Full suite must be green
- **Max feedback latency:** 60 seconds

---

## Per-Task Verification Map

| Task ID | Plan | Wave | Requirement | Test Type | Automated Command | File Exists | Status |
|---------|------|------|-------------|-----------|-------------------|-------------|--------|
| 07-01-01 | 01 | 1 | OCLAW-01 | integration | 复用 Phase 6 测试 | N/A | ⬜ pending |
| 07-01-02 | 01 | 1 | OCLAW-02 | integration | 复用 Phase 6 测试 | N/A | ⬜ pending |
| 07-02-01 | 02 | 1 | OCLAW-03 | unit | `pytest tests/test_openclaw101_fetcher.py -x` | ⬜ W0 | ⬜ pending |
| 07-02-02 | 02 | 1 | OCLAW-04 | unit | `pytest tests/test_typescript_parser.py -x` | ⬜ W0 | ⬜ pending |
| 07-02-03 | 02 | 1 | OCLAW-05 | unit | `pytest tests/test_resource_formatter.py -x` | ⬜ W0 | ⬜ pending |

*Status: ⬜ pending · ✅ green · ❌ red · ⚠️ flaky*

---

## Wave 0 Requirements

- [ ] `tests/test_openclaw101_fetcher.py` — 覆盖 OCLAW-03 (resources.ts 抓取)
- [ ] `tests/test_typescript_parser.py` — 覆盖 OCLAW-04 (TypeScript 解析)
- [ ] `tests/test_resource_formatter.py` — 覆盖 OCLAW-05 (资源转换)

---

## Manual-Only Verifications

| Behavior | Requirement | Why Manual | Test Instructions |
|----------|-------------|------------|-------------------|
| README 内容质量 | OCLAW-01 | 内容质量需要人工判断 | 检查生成的文件内容是否通顺 |
| Issues 转换质量 | OCLAW-02 | Issue 内容质量需要人工判断 | 检查转换后的 Markdown 格式 |
| Hugo 构建成功 | N/A | 需要 hugo 命令验证 | `hugo --quiet --gc` |

*If none: "All phase behaviors have automated verification."*

---

## Validation Sign-Off

- [ ] All tasks have `<automated>` verify or Wave 0 dependencies
- [ ] Sampling continuity: no 3 consecutive tasks without automated verify
- [ ] Wave 0 covers all MISSING references
- [ ] No watch-mode flags
- [ ] Feedback latency < 60s
- [ ] `nyquist_compliant: true` set in frontmatter

**Approval:** pending
