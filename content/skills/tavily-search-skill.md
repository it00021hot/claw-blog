---
title: "Tavily Web Search Skill - AI 优化搜索引擎"
date: 2026-03-10T14:20:00+08:00
draft: false
categories: ["搜索工具"]
tags: ["AI 搜索", "信息检索", "开发辅助"]
---

## 功能介绍
专为 AI 代理优化的网页搜索工具，返回高度相关、简洁的搜索结果：
- 实时网页信息抓取
- 结果自动去重、摘要提取
- 支持多语言搜索
- 适配 Agent 上下文格式

## 安装方式
```bash
npx clawhub@latest install tavily-search
```

## 使用场景
1. 开发问题解决方案搜索
2. 最新技术文档检索
3. 开源项目信息查询
4. 实时资讯获取

## 使用教程
### 前置准备
1. 首先去 [Tavily 官网](https://tavily.com) 注册账号，获取 API Key
2. 将 API Key 添加到环境变量：
```bash
# 临时生效
export TAVILY_API_KEY="你的API Key"

# 永久生效（添加到 ~/.zshrc 或 ~/.bashrc）
echo 'export TAVILY_API_KEY="你的API Key"' >> ~/.zshrc
source ~/.zshrc
```

### 基础使用
#### 普通搜索
```bash
# 默认返回 5 条结果
node ~/.openclaw/skills/tavily-search/scripts/search.mjs "OpenClaw 多代理使用教程"
```

#### 指定结果数量
```bash
# 返回 10 条结果
node ~/.openclaw/skills/tavily-search/scripts/search.mjs "Rust 异步编程最佳实践" -n 10
```

#### 深度搜索（更全面，速度稍慢）
```bash
node ~/.openclaw/skills/tavily-search/scripts/search.mjs "2026 年 AI 创业趋势" --deep
```

#### 新闻搜索（实时资讯）
```bash
# 搜索最近 7 天的新闻
node ~/.openclaw/skills/tavily-search/scripts/search.mjs "OpenClaw 最新版本发布" --topic news --days 7
```

### 网页内容提取
直接提取指定 URL 的正文内容：
```bash
node ~/.openclaw/skills/tavily-search/scripts/extract.mjs "https://docs.openclaw.ai/guide/skills"
```

### 可用参数说明
| 参数 | 说明 | 默认值 |
|------|------|--------|
| `-n <count>` | 返回结果数量 | 5（最大 20） |
| `--deep` | 开启深度搜索 | 关闭 |
| `--topic <topic>` | 搜索主题：general(通用)/news(新闻) | general |
| `--days <n>` | 新闻搜索时限制时间范围（最近 n 天） | 无限制 |

### 使用技巧
1. 开发问题搜索建议使用默认参数，返回结果最精准
2. 调研行业趋势、最新技术动态时使用 `--deep` 参数
3. 查找实时新闻、版本发布信息时使用 `--topic news`
4. 提取网页内容时支持 Markdown 格式输出，可直接用于文档编写

## 评分
⭐ 724 · 下载量 142k
作者：@arun-8687