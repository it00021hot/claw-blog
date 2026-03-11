---
title: "Github Skill - GitHub 操作工具"
date: 2026-03-10T14:20:00+08:00
draft: false
categories: ["开发工具"]
tags: ["Github", "CLI", "开发效率"]
---

## 功能介绍
基于 `gh` CLI 封装的 OpenClaw Skill，支持所有 GitHub 操作：
- Issues 管理（创建、评论、分配、标签）
- PR 管理（查看、合并、审查、CI 状态查询）
- CI/CD 运行日志查看
- 高级 API 调用

## 安装方式
```bash
npx clawhub@latest install github
```

## 使用场景
1. 项目维护：自动处理 issue 和 PR
2. CI 监控：实时查询构建状态
3. 代码审查：批量处理 PR 评论
4. 仓库管理：批量创建/迁移仓库

## 使用教程
### 前置依赖
使用前需要先安装 GitHub CLI：
```bash
# MacOS
brew install gh

# Ubuntu/Debian
sudo apt install gh

# 验证安装
gh --version
```

安装后需要登录授权：
```bash
gh auth login
```

### 常用示例
#### PR 相关操作
1. **查看 PR CI 状态**：
```bash
gh pr checks 55 --repo owner/repo
```

2. **列出最近 10 次工作流运行记录**：
```bash
gh run list --repo owner/repo --limit 10
```

3. **查看运行详情和失败步骤**：
```bash
gh run view <run-id> --repo owner/repo
```

4. **只查看失败步骤的日志**：
```bash
gh run view <run-id> --repo owner/repo --log-failed
```

#### 高级 API 查询
1. **获取指定 PR 的详细信息**：
```bash
gh api repos/owner/repo/pulls/55 --jq '.title, .state, .user.login'
```

2. **列出所有 Issue 并格式化输出**：
```bash
gh issue list --repo owner/repo --json number,title --jq '.[] | "\(.number): \(.title)"'
```

## 评分
⭐ 286 · 下载量 85.8k
作者：@steipete