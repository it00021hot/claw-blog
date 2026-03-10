---
title: "安装指南"
---

## 快速开始

### 前置要求

| 系统 | 要求 |
|------|------|
| macOS | 12.0+ (Monterey 及以上)，Intel 或 Apple Silicon 芯片 |
| Linux | 内核版本 5.0+，支持 systemd 或 launchd |
| Windows | Windows 10 21H2+，推荐使用 WSL2 |
| 运行时 | Node.js 22.0+（必须） |

**检查 Node.js 版本：**
```bash
node -v  # 需要 >= v22.0.0
```

### 一、安装方式

#### 一键安装（推荐）

**macOS / Linux / WSL2：**
```bash
curl -fsSL https://openclaw.ai/install.sh | bash
```

**Windows PowerShell：**
```powershell
iwr -useb https://openclaw.ai/install.ps1 | iex
```

#### 包管理器安装

```bash
# npm
npm install -g openclaw@latest

# pnpm
pnpm add -g openclaw@latest
pnpm approve-builds -g
```

#### 源码安装（开发者）

```bash
git clone https://github.com/openclaw/openclaw.git
cd openclaw
pnpm install
pnpm build
pnpm link --global
```

### 二、初始化配置

```bash
openclaw onboard --install-daemon
```

向导会引导完成：
1. Gateway 服务配置（端口、远程访问）
2. 模型配置（支持所有主流 LLM 提供商）
3. 渠道接入（Telegram/Discord/WhatsApp 等）
4. 技能市场初始化

### 三、验证安装

```bash
openclaw --version    # 检查版本
openclaw doctor       # 健康检查
openclaw status       # 查看运行状态
openclaw dashboard    # 打开管理后台
```

### 详细文档

- [安装程序](/openclaw/install/installer/) - 一键安装脚本详解
- [Docker 部署](/openclaw/install/docker/) - Docker 安装方式
- [从源码开发](/openclaw/install/development-channels/) - 开发环境搭建
- [更新升级](/openclaw/install/updating/) - 版本更新指南
- [卸载](/openclaw/install/uninstall/) - 卸载 OpenClaw
