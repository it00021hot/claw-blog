---
title: "OpenClaw 安装教程：macOS / Linux / Windows 三平台完整指南（2026）"
date: 2026-03-09
categories:
  - 安装
  - 教程
tags:
  - OpenClaw
  - 安装
  - 教程
description: "从零安装 OpenClaw 的完整指南，覆盖 macOS、Linux、Windows 三平台，包含常见问题排查。"
keywords:
  - OpenClaw
  - 安装教程
  - 部署
featured: true
---

## 什么是 OpenClaw

OpenClaw 是一款开源的本地 AI Agent 框架，允许你在自己的设备上运行一个拥有记忆、可以使用工具、并能完成复杂任务的 AI 助手。与纯聊天机器人不同，OpenClaw 能够主动执行操作——搜索网页、读写文件、运行代码、发送邮件——而这些操作完全运行在你的控制之下。

自 2026 年初在 GitHub 迅速走红（14 天内突破 19 万 Star）以来，OpenClaw 已成为个人 AI 自动化领域最受关注的开源项目。本文将带你在三个主流平台上完成完整安装，让你在 15 分钟内完成从零到第一次对话。

---

## 前置要求

在开始安装之前，请确认你的环境满足以下条件：

| 依赖 | 最低版本 | 推荐版本 | 说明 |
|------|---------|---------|------|
| Node.js | 18.x | 20.x LTS | OpenClaw 核心运行时 |
| npm | 9.x | 10.x | 随 Node.js 附带 |
| 内存 | 4 GB | 8 GB+ | 运行本地模型需要更多 |
| 磁盘空间 | 500 MB | 2 GB+ | 含依赖和模型缓存 |

**检查当前 Node.js 版本：**

```bash
node -v
npm -v
```

