---
title: "Summarize Skill - 多格式内容摘要工具"
date: 2026-03-10T14:20:00+08:00
draft: false
categories: ["效率工具"]
tags: ["摘要", "PDF 处理", "音视频转写"]
---

## 功能介绍
支持多格式内容的自动摘要生成：
- 网页内容摘要
- PDF/Word 文档摘要
- 图片 OCR + 摘要
- 音频/视频转写 + 摘要
- YouTube 视频自动总结

## 安装方式
```bash
npx clawhub@latest install summarize
```

## 使用场景
1. 技术文档快速阅读
2. 会议记录自动总结
3. 长视频/音频内容提炼
4. 文献综述自动生成

## 使用教程
### 前置准备
1. 首先安装 summarize CLI：
```bash
# MacOS (推荐)
brew install steipete/tap/summarize

# 跨平台 npm 安装
npm install -g @steipete/summarize
```

2. 配置 LLM API Key（选择其中一个即可）：
```bash
# Google Gemini (默认模型，免费额度高)
export GEMINI_API_KEY="你的Gemini API Key"

# OpenAI
export OPENAI_API_KEY="你的OpenAI API Key"

# Anthropic Claude
export ANTHROPIC_API_KEY="你的Claude API Key"

# 永久生效（添加到 ~/.zshrc）
echo 'export GEMINI_API_KEY="你的API Key"' >> ~/.zshrc
source ~/.zshrc
```

### 基础使用
#### 网页摘要
```bash
# 默认使用 Gemini 模型，中等长度摘要
summarize "https://docs.openclaw.ai/guide/skills"
```

#### 本地文件摘要（PDF/Word/图片/音频）
```bash
# 生成 PDF 文档摘要
summarize "/path/to/技术方案.pdf"

# 生成图片 OCR + 摘要
summarize "/path/to/架构图.png"

# 生成音频转写 + 摘要
summarize "/path/to/会议录音.mp3"
```

#### YouTube 视频摘要
```bash
# 自动获取字幕并生成摘要
summarize "https://youtu.be/dQw4w9WgXcQ" --youtube auto
```

### 高级参数
#### 指定摘要长度
```bash
# 短摘要（适合快速预览）
summarize "https://example.com/article" --length short

# 长摘要（适合深度阅读）
summarize "https://example.com/long-article" --length long

# 自定义长度（最多 10000 字符）
summarize "https://example.com/report" --length 5000
```

#### 指定模型
```bash
# 使用 GPT-4o
summarize "/path/to/论文.pdf" --model openai/gpt-4o

# 使用 Claude 3 Opus
summarize "/path/to/法律文档.pdf" --model anthropic/claude-3-opus
```

#### 特殊功能
```bash
# 只提取网页正文，不生成摘要
summarize "https://example.com" --extract-only

# 输出 JSON 格式（便于程序处理）
summarize "https://example.com" --json

# 开启 Firecrawl  fallback（解决反爬网站无法提取的问题）
summarize "https://blocked-site.com/article" --firecrawl auto
```

### 配置文件（可选）
创建 `~/.summarize/config.json` 配置默认参数：
```json
{
  "model": "openai/gpt-4o",
  "length": "medium",
  "firecrawl": "auto"
}
```

### 使用技巧
1. 长文档、技术论文建议使用长摘要模式，搭配 Claude/GPT 模型效果更好
2. YouTube 视频摘要需要配置 `APIFY_API_TOKEN` 作为 fallback，应对字幕无法获取的情况
3. 处理反爬网站时添加 `--firecrawl auto` 参数，会自动使用 Firecrawl 服务提取内容
4. 批量处理文件时可以结合 shell 脚本实现自动化摘要生成

## 评分
⭐ 448 · 下载量 107k
作者：@steipete