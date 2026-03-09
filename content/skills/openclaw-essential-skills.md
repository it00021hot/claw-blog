---
title: "OpenClaw 必备 Skills 清单：2026 年最值得安装的 10 个技能"
date: 2026-03-09T08:05:00+08:00
categories: ["Skills解读"]
tags: ["OpenClaw", "Skills", "MCP", "插件生态"]
draft: false
---

## 什么是 OpenClaw Skill

OpenClaw Skill 是可以插件式安装到你的 AI Agent 上的能力扩展模块。安装 Skill 之后，OpenClaw 就获得了该 Skill 所赋予的工具——例如，安装了 `browser-use` 之后，你可以直接让 Agent 打开网页、点击按钮、截图；安装了 `calendar` 之后，Agent 可以查询和创建你的日程事件。

Skills 的底层协议基于 **MCP（Model Context Protocol）**——一个由 Anthropic 主导设计的开放标准，用于规范化 AI 模型与外部工具之间的通信方式。MCP 定义了工具描述、调用格式和返回值结构，使得不同厂商开发的 Skill 可以无缝集成到任何兼容 MCP 的 Agent 框架中。OpenClaw 完全兼容 MCP，因此你不仅可以使用官方 Skills，还可以安装社区开发的第三方 Skill，甚至自己编写。

与传统的插件系统不同，MCP 的优势在于 **工具描述对 LLM 可读**——AI 模型能够理解每个工具的功能和参数，从而智能地决定何时调用、如何调用，而无需你手动触发。

---

## 如何安装 Skill

OpenClaw 提供了统一的 Skill 管理命令，安装、卸载、列出 Skill 都非常简单：

```bash
# 安装一个 Skill
openclaw skill add <skill-name>

# 列出已安装的 Skills
openclaw skill list

# 查看某个 Skill 的详细信息
openclaw skill info <skill-name>

# 卸载一个 Skill
openclaw skill remove <skill-name>

# 更新所有 Skill 到最新版本
openclaw skill update --all
```

安装完 Skill 后，重启 OpenClaw（或运行 `openclaw reload`），Agent 即可立即使用新的工具能力。

---

## 推荐清单：10 个必装 Skills

### 1. memory — 长期记忆管理

**用途：** 让 Agent 在对话结束后保留记忆，下次对话时自动回忆相关内容，实现真正的"懂你"AI。

```bash
openclaw skill add memory
```

**功能特性：**
- 自动提取对话中的关键事实并存储
- 按时间和语义双重索引，检索准确
- 支持手动添加、编辑和删除记忆条目

**使用示例：**
```
你：我住在北京，平时用 Mac，主要写 Python 后端。
（之后的对话中，Agent 会自动记住这些信息并在合适时引用）

你：帮我推荐一个本地开发工具。
Agent：考虑到你用 Mac 做 Python 开发，推荐安装 Homebrew 并使用 pyenv 管理 Python 版本……
```

---

### 2. browser-use — 网页浏览与截图

**用途：** 让 Agent 像真人一样操控浏览器，可以打开网页、填写表单、点击按钮、提取内容和截图。

```bash
openclaw skill add browser-use
```

**功能特性：**
- 基于 Playwright，支持 Chromium / Firefox / WebKit
- 自动处理 JavaScript 渲染的动态页面
- 可截图、提取文本、监控页面变化

**使用示例：**
```
你：去 Hacker News 首页，找出今天点赞数最高的 5 篇文章，总结它们的主题。
```

---

### 3. code-interpreter — 本地代码执行

**用途：** 让 Agent 在沙箱环境中编写并执行 Python / JavaScript / Shell 代码，获取真实运行结果。

```bash
openclaw skill add code-interpreter
```

**功能特性：**
- 隔离的代码执行沙箱，安全可控
- 支持 Python、Node.js、Shell 脚本
- 可安装依赖、读写文件、处理数据

**使用示例：**
```
你：用 Python 分析这份 CSV 数据，计算每个类别的平均值和标准差，画出分布图。
```

---

### 4. file-manager — 文件读写管理

**用途：** 赋予 Agent 读取、写入、移动、搜索本地文件和目录的能力。

```bash
openclaw skill add file-manager
```

**功能特性：**
- 读写文本文件（Markdown、代码、配置等）
- 批量文件操作（重命名、移动、复制）
- 目录树遍历与文件搜索

**安全配置（推荐）：**

安装后建议在 `~/.openclaw/config.yaml` 中限制可访问目录：

```yaml
skills:
  file-manager:
    allowed_dirs:
      - ~/Documents
      - ~/Projects
    forbidden_dirs:
      - ~/.ssh
      - ~/Library
```

**使用示例：**
```
你：在 ~/Documents/notes 目录下，把所有文件名包含"2025"的 Markdown 文件移动到 ~/Documents/archive/2025/ 文件夹。
```

---

### 5. web-search — 网页搜索集成

**用途：** 让 Agent 实时搜索互联网，获取最新信息，突破 LLM 知识截止日期的限制。

```bash
openclaw skill add web-search
```

支持多种搜索 API 后端（选择一个配置 API Key）：

```bash
# 使用 Tavily（推荐，专为 AI 优化）
openclaw config set skills.web-search.provider tavily
openclaw config set skills.web-search.apiKey "tvly-your-key"

# 使用 Serper（Google 搜索代理）
openclaw config set skills.web-search.provider serper
openclaw config set skills.web-search.apiKey "your-serper-key"

# 使用 DuckDuckGo（免费，无需 API Key）
openclaw config set skills.web-search.provider duckduckgo
```

