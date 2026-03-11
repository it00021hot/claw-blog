---
title: "Self-Improving Agent Skill - 自进化代理"
date: 2026-03-10T14:20:00+08:00
draft: false
categories: ["AI 代理"]
tags: ["自学习", "Agent", "效率提升"]
---

## 功能介绍
自动捕获操作错误、用户纠正和使用反馈，实现代理能力的持续进化：
- 错误自动学习，避免重复踩坑
- 用户偏好自动记录，适配使用习惯
- 操作日志自动总结，提炼最佳实践
- 支持 WAL 协议和自主 Cron 调度

## 安装方式
### 方式1：安装到当前工作区（默认）
```bash
npx clawhub@latest install self-improving-agent
```
安装路径：`~/.openclaw/workspace/skills/self-improving-agent

### 方式2：全局安装（所有工作区可用
```bash
npx clawhub@latest install self-improving-agent --global
```
安装路径：`~/.openclaw/skills/self-improving-agent

## 使用场景
1. 日常操作自动化优化
2. 错误处理流程自动迭代
3. 用户交互体验持续提升
4. 代理能力自主进化

## 使用教程
### 前置准备
1. 安装完成后，先创建学习日志目录：
```bash
mkdir -p ~/.openclaw/workspace/.learnings
```

2. 在目录下创建三个日志文件：
```bash
# 学习记录
touch ~/.openclaw/workspace/.learnings/LEARNINGS.md
# 错误记录
touch ~/.openclaw/workspace/.learnings/ERRORS.md
# 功能需求记录
touch ~/.openclaw/workspace/.learnings/FEATURE_REQUESTS.md
```

### 核心工作流程
| 场景 | 操作 |
|------|------|
| 命令/操作失败 | 记录到 `.learnings/ERRORS.md` |
| 用户纠正了你的错误 | 记录到 `.learnings/LEARNINGS.md`，分类为 `correction` |
| 用户提出新功能需求 | 记录到 `.learnings/FEATURE_REQUESTS.md` |
| 外部 API/工具调用失败 | 记录到 `.learnings/ERRORS.md`，附带集成详情 |
| 发现知识过时 | 记录到 `.learnings/LEARNINGS.md`，分类为 `knowledge_gap` |
| 找到更好的实现方案 | 记录到 `.learnings/LEARNINGS.md`，分类为 `best_practice` |

### 日志格式示例
#### 学习记录 (LEARNINGS.md)
```markdown
## [LRN-20260310-001] correction
**Logged**: 2026-03-10T14:30:00+08:00
**Priority**: medium
**Status**: pending
**Area**: workflow

### Summary
用户纠正了安装命令的拼写错误，正确命令是 `npx clawhub` 不是 `npx clawdhub`。

### Details
之前的文档里误写了 clawhub 的命令为 clawdhub，导致用户安装失败。正确的命令前缀是 clawhub。

### Suggested Action
修改所有文档里的错误拼写，后续使用时注意命令正确性。

### Metadata
- Source: user_feedback
- Related Files: content/skills/*.md
- Tags: cli, documentation
```

#### 错误记录 (ERRORS.md)
```markdown
## [ERR-20260310-001] github_cli
**Logged**: 2026-03-10T14:35:00+08:00
**Priority**: high
**Status**: pending
**Area**: tools

### Summary
调用 gh pr checks 命令失败，提示未授权。

### Error
```
gh: authentication failed
```

### Context
尝试查询 PR #55 的 CI 状态，未登录 GitHub 账号。

### Suggested Fix
运行 `gh auth login` 完成授权。
```

### 高级配置：启用自动触发钩子
1. 先创建 OpenClaw 钩子目录（默认不存在需要手动创建）：
```bash
mkdir -p ~/.openclaw/hooks
```

2. 复制钩子文件到 OpenClaw 钩子目录（根据安装方式选择对应命令）：
```bash
# 如果是安装到当前工作区（默认安装方式）
cp -r ~/.openclaw/workspace/skills/self-improving-agent/hooks/openclaw ~/.openclaw/hooks/self-improvement

# 如果是全局安装（加了--global参数）
cp -r ~/.openclaw/skills/self-improving-agent/hooks/openclaw ~/.openclaw/hooks/self-improvement
```

3. 启用钩子：
```bash
openclaw hooks enable self-improvement
```

启用后，每次会话开始和工具调用后会自动提醒你记录学习和错误。

### 知识晋升规则
当学习内容具有普遍适用性时，可以晋升到工作区的核心配置文件：
| 学习类型 | 晋升目标文件 |
|----------|--------------|
| 行为模式、沟通风格 | SOUL.md |
| 工作流、自动化规则 | AGENTS.md |
| 工具使用技巧、坑点 | TOOLS.md |
| 项目规范、约定 | MEMORY.md |

## 评分
⭐ 1.6k · 下载量 137k
作者：@pskoett