# Phase 7: 抓取 openclaw101 仓库内容 - Research

**Researched:** 2026-03-09
**Domain:** GitHub 仓库内容抓取 + TypeScript 数据解析 + Hugo Markdown 转换
**Confidence:** HIGH

## Summary

Phase 7 需要抓取 https://github.com/mengjian-github/openclaw101 这个特定仓库的内容并转换为 Hugo 博客文章。

**核心发现：**
- 该仓库是一个 OpenClaw AI 助手的中文资源聚合站，拥有 357 个优质教程资源
- Phase 6 的工具可以直接抓取 README 和 Issues
- Phase 7 需要额外实现：resources.ts TypeScript 数据文件解析，将 357 个资源转换为独立文章
- 分类映射：仓库有 10 个分类（official, getting-started, channel-integration 等），需要映射到 Hugo Categories

**推荐方案：**
- 复用 Phase 6 的 GitHubFetcher（抓取 README、Issues）
- 新增 OpenClaw101Fetcher（专门抓取 resources.ts）
- 新增 TypeScript 解析器（解析 resources.ts 数据结构）
- AI 辅助为每个资源生成独立的 Hugo Markdown 文章

---

<user_constraints>
## User Constraints (from CONTEXT.md)

*No CONTEXT.md exists for Phase 7. This is the initial research phase.*

</user_constraints>

---

<phase_requirements>
## Phase Requirements

| ID | Description | Research Support |
|----|-------------|------------------|
| OCLAW-01 | 抓取 openclaw101 仓库的 README | Phase 6 GitHubFetcher.fetch_readme() 可直接复用 |
| OCLAW-02 | 抓取 openclaw101 仓库的 Issues | Phase 6 GitHubFetcher.fetch_issues() 可直接复用 |
| OCLAW-03 | 抓取 resources.ts 数据文件 | 需要新增 fetcher 实现 |
| OCLAW-04 | 解析 TypeScript 数据结构 | 需要新增解析器（正则或简单解析） |
| OCLAW-05 | 将资源转换为 Hugo Markdown | 复用 Phase 6 save_as_hugo_markdown() + AI 增强 |
| OCLAW-06 | 分类映射（10 个分类） | resources.ts 有 categoryMeta 映射关系 |
</phase_requirements>

---

## 1. openclaw101 仓库分析

### 基本信息

| 属性 | 值 |
|------|-----|
| 仓库名 | mengjian-github/openclaw101 |
| 描述 | 从零开始，7天掌握你的 AI 私人助理 \| 全网资源聚合站 |
| Stars | 1500+ |
| Forks | 147 |
| 语言 | TypeScript |
| 主题 | ai-assistant, chinese, nextjs, openclaw, resource, tutorial |

### 可抓取内容

| 内容类型 | 数量 | 抓取方式 |
|----------|------|----------|
| README | 1 | GitHub API /readme 端点 |
| Issues | 3 | GitHub API /issues 端点 |
| PRs | 2 | GitHub API /pulls 端点 |
| resources.ts | 357 个资源 | GitHub API /contents 端点 |

### 资源分类（10 个）

| Category | 中文标签 | 颜色 |
|----------|----------|------|
| official | 官方资源 | blue |
| getting-started | 入门部署 | green |
| channel-integration | 平台接入 | purple |
| skill-dev | 技能开发 | orange |
| video | 视频教程 | red |
| deep-dive | 深度文章 | indigo |
| tools | 工具与插件 | teal |
| cloud-deploy | 云平台部署 | sky |
| use-cases | 玩法与场景 | amber |

### 示例资源

```
- OpenClaw 官方文档
- GitHub — openclaw/openclaw
- 阿里云 — 部署 OpenClaw 构建钉钉 AI 助理
- 腾讯云 — OpenClaw 接入飞书保姆级教程
- DigitalOcean — One-Click Deploy OpenClaw
- B站视频教程
```

---

## 2. 抓取方案建议

### 方案 A: 复用 Phase 6 + 新增专用 Fetcher（推荐）

**优点：** 模块化、易维护、复用度高
**缺点：** 需要新增代码