**使用示例：**
```
你：搜索最近一周关于 GPT-5 发布的最新消息，整理成摘要。
```

---

### 6. calendar — 日历集成

**用途：** 让 Agent 读取和创建你的日历事件，实现日程管理自动化。

```bash
openclaw skill add calendar
```

**支持的日历服务：**
- Google Calendar（需要 OAuth 授权）
- Microsoft Outlook / Exchange
- Apple Calendar（macOS 本地）
- CalDAV 通用协议

**配置 Google Calendar：**

```bash
openclaw skill configure calendar
# 按提示完成 Google OAuth 授权流程
```

**使用示例：**
```
你：下周三下午 3 点帮我创建一个"产品需求评审"会议，时长 90 分钟，备注提醒准备 PRD 文档。
```

---

### 7. email — 邮件发送

**用途：** 让 Agent 代你撰写和发送邮件，或在工作流自动化中触发邮件通知。

```bash
openclaw skill add email
```

**支持的邮件服务：**
- Gmail（通过 Google OAuth 或 App Password）
- 任意 SMTP 服务器

**配置 SMTP：**

```bash
openclaw config set skills.email.smtp.host "smtp.gmail.com"
openclaw config set skills.email.smtp.port "587"
openclaw config set skills.email.smtp.user "your@gmail.com"
openclaw config set skills.email.smtp.password "your-app-password"
```

**使用示例：**
```
你：根据今天的工作日报，给团队群发一封周报摘要邮件，收件人是 team@company.com。
```

---

### 8. image-gen — AI 图片生成

**用途：** 让 Agent 在对话中直接生成图片，支持本地 Stable Diffusion 和云端 API。

```bash
openclaw skill add image-gen
```

**支持的后端：**

```bash
# 使用 OpenAI DALL-E 3（云端，需要 API Key）
openclaw config set skills.image-gen.provider dalle
openclaw config set skills.image-gen.apiKey "sk-your-openai-key"

# 使用本地 Stable Diffusion WebUI（免费，需要本地运行 SD）
openclaw config set skills.image-gen.provider stable-diffusion
openclaw config set skills.image-gen.baseUrl "http://localhost:7860"
```

**使用示例：**
```
你：为我的技术博客文章生成一张封面图，主题是"AI Agent 协作"，风格是极简主义，16:9 比例。
```

---

### 9. database — 数据库查询

**用途：** 让 Agent 直接读写本地或远程数据库，执行 SQL 查询，处理结构化数据。

```bash
openclaw skill add database
```

**支持的数据库：**
- SQLite（无需服务器，适合本地数据分析）
- PostgreSQL
- MySQL / MariaDB

**配置示例（PostgreSQL）：**

```bash
openclaw config set skills.database.connections.prod.type postgresql
openclaw config set skills.database.connections.prod.url "postgresql://user:pass@localhost:5432/mydb"
```

**安全建议：** 强烈建议只授予 Agent 只读权限（`SELECT` 权限），避免数据误操作。

**使用示例：**
```
你：查询上个月每天的订单数量，找出销售额最高的三天，并解释可能的原因。
```

---

### 10. git-tools — Git 操作自动化

**用途：** 让 Agent 执行 Git 操作，自动提交代码、切换分支、查看差异，加速开发工作流。

```bash
openclaw skill add git-tools
```

**功能特性：**
- 查看 `git status`、`git diff`、`git log`
- 创建分支、提交代码、创建 PR
- 解析提交历史，生成变更日志

**使用示例：**
```
你：查看我今天修改了哪些文件，为每个文件写一条清晰的提交信息，然后按功能模块分组提交。
```

---

## 如何发现更多 Skills：ClauHub 平台

**[ClauHub](https://clawhub.ai)** 是 OpenClaw 社区的官方 Skill 目录，类似于 VS Code 的插件市场。在这里你可以：

- 按类别浏览（生产力、开发工具、数据、媒体等）
- 查看每个 Skill 的安装量、评分和用户评价
- 直接复制安装命令
- 查看 Skill 的源代码（大部分是开源的）

截至 2026 年 3 月，ClauHub 上已有超过 1,400 个 Skills。安装社区 Skill 的方式与官方 Skill 相同：

```bash
openclaw skill add @community/skill-name
```

---

## 安全注意事项

在安装和使用 Skills 时，请牢记以下安全原则：

**1. 只安装可信来源的 Skills**

官方 Skills（`@openclaw/` 前缀）经过安全审查。社区 Skills 要查看其 GitHub 源码和用户反馈再决定是否安装。

**2. 最小权限原则**

为每个 Skill 配置最小必要权限。例如，`file-manager` 限制可访问目录；`database` 使用只读账号；`email` 只授权必要的发件权限。

**3. 敏感操作需要确认**

在 `config.yaml` 中开启高风险操作的确认提示：

```yaml
agent:
  require_confirmation:
    - file-manager.delete
    - email.send
    - database.write
```

**4. 定期审查 Skill 列表**

运行 `openclaw skill list` 定期检查已安装的 Skills，卸载不再需要的模块。

---

## 下一步

掌握了 Skills 的安装和使用后，你可以进一步：

- [OpenClaw 多 Agent 配置教程：打造你的 AI 团队协作工作流](/tech/openclaw-multi-agent-setup/) — 学习如何组织多个专业化 Agent 分工协作，实现复杂任务自动化
- 如果你还没有安装 OpenClaw，请先阅读 [OpenClaw 安装教程：三平台完整指南](/tech/openclaw-install-guide/)
