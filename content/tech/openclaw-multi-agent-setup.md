---
title: "OpenClaw 多 Agent 配置教程：打造你的 AI 团队协作工作流（2026）"
date: 2026-03-09
categories:
  - 进阶
  - 教程
tags:
  - OpenClaw
  - Multi-Agent
  - 工作流
description: "手把手教你在 OpenClaw 中配置多个 AI Agent 协作工作，实现自动化业务流水线，附完整配置文件示例。"
keywords:
  - OpenClaw
  - 多Agent
  - 工作流
  - 自动化
featured: true
---

## 什么是 Multi-Agent，为什么需要它

在面对复杂任务时，单个 AI Agent 往往力不从心——不是因为能力不足，而是因为**上下文窗口有限、专注度有限、工具集有限**。想象你要完成一份深度行业分析报告：需要搜集数十个来源的数据、进行统计分析、撰写结构化内容、润色语言风格、配图排版……这些事情对一个通才 Agent 来说负担极重，很可能在某个环节出现疏漏。

这正是 Multi-Agent 架构要解决的问题。Multi-Agent 的核心思想是**分工与专业化**：将一个复杂任务拆分成若干子任务，分别交给在该领域经过专门配置的 Agent 处理，最后由一个协调 Agent 汇总结果。这种模式类似于一个真实的团队：有项目经理协调全局，有专家各司其职，效率远高于单打独斗。

OpenClaw 从 v2026.2 版本开始内置了完整的 Multi-Agent 支持，无需第三方框架，只需一个 `agents.yaml` 配置文件即可搭建你自己的 AI 团队。

---

## 核心概念：三种 Agent 角色

在 OpenClaw 的 Multi-Agent 体系中，Agent 分为三种角色：

### Orchestrator Agent（协调者）

负责任务分解、工作分配和结果汇总。Orchestrator 接收用户的原始请求，决定将哪些子任务派发给哪些 Worker，并在所有子任务完成后合并输出最终结果。通常使用能力最强的 LLM 模型（如 Claude Opus 或 GPT-4o）。

**特点：**
- 理解整体目标，制定执行计划
- 动态调度 Worker Agent
- 负责错误处理和重试逻辑
- 生成最终的用户可见输出

### Worker Agent（执行者）

负责执行具体的单一任务。Worker 接收来自 Orchestrator 的明确指令，使用自己配置的 Skill 完成任务，将结果返回给 Orchestrator。通常使用高性价比的 LLM 模型（如 Claude Haiku 或 GPT-4o-mini）以节省成本。

**特点：**
- 专注于一类具体任务
- 配置特定的 Skills 子集
- 上下文较短，成本可控
- 可并行运行多个实例

### Specialized Agent（专家）

Worker 的特殊变体，深度专注于某个垂直领域，通常配有详细的 System Prompt 来注入领域知识。例如：专门做数据分析的 Analyst Agent、专门写营销文案的 Copywriter Agent、专门做安全审查的 Security Agent 等。

---

## 基础配置：agents.yaml 文件结构

所有 Agent 配置都在一个 `agents.yaml` 文件中定义，默认路径为 `~/.openclaw/agents.yaml`。

以下是配置文件的基本结构说明：

```yaml
# ~/.openclaw/agents.yaml

version: "1.0"

# 全局默认设置
defaults:
  timeout: 120          # Agent 超时时间（秒）
  max_retries: 3        # 失败重试次数
  log_level: info       # 日志级别：debug | info | warn | error

agents:
  # 定义一个 Agent
  - id: my-agent                    # 唯一标识符（必填）
    name: "我的助手"                 # 显示名称
    role: worker                    # 角色：orchestrator | worker | specialized
    model:
      provider: anthropic           # LLM 提供商
      name: claude-haiku-4-5        # 模型名称
    system_prompt: |                # Agent 的角色设定（多行文本）
      你是一个专业的助手……
    skills:                         # 该 Agent 可使用的 Skills
      - web-search
      - file-manager
    context_limit: 8000             # 上下文长度限制（tokens）
```

**重要配置字段说明：**