```
Phase 6 现有模块:
├── scripts/fetchers/github_fetcher.py  ← 直接复用
├── scripts/formatters/openai_formatter.py  ← 直接复用
└── scripts/storage/url_store.py  ← 直接复用

Phase 7 新增模块:
├── scripts/fetchers/openclaw101_fetcher.py  ← 新增：抓取 resources.ts
├── scripts/parsers/typescript_parser.py  ← 新增：解析 resources.ts
└── scripts/formatters/resource_formatter.py  ← 新增：资源格式化
```

### 方案 B: 在现有模块中添加配置

**优点：** 改动最小
**缺点：** 代码耦合度高、不够灵活

### 推荐方案 A，理由：
1. Phase 6 是通用抓取工具，不适合硬编码特定仓库逻辑
2. openclaw101 有特殊数据结构（TypeScript 数组），需要专用解析器
3. 357 个资源需要分批处理，需要专门的资源格式化器

---

## 3. 内容转换方案

### 3.1 README 转换

```
输入：README.md (Markdown)
输出：content/tech/openclaw101-intro.md
Front Matter:
  - title: "OpenClaw 101 - 从零开始掌握 AI 私人助理"
  - categories: ["教程"]
  - tags: ["openclaw", "ai", "资源聚合"]
  - description: 简短描述
```

### 3.2 Issues 转换

```
输入：Issue #1, #2, #3
输出：content/tech/openclaw101-issue-{number}.md
Front Matter:
  - title: Issue 标题
  - categories: ["常见问题"]（或 AI 判断）
  - tags: 从 Issue labels 提取
  - description: Issue 摘要
```

### 3.3 Resources 转换（核心工作量）

```
输入：resources.ts (357 个 Resource 对象)
输出：content/tech/openclaw101-resource-{slug}.md（每个资源一篇）

资源转换逻辑：
1. 解析 TypeScript 数据 → Resource 对象列表
2. 对每个 Resource：
   - title → Hugo title
   - desc → Hugo description
   - url → 原文链接
   - source → 来源网站
   - lang → 语言
   - category → Hugo categories（需映射）
   - tags → Hugo tags
   - featured → 是否推荐

分类映射：
  official → ["官方资源"]
  getting-started → ["安装", "教程"]
  channel-integration → ["进阶"]
  skill-dev → ["进阶"]
  video → ["教程"]
  deep-dive → ["源码解析"]
  tools → ["工具"]
  cloud-deploy → ["教程"]
  use-cases → ["教程"]
```

### 3.4 AI 增强

由于资源数据字段有限（title, desc, url, source, lang, category, featured, tags），建议使用 OpenAI API 增强内容：
- 根据 title 和 desc 生成更详细的 description
- 从 url 抓取目标页面内容，生成摘要
- 自动补充相关 tags

---

## 4. 任务分解

### Task 1: 创建 OpenClaw101 Fetcher
**文件：** scripts/fetchers/openclaw101_fetcher.py
**功能：**
- 继承 BaseFetcher
- fetch_resources(owner, repo): 抓取 resources.ts 文件
- 使用 GitHub API /contents/src/data/resources.ts
- base64 解码并返回原始 TypeScript 内容

### Task 2: 创建 TypeScript 解析器
**文件：** scripts/parsers/typescript_parser.py
**功能：**
- parse_resources(content: str) → List[Resource]
- 使用正则表达式解析 TypeScript 对象数组
- 提取字段：title, desc, url, source, lang, category, featured, tags

### Task 3: 创建资源格式化器
**文件：** scripts/formatters/resource_formatter.py
**功能：**
- 复用 save_as_hugo_markdown()
- 分类映射函数（TypeScript category → Hugo categories）
- 资源文件名生成（openclaw101-resource-{slug}.md）

### Task 4: 更新配置文件
**文件：** scripts/config.py
**修改：**
- 添加 openclaw101 仓库到 github_repos 列表
- 或创建专门的抓取目标配置