如果版本不满足要求，请先访问 [https://nodejs.org](https://nodejs.org) 下载最新 LTS 版本，或使用下文各平台的包管理器安装。

---

## macOS 安装

macOS 用户有两种推荐方式：Homebrew（推荐）和直接使用 npm。

### 方式一：Homebrew 安装（推荐）

Homebrew 是 macOS 上最流行的包管理器，能自动处理依赖关系。

**第一步：安装 Homebrew（已安装可跳过）**

```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

**第二步：通过 Homebrew 安装 Node.js**

```bash
brew install node@20
echo 'export PATH="/opt/homebrew/opt/node@20/bin:$PATH"' >> ~/.zshrc
source ~/.zshrc
```

**第三步：全局安装 OpenClaw**

```bash
npm install -g @openclaw/cli
```

### 方式二：直接 npm 安装

如果你已有 Node.js 18+，可以直接运行：

```bash
npm install -g @openclaw/cli
```

**Apple Silicon（M1/M2/M3/M4）特别说明：**

Apple Silicon Mac 用户通常无需额外配置。但如果遇到原生模块编译问题，请确保安装了 Xcode Command Line Tools：

```bash
xcode-select --install
```

---

## Linux 安装

以下以 Ubuntu 22.04 / Debian 12 为示例，其他发行版步骤类似。

### 安装系统依赖

```bash
# 更新包列表
sudo apt update

# 安装编译工具（某些原生模块需要）
sudo apt install -y build-essential curl git

# 安装 Node.js（使用 NodeSource 仓库）
curl -fsSL https://deb.nodesource.com/setup_20.x | sudo -E bash -
sudo apt install -y nodejs

# 验证安装
node -v
npm -v
```

### 安装 OpenClaw

```bash
# 全局安装（可能需要 sudo，取决于 npm 权限配置）
npm install -g @openclaw/cli

# 如果遇到权限问题，推荐使用 npx 或配置 npm 用户目录
mkdir -p ~/.npm-global
npm config set prefix '~/.npm-global'
echo 'export PATH=~/.npm-global/bin:$PATH' >> ~/.bashrc
source ~/.bashrc
npm install -g @openclaw/cli
```

### 无头服务器配置

在没有图形界面的服务器上，OpenClaw 支持纯 CLI 模式运行。确保开放所需端口（默认 3000）：

```bash
# 如果使用 ufw 防火墙
sudo ufw allow 3000/tcp
```

---

## Windows 安装

Windows 用户有两条路径：WSL2（推荐）和原生 PowerShell。

### 方式一：WSL2 安装（强烈推荐）

WSL2（Windows Subsystem for Linux 2）提供接近原生 Linux 的体验，是在 Windows 上运行 OpenClaw 的最佳方式。

**第一步：启用 WSL2**

以管理员身份打开 PowerShell，运行：

```powershell
wsl --install
```

重启计算机后，WSL2 会自动完成安装并创建 Ubuntu 环境。

**第二步：在 WSL2 中安装 Node.js 和 OpenClaw**

打开 WSL2 终端（Ubuntu），然后按照上方 Linux 安装步骤操作即可。

### 方式二：原生 Windows（PowerShell）

**第一步：安装 Node.js**

访问 [https://nodejs.org/zh-cn/download/](https://nodejs.org/zh-cn/download/) 下载 Windows 安装包（.msi），双击运行，全程使用默认配置。

**第二步：安装 Windows Build Tools（可选，处理原生模块需要）**

以管理员身份在 PowerShell 中运行：

```powershell
npm install -g windows-build-tools
```

**第三步：安装 OpenClaw**

```powershell
npm install -g @openclaw/cli
```

**Windows 注意事项：**
- 建议使用 Windows Terminal 而非传统 CMD
- 路径中避免中文或空格
- 如遇到 PowerShell 执行策略问题，运行 `Set-ExecutionPolicy RemoteSigned -Scope CurrentUser`

---

## 首次启动与配置

安装完成后，使用以下命令初始化 OpenClaw：

```bash
openclaw init
```

初始化向导会引导你完成以下配置：

### 配置 API Key

OpenClaw 支持多种 LLM 提供商，选择你已有账号的服务商：

**使用 Anthropic Claude（推荐）：**

```bash
openclaw config set llm.provider anthropic
openclaw config set llm.apiKey "sk-ant-your-api-key-here"
openclaw config set llm.model "claude-sonnet-4-6"
```

**使用 OpenAI：**

```bash
openclaw config set llm.provider openai
openclaw config set llm.apiKey "sk-your-openai-api-key"
openclaw config set llm.model "gpt-4o"
```

**使用 Ollama（本地免费模型）：**

```bash
# 先安装 Ollama
curl -fsSL https://ollama.ai/install.sh | sh
ollama pull llama3.2

# 然后配置 OpenClaw
openclaw config set llm.provider ollama
openclaw config set llm.model "llama3.2"
openclaw config set llm.baseUrl "http://localhost:11434"
```

### 配置文件位置

OpenClaw 的配置文件存储在：
- macOS / Linux：`~/.openclaw/config.yaml`
- Windows：`%APPDATA%\openclaw\config.yaml`

你也可以直接编辑该文件进行高级配置。

---

## 验证安装

配置完成后，运行以下命令验证安装是否成功：

```bash
# 检查版本
openclaw --version

# 检查配置
openclaw config check

# 发送一条测试消息
openclaw chat "你好，请用一句话介绍你自己"
```

如果 `config check` 显示 `✓ LLM connected`，并且 `chat` 命令返回了 AI 的回复，说明安装已成功。

你也可以通过 Web 界面访问 OpenClaw：

```bash
openclaw server start
# 然后在浏览器中打开 http://localhost:3000
```

---

## 常见问题排查

**Q1：运行 `openclaw` 提示 `command not found`**

这通常是 npm 全局目录未加入 `PATH` 导致的。运行以下命令查找 npm 全局目录：

```bash
npm config get prefix
```

然后将输出路径下的 `bin` 目录添加到 `PATH`。例如输出为 `/usr/local`，则添加 `export PATH="/usr/local/bin:$PATH"` 到你的 shell 配置文件。

**Q2：`npm install -g @openclaw/cli` 报错 `EACCES: permission denied`**

这是 npm 权限问题。推荐方案是配置 npm 用户级全局目录：

```bash
mkdir -p ~/.npm-global
npm config set prefix '~/.npm-global'
echo 'export PATH=~/.npm-global/bin:$PATH' >> ~/.bashrc  # 或 ~/.zshrc
source ~/.bashrc
```

然后重新运行安装命令（不需要 sudo）。

**Q3：`openclaw config check` 显示 `✗ LLM connection failed`**

请检查：
1. API Key 是否正确复制（无多余空格）
2. 网络是否能访问 LLM 提供商的 API 端点
3. 账户是否有足够的额度或权限
4. 如果使用 Ollama，确认 `ollama serve` 进程正在运行

**Q4：在 M1/M2 Mac 上安装原生模块失败**

确保 Xcode Command Line Tools 已安装，然后运行：

```bash
arch -arm64 npm install -g @openclaw/cli
```

**Q5：Windows 上遇到 `EPERM: operation not permitted`**

以管理员身份运行 PowerShell 或 CMD，或者将 OpenClaw 数据目录的权限开放给当前用户。

---

## 下一步

安装成功后，建议阅读以下内容继续深入学习：

- [OpenClaw 必备 Skills 清单：2026 年最值得安装的 10 个技能](/tech/openclaw-essential-skills/) — 通过安装 Skills 大幅扩展 OpenClaw 的能力
- [OpenClaw 多 Agent 配置教程：打造你的 AI 团队协作工作流](/tech/openclaw-multi-agent-setup/) — 学习如何让多个 AI Agent 分工协作

如有问题，可以在 OpenClaw 的 [GitHub Issues](https://github.com/openclawai/openclaw/issues) 或 Discord 社区寻求帮助。