| 字段 | 类型 | 说明 |
|------|------|------|
| `id` | string | 唯一标识符，其他 Agent 引用时使用 |
| `role` | enum | orchestrator / worker / specialized |
| `model.provider` | string | anthropic / openai / ollama |
| `model.name` | string | 具体的模型名称 |
| `system_prompt` | string | Agent 的角色和行为设定 |
| `skills` | list | 该 Agent 可使用的已安装 Skills |
| `context_limit` | int | 最大上下文长度（影响费用） |

---

## 实战案例一：内容创作团队

**场景：** 输入一个主题，自动完成从资料研究到文章定稿的全流程。

**团队构成：**
- `researcher`：搜索和整理资料
- `writer`：基于资料撰写初稿
- `editor`：润色语言、优化结构

### 完整 agents.yaml 配置

```yaml
version: "1.0"

defaults:
  timeout: 180
  max_retries: 2

agents:
  # 协调者：接收用户请求，分派任务，汇总输出
  - id: content-orchestrator
    name: "内容团队协调者"
    role: orchestrator
    model:
      provider: anthropic
      name: claude-sonnet-4-6
    system_prompt: |
      你是一个内容创作团队的项目经理。
      当用户提出内容创作请求时，你需要：
      1. 分析主题和目标受众
      2. 将研究任务交给 researcher
      3. 将写作任务连同研究结果交给 writer
      4. 将初稿交给 editor 进行润色
      5. 整合最终结果返回给用户
      始终按照这个顺序串行执行，确保每个步骤的输出作为下一步的输入。
    delegates_to:
      - researcher
      - writer
      - editor

  # 研究员：专注信息搜集
  - id: researcher
    name: "资料研究员"
    role: specialized
    model:
      provider: anthropic
      name: claude-haiku-4-5    # 使用 Haiku 节省成本
    system_prompt: |
      你是一个专业的信息研究员，擅长快速搜集和整理资料。
      收到研究主题后，你需要：
      1. 搜索 3-5 个高质量来源
      2. 提取关键数据点、观点和案例
      3. 按照"背景 → 现状 → 趋势"结构整理笔记
      4. 标注每个信息点的来源 URL
      输出格式：结构化 Markdown 研究笔记
    skills:
      - web-search
      - browser-use
    context_limit: 12000

  # 写作员：基于资料撰写初稿
  - id: writer
    name: "内容撰写员"
    role: specialized
    model:
      provider: anthropic
      name: claude-sonnet-4-6
    system_prompt: |
      你是一个擅长技术写作的内容创作者，文风清晰、有洞察力。
      收到研究笔记和写作要求后，你需要：
      1. 拟定清晰的文章结构（标题层级）
      2. 撰写引人入胜的开头
      3. 展开每个章节，插入数据和案例支撑观点
      4. 写出有力的结论段
      避免空洞的套话，每个段落都要有实质性内容。
    skills:
      - file-manager    # 可以保存草稿
    context_limit: 16000

  # 编辑：润色和优化
  - id: editor
    name: "内容编辑"
    role: specialized
    model:
      provider: anthropic
      name: claude-haiku-4-5
    system_prompt: |
      你是一个经验丰富的内容编辑，专注于：
      1. 检查逻辑连贯性和论证完整性
      2. 消除重复表达和冗余句子
      3. 优化标题和小标题的吸引力
      4. 确保专业术语使用准确
      5. 检查格式规范（标点、空格、代码块等）
      保留原文的核心观点和结构，只做必要的语言优化。
    context_limit: 10000
```

### 触发方式

配置完成后，通过 OpenClaw 的 `team` 命令启动内容创作团队：

```bash
# 命令行触发
openclaw team run content-orchestrator \
  --input "写一篇关于 AI Agent 在 2026 年企业落地挑战的深度分析文章，目标受众是技术决策者，字数 2000 字"

# 或在交互式对话中使用 @mention 语法
openclaw chat --agent content-orchestrator
```

### 预期输出

整个流程大约需要 2-5 分钟（取决于网络速度和模型响应）。最终输出是一篇完整的 Markdown 格式文章，包含：
- 研究员的资料笔记（中间过程可选查看）
- 写作员的初稿
- 编辑润色后的终稿
- 引用的信息来源列表

---

## 实战案例二：数据分析流水线