### Task 5: 创建主抓取脚本
**文件：** scripts/fetch_openclaw101.py
**功能：**
- 编排抓取流程：README → Issues → Resources
- 批量处理 357 个资源
- 进度显示和错误处理

### Task 6: 测试和验证
- 运行抓取脚本
- 检查生成的文件格式
- 验证 Hugo 构建

---

## 5. 代码示例

### 5.1 OpenClaw101 Fetcher

```python
# Source: 基于 Phase 6 GitHubFetcher 模式
import base64
import httpx
from typing import List, Optional

class OpenClaw101Fetcher(BaseFetcher):
    """Fetch OpenClaw101 resources data file."""

    def __init__(self, token: Optional[str] = None):
        self.token = token
        self.base_url = "https://api.github.com"

    def _get_headers(self) -> dict:
        headers = {
            "Accept": "application/vnd.github+json",
            "X-GitHub-Api-Version": "2022-11-28",
        }
        if self.token:
            headers["Authorization"] = f"Bearer {self.token}"
        return headers

    def fetch_resources(self, owner: str = "mengjian-github", repo: str = "openclaw101") -> Optional[str]:
        """Fetch resources.ts file content."""
        url = f"{self.base_url}/repos/{owner}/{repo}/contents/src/data/resources.ts"

        try:
            with httpx.Client(timeout=30.0) as client:
                response = client.get(url, headers=self._get_headers())
                response.raise_for_status()
                data = response.json()
                content = base64.b64decode(data["content"]).decode("utf-8")
                return content
        except Exception as e:
            logger.error(f"Error fetching resources.ts: {e}")
            return None
```

### 5.2 TypeScript 解析器

```python
# Source: 自定义解析逻辑
import re
from dataclasses import dataclass
from typing import List, Optional

@dataclass
class Resource:
    title: str
    desc: str
    url: str
    source: str
    lang: str
    category: str
    featured: bool = False
    tags: List[str] = None

    def __post_init__(self):
        if self.tags is None:
            self.tags = []

def parse_resources(content: str) -> List[Resource]:
    """Parse TypeScript resources array."""
    resources = []

    # Match resource objects in the array
    pattern = r"\{\s*title:\s*'([^']+)',\s*desc:\s*'([^']+)',\s*url:\s*'([^']+)',\s*source:\s*'([^']+)'(?:,\s*sourceIcon:[^,]*)?(?:,\s*lang:\s*'([^']+)')?(?:,\s*category:\s*'([^']+)')?(?:,\s*featured:\s*(True|False))?(?:,\s*tags:\s*\[([^\]]*)\])?\s*\}"

    for match in re.finditer(pattern, content):
        title, desc, url, source, lang, category, featured, tags_str = match.groups()

        tags = []
        if tags_str:
            tags = [t.strip().strip("'\"") for t in tags_str.split(",") if t.strip()]

        resources.append(Resource(
            title=title,
            desc=desc,
            url=url,
            source=source,
            lang=lang or "en",
            category=category or "official",
            featured=featured == "True" if featured else False,
            tags=tags,
        ))

    return resources
```

### 5.3 分类映射

```python
# Category mapping from resources.ts to Hugo categories
CATEGORY_MAP = {
    "official": ["官方资源"],
    "getting-started": ["安装", "教程"],
    "channel-integration": ["进阶"],
    "skill-dev": ["进阶"],
    "video": ["教程"],
    "deep-dive": ["源码解析"],
    "tools": ["工具"],
    "cloud-deploy": ["教程"],
    "use-cases": ["教程"],
    # Default fallback
    None: ["教程"],
}

def map_category(ts_category: str) -> List[str]:
    """Map TypeScript category to Hugo categories."""
    return CATEGORY_MAP.get(ts_category, CATEGORY_MAP[None])
```

---

## 6. 差异化处理总结

| 功能 | Phase 6 通用工具 | Phase 7 额外处理 |
|------|------------------|------------------|
| README 抓取 | 直接可用 | 直接复用 |
| Issues 抓取 | 直接可用 | 直接复用 |
| PRs 抓取 | 不支持 | 需要新增（可选） |
| resources.ts 抓取 | 不支持 | **需要新增** |
| TypeScript 解析 | 不支持 | **需要新增** |
| 资源→文章转换 | 通用逻辑 | **需要新增 + AI 增强** |
| 分类映射 | AI 自动判断 | 预定义映射 + AI 增强 |