**场景：** 自动完成从原始数据到分析报告的端到端流程。

**团队构成：**
- `data-collector`：获取和清洗数据
- `analyst`：统计分析和模式发现
- `reporter`：生成可读的分析报告

### 完整配置示例

```yaml
# 追加到 agents.yaml 的 agents 列表中

  # 数据分析流水线协调者
  - id: data-pipeline-orchestrator
    name: "数据分析流水线"
    role: orchestrator
    model:
      provider: anthropic
      name: claude-sonnet-4-6
    system_prompt: |
      你是数据分析团队的协调者。
      接收数据分析请求后，按顺序执行：
      1. 让 data-collector 获取和预处理数据
      2. 将清洗后的数据交给 analyst 进行分析
      3. 将分析结果交给 reporter 生成报告
      如果任何步骤失败，记录错误并通知用户。
    delegates_to:
      - data-collector
      - analyst
      - reporter

  - id: data-collector
    name: "数据采集员"
    role: specialized
    model:
      provider: openai
      name: gpt-4o-mini         # 使用 OpenAI mini 降低成本
    system_prompt: |
      你是数据工程师，负责数据获取和预处理。
      1. 根据要求获取数据（文件、数据库查询或网络爬取）
      2. 检查数据完整性，处理缺失值
      3. 标准化数据格式（日期、数值、类别）
      4. 输出清洗后的 CSV 格式数据和数据质量报告
    skills:
      - database
      - file-manager
      - code-interpreter
    context_limit: 8000

  - id: analyst
    name: "数据分析师"
    role: specialized
    model:
      provider: anthropic
      name: claude-sonnet-4-6
    system_prompt: |
      你是统计分析专家，擅长发现数据中的规律和洞察。
      1. 执行描述性统计分析（均值、中位数、分布）
      2. 识别趋势、异常值和相关性
      3. 生成数据可视化图表
      4. 提出 3-5 个有价值的业务洞察
      5. 量化每个洞察的置信度
    skills:
      - code-interpreter    # 执行 Python 数据分析代码
      - file-manager
    context_limit: 16000

  - id: reporter
    name: "报告撰写员"
    role: specialized
    model:
      provider: anthropic
      name: claude-haiku-4-5
    system_prompt: |
      你是商业报告撰写专家，将技术分析结果转化为清晰的业务报告。
      1. 撰写执行摘要（200字以内，适合管理层阅读）
      2. 用非技术语言解释关键发现
      3. 突出对业务决策最相关的洞察
      4. 提出可操作的建议
      5. 使用表格和列表提高可读性
    skills:
      - file-manager    # 保存最终报告
    context_limit: 8000
```

**触发示例：**

```bash
openclaw team run data-pipeline-orchestrator \
  --input "分析 ~/sales-data/Q1-2026.csv，重点关注各产品线的销售趋势和异常，生成适合向管理层汇报的分析报告"
```

---

## Agent 间通信：消息传递格式

Agent 之间通过结构化消息传递中间结果。了解这个机制有助于优化 Prompt 设计。

### 上下文共享

Orchestrator 将子任务的结果通过 `context` 字段传递给后续 Agent：

```json
{
  "task": "基于以下研究笔记写一篇文章",
  "context": {
    "research_notes": "...",
    "word_count": 2000,
    "target_audience": "技术决策者"
  }
}
```

在 `agents.yaml` 中，你可以指定哪些上下文字段要传递给每个 Worker：

```yaml
- id: content-orchestrator
  pipeline:
    - agent: researcher
      output_key: research_notes
    - agent: writer
      inject_context:
        - research_notes    # 将 researcher 的输出注入给 writer
```

### 检查 Agent 通信日志

```bash
# 查看最近一次 Agent 执行的完整通信日志
openclaw team logs --last

# 实时监控 Agent 间的消息传递（调试用）
openclaw team run content-orchestrator --input "..." --debug
```

---

## 调试技巧

### 查看 Agent 日志

```bash
# 查看指定 Agent 的最近日志
openclaw logs --agent researcher --lines 50

# 导出完整执行报告（JSON 格式）
openclaw team export-report --last --output ./debug-report.json
```

### 排查常见错误