---

## 7. 潜在问题

### 问题 1: TypeScript 解析可能不完整
- resources.ts 可能有多种格式（单引号/双引号、尾随逗号等）
- **解决方案：** 使用正则覆盖常见模式，或使用 TypeScript AST 解析器（如 pyright）

### 问题 2: 357 个资源处理量大
- 每次调用 OpenAI API 有成本
- **解决方案：**
  1. 先批量抓取所有资源，不调用 AI
  2. 单独运行 AI 增强（可配置开关）
  3. 使用 gpt-4o-mini 降低成本

### 问题 3: URL 去重
- 357 个资源的 URL 都是外部链接
- **解决方案：** 复用 Phase 6 URLStore，按原始 URL 去重

### 问题 4: 文件名冲突
- 不同资源可能有相同标题
- **解决方案：** 使用 URL hash 或序号区分

---

## 8. 验证架构

> Skip this section entirely if workflow.nyquist_validation is explicitly set to false in .planning/config.json.

### Test Framework
| Property | Value |
|----------|-------|
| Framework | pytest 8.x |
| Config file | pytest.ini (or pyproject.toml) |
| Quick run command | `pytest tests/ -x -v` |
| Full suite command | `pytest tests/ --cov=scripts --cov-report=html` |

### Phase Requirements → Test Map
| Req ID | Behavior | Test Type | Automated Command | File Exists? |
|--------|----------|-----------|-------------------|-------------|
| OCLAW-01 | README 抓取 | integration | 复用 Phase 6 测试 | N/A |
| OCLAW-02 | Issues 抓取 | integration | 复用 Phase 6 测试 | N/A |
| OCLAW-03 | resources.ts 抓取 | unit | `pytest tests/test_openclaw101_fetcher.py -x` | 需要创建 |
| OCLAW-04 | TypeScript 解析 | unit | `pytest tests/test_typescript_parser.py -x` | 需要创建 |
| OCLAW-05 | 资源转换 | unit | `pytest tests/test_resource_formatter.py -x` | 需要创建 |

### Sampling Rate
- **Per task commit:** `pytest tests/ -x -v`
- **Per wave merge:** `pytest tests/ --cov=scripts`
- **Phase gate:** Full suite green before `/gsd:verify-work`

### Wave 0 Gaps
- [ ] `tests/test_openclaw101_fetcher.py` — 覆盖 OCLAW-03
- [ ] `tests/test_typescript_parser.py` — 覆盖 OCLAW-04
- [ ] `tests/test_resource_formatter.py` — 覆盖 OCLAW-05

---

## Sources

### Primary (HIGH confidence)
- [GitHub API 文档](https://docs.github.com/en/rest) - 仓库内容 API
- Phase 6 实现代码 - scripts/fetchers/github_fetcher.py
- Phase 6 研究文档 - 06-RESEARCH.md

### Secondary (MEDIUM confidence)
- [openclaw101 仓库](https://github.com/mengjian-github/openclaw101) - 实际数据源

### Tertiary (LOW confidence)
- TypeScript 解析最佳实践

---

## Metadata

**Confidence breakdown:**
- Standard stack: HIGH - 复用 Phase 6 成熟方案
- Architecture: HIGH - 基于现有模式扩展
- Pitfalls: MEDIUM - TypeScript 解析可能有边界情况
- Validation: MEDIUM - 测试策略基于 pytest 最佳实践

**Research date:** 2026-03-09
**Valid until:** 2026-04-09 (30 天)

---

## 下一步

1. 确认是否需要抓取 PRs（当前有 2 个 open PR）
2. 确认是否需要 AI 增强资源内容（成本 vs 质量权衡）
3. 确认目标输出目录（content/tech/ 或新建 openclaw101/ 子目录）
4. 开始实现 Phase 7 计划