**错误 1：`Agent 'researcher' not found`**

确认 `agents.yaml` 中 Agent 的 `id` 与 `delegates_to` 列表中的名称完全匹配（区分大小写）。

**错误 2：`Context limit exceeded`**

将某个 Agent 的 `context_limit` 提高，或优化 System Prompt 减少不必要的上下文传递。也可以在 Orchestrator 中添加摘要步骤，在传递给下一个 Agent 之前先压缩上文。

**错误 3：`Skill 'web-search' not authorized for agent 'researcher'`**

确保该 Skill 已安装（`openclaw skill list`），且在 Agent 配置的 `skills` 列表中声明了它。

**错误 4：Orchestrator 卡住不响应**

通常是 Orchestrator 在等待某个 Worker 超时。检查 `timeout` 配置，或查看对应 Worker 的日志找出瓶颈。

---

## 进阶：动态 Agent 创建

除了静态配置文件，OpenClaw 还支持通过 Orchestrator 动态创建 Agent，适用于任务类型不固定的场景。

在 Orchestrator 的 System Prompt 中，你可以让 LLM 自行决定需要创建什么类型的 Worker：

```yaml
- id: adaptive-orchestrator
  name: "自适应协调者"
  role: orchestrator
  model:
    provider: anthropic
    name: claude-sonnet-4-6
  system_prompt: |
    你是一个智能任务协调者。分析用户请求后，自行决定需要哪些专门的 Worker Agent：
    - 如果任务需要网络信息：创建配备 web-search 的 researcher
    - 如果任务需要代码执行：创建配备 code-interpreter 的 developer
    - 如果任务需要文件操作：创建配备 file-manager 的 file-handler
    - 如果任务需要生成报告：创建配备写作能力的 writer
    动态创建后，分配任务，收集结果，汇总输出。
  dynamic_agents: true    # 开启动态 Agent 创建
  agent_pool:             # 可用的 Agent 模板
    - template: researcher
    - template: developer
    - template: writer
```

> **注意：** 动态 Agent 创建会增加额外的 LLM 调用开销（Orchestrator 需要先"思考"要创建什么 Agent），适合任务类型多样、难以预定义的场景。

---

## 性能优化：并行执行 vs 串行执行

默认情况下，Orchestrator 串行调用 Worker。如果子任务之间没有依赖关系，可以开启并行执行大幅提速：

```yaml
- id: parallel-orchestrator
  name: "并行协调者"
  role: orchestrator
  execution:
    mode: parallel          # 改为 parallel（默认是 sequential）
    max_concurrent: 3       # 最多同时运行 3 个 Worker
  delegates_to:
    - researcher-1
    - researcher-2
    - researcher-3
```

**选择原则：**

| 场景 | 推荐模式 | 原因 |
|------|---------|------|
| 后续任务依赖前一步输出 | 串行（sequential） | 必须等待前置结果 |
| 多个独立数据源采集 | 并行（parallel） | 互不依赖，同时进行 |
| 同一文档的不同维度分析 | 并行（parallel） | 互不依赖，节省时间 |
| 写作 → 编辑 流程 | 串行（sequential） | 编辑需要写作的输出 |

**实际效果：** 在内容创作案例中，如果研究阶段需要搜索 5 个来源，使用并行模式（5 个并发 Worker）可将时间从约 2 分钟缩短至约 30 秒。

---

## 相关资源

掌握多 Agent 配置后，建议结合以下资源提升你的 OpenClaw 使用体验：

- [OpenClaw 安装教程：macOS / Linux / Windows 三平台完整指南](/tech/openclaw-install-guide/) — 如果你还没有安装 OpenClaw，从这里开始
- [OpenClaw 必备 Skills 清单：2026 年最值得安装的 10 个技能](/tech/openclaw-essential-skills/) — 了解 Agent 可用的各类工具 Skills，为你的 Agent 团队装备最合适的能力
- [OpenClaw 官方文档 - Multi-Agent](https://docs.openclaw.ai/advanced/multi-agent) — 官方参考文档（英文）
- [ClauHub 多 Agent 配置模板库](https://clawhub.ai/templates) — 社区贡献的多 Agent 配置模板，覆盖常见业务场景
