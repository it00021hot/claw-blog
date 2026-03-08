# Phase 6: 内容抓取工具 - Research

**Researched:** 2026-03-08
**Domain:** Python 爬虫 + GitHub API + OpenAI API 集成
**Confidence:** HIGH

## Summary

Phase 6 需要构建一个文章抓取工具，从 GitHub 仓库（Issues、PRs、README）和技术博客抓取内容，使用 OpenAI API 转换为 Hugo Markdown 格式，并自动分类。

**核心推荐方案：**
- 使用 Python + httpx（异步 HTTP 客户端）+ BeautifulSoup4（HTML 解析）
- GitHub API 直接调用（无需额外库）
- 独立 GitHub Actions workflow（定时 8:00 UTC）
- JSON 文件存储已抓取 URL 实现去重

## User Constraints (from CONTEXT.md)

### Locked Decisions
- 触发方式：混合模式（手动运行 + GitHub Actions 定时每天 8:00 UTC）
- 输出目录：content/tech/ 和 content/fiction/
- Front Matter：由 AI 自动判断
- 去重策略：基于 URL，JSON 文件存储
- 抓取来源：GitHub 仓库（Issues、PR、README）+ 技术博客 URL
- AI 格式化：OpenAI API (GPT-4)
- 分类方式：AI 自动分析，Categories + Tags

### Claude's Discretion
- 具体的 Python 依赖库选择
- JSON 文件的具体格式和路径
- 定时任务的具体 cron 表达式
- 错误处理和日志策略

### Deferred Ideas (OUT OF SCOPE)
- 多平台内容抓取（抖音、小红书等）- 未来阶段

---

<phase_requirements>
## Phase Requirements

| ID | Description | Research Support |
|----|-------------|------------------|
| FETCH-01 | 从 GitHub 仓库抓取 Issues、PRs、README | GitHub REST API 直接调用，无需额外库 |
| FETCH-02 | 从技术博客抓取文章 | httpx + BeautifulSoup4 标准爬虫组合 |
| FETCH-03 | 使用 OpenAI API 转换为 Hugo Markdown | openai Python SDK |
| FETCH-04 | AI 自动分类（Categories/Tags） | GPT-4 API 调用 |
| FETCH-05 | URL 去重（JSON 文件） | Python json 模块 |
| FETCH-06 | 手动运行支持 | Python 脚本入口 |
| FETCH-07 | GitHub Actions 定时自动抓取 | .github/workflows/fetch-articles.yaml |
</phase_requirements>

---

## Standard Stack

### Core
| Library | Version | Purpose | Why Standard |
|---------|---------|---------|--------------|
| httpx | 0.28.1 | 异步 HTTP 客户端 | 现代 Python HTTP 库，支持同步/异步，2024 年主流选择 |
| beautifulsoup4 | 4.14.3 | HTML 解析 | Python 最流行的 HTML 解析库 |
| openai | >=1.0.0 | OpenAI API 客户端 | 官方 SDK，GPT-4 集成 |
| python-dotenv | >=1.0.0 | 环境变量管理 | 安全存储 API 密钥 |

### Supporting
| Library | Version | Purpose | When to Use |
|---------|---------|---------|-------------|
| PyGithub | >=2.0.0 | GitHub API 封装 | 需要更高级 GitHub API 操作时（可选） |
| python-dateutil | >=2.8.0 | 日期解析 | 处理各种日期格式 |
| requests | 2.32.5 | 备用 HTTP 库 | 简单同步场景（httpx 优先） |

### Alternatives Considered
| Instead of | Could Use | Tradeoff |
|------------|-----------|----------|
| httpx | requests | requests 更简单但不支持异步；httpx 是 future-proof 选择 |
| BeautifulSoup4 | lxml, parsel | lxml 更快但功能少；BS4 功能最全 |
| PyGithub | 直接调用 API | PyGithub 更易用但增加依赖；直接调用更轻量 |

**Installation:**
```bash
pip install httpx beautifulsoup4 openai python-dotenv python-dateutil
```

---

## Architecture Patterns

### Recommended Project Structure
```
scripts/
├── fetch_articles.py      # 主入口脚本
├── fetchers/
│   ├── __init__.py
│   ├── github_fetcher.py  # GitHub 仓库抓取
│   ├── blog_fetcher.py   # 博客抓取
│   └── base.py           # 基础 fetcher 类
├── formatters/
│   ├── __init__.py
│   └── openai_formatter.py # OpenAI 格式化
├── storage/
│   ├── __init__.py
│   └── url_store.py      # URL 去重存储
├── config.py             # 配置管理
└── main.py               # CLI 入口

.github/workflows/
└── fetch-articles.yaml   # GitHub Actions 工作流

data/
└── fetched_urls.json     # 已抓取 URL 记录

.env.example              # 环境变量示例
```

### Pattern 1: Fetcher 抽象基类
**What:** 定义统一的抓取接口，所有 fetcher 实现相同的方法签名
**When to use:** 需要支持多种数据源时
**Example:**
```python
# Source: 基于常见 Python 设计模式
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import List, Optional

@dataclass
class Article:
    url: str
    title: str
    content: str
    source: str
    created_at: Optional[str] = None

class BaseFetcher(ABC):
    @abstractmethod
    async def fetch(self, sources: List[str]) -> List[Article]:
        """抓取文章列表"""
        pass

    @abstractmethod
    def can_fetch(self, url: str) -> bool:
        """判断是否支持该 URL"""
        pass
```

### Pattern 2: URL 去重存储
**What:** 使用 JSON 文件存储已抓取 URL，实现增量更新
**When to use:** 需要避免重复抓取时
**Example:**
```python
# Source: 常见增量抓取模式
import json
from pathlib import Path
from typing import Set

class URLStore:
    def __init__(self, path: str = "data/fetched_urls.json"):
        self.path = Path(path)
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self._urls: Set[str] = self._load()

    def _load(self) -> Set[str]:
        if self.path.exists():
            with open(self.path) as f:
                data = json.load(f)
                return set(data.get("urls", []))
        return set()

    def save(self):
        with open(self.path, "w") as f:
            json.dump({"urls": list(self._urls), "updated": str(datetime.now())}, f, ensure_ascii=False, indent=2)

    def is_fetched(self, url: str) -> bool:
        return url in self._urls

    def add(self, url: str):
        self._urls.add(url)
```

### Pattern 3: OpenAI 格式化管道
**What:** 将原始内容发送给 OpenAI API，返回 Hugo Markdown 格式
**When to use:** 需要 AI 辅助格式化时
**Example:**
```python
# Source: OpenAI API 官方文档模式
from openai import OpenAI
from typing import Dict, Any

class OpenAIFormatter:
    def __init__(self, api_key: str, model: str = "gpt-4"):
        self.client = OpenAI(api_key=api_key)
        self.model = model

    def format_article(self, article: Article, target_dir: str) -> Dict[str, Any]:
        """使用 AI 分析内容并生成 Front Matter"""
        prompt = f"""你是一个 Hugo 博客助手。请分析以下文章内容，生成合适的 Front Matter 元数据。

文章信息：
- 标题: {article.title}
- 来源: {article.source}
- 原文链接: {article.url}

文章内容（前 2000 字）:
{article.content[:2000]}

请返回 JSON 格式的 Front Matter：
{{
    "title": "文章标题",
    "date": "2026-03-08",
    "categories": ["分类1", "分类2"],
    "tags": ["标签1", "标签2"],
    "description": "简短描述（100字以内）",
    "keywords": ["关键词1", "关键词2"]
}}

注意：categories 必须是以下之一：安装、进阶、常见问题、教程、源码解析
"""
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.3
        )
        return self._parse_response(response.choices[0].message.content)
```

### Anti-Patterns to Avoid
- **硬编码 API 密钥**: 永远使用环境变量或 .env 文件
- **同步阻塞抓取**: 使用 httpx 异步方式提高效率
- **忽略速率限制**: GitHub API 有 60 次/小时限制，需处理 429 错误
- **重复请求失败不重试**: 使用指数退避策略

---

## Don't Hand-Roll

| Problem | Don't Build | Use Instead | Why |
|---------|-------------|-------------|-----|
| HTTP 请求 | 自己写 socket 库 | httpx | 成熟的连接池、超时、重试机制 |
| HTML 解析 | 正则表达式 | BeautifulSoup4 | HTML 解析复杂，BS4 健壮 |
| OpenAI API | 自己调用原始 API | openai SDK | 官方 SDK 处理错误、重试、流式 |
| URL 去重 | 数据库 | JSON 文件 | 轻量简单，无需额外依赖 |

---

## Common Pitfalls

### Pitfall 1: GitHub API 速率限制
**What goes wrong:** 未认证请求 60 次/小时，认证后 5000 次/小时
**Why it happens:** GitHub API 保护机制
**How to avoid:**
1. 使用 `GITHUB_TOKEN` 环境变量（GitHub Actions 自动提供）
2. 添加 `X-GitHub-Api-Version` header
3. 实现指数退避重试
**Warning signs:** 收到 403/429 状态码

### Pitfall 2: OpenAI API 成本失控
**What goes wrong:** 大规模抓取导致 API 费用快速增加
**Why it happens:** GPT-4 API 费用较高（输入 $0.03/1K tokens，输出 $0.06/1K tokens）
**How to avoid:**
1. 设置每月预算限制
2. 限制每次请求的 content 长度（如前 2000 字）
3. 使用 gpt-4o-mini 处理简单分类
4. 实现缓存机制避免重复处理

### Pitfall 3: 内容质量参差不齐
**What goes wrong:** 抓取的低质量内容污染博客
**Why it happens:** 未对来源进行筛选
**How to avoid:**
1. 预设可信来源白名单
2. 检查内容长度（过短过滤）
3. 检查是否为广告/推广内容

### Pitfall 4: 中文编码问题
**What goes wrong:** 保存的 Markdown 文件出现乱码
**Why it happens:** 文件写入未指定 UTF-8 编码
**How to avoid:**
```python
# 始终指定编码
with open(filepath, 'w', encoding='utf-8') as f:
    f.write(content)
```

---

## Code Examples

### GitHub Issues 抓取
```python
# Source: GitHub REST API 官方文档
import httpx
import base64

async def fetch_github_issues(owner: str, repo: str, token: str = None):
    headers = {
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2022-11-28"
    }
    if token:
        headers["Authorization"] = f"Bearer {token}"

    async with httpx.AsyncClient() as client:
        # 获取 Issues
        response = await client.get(
            f"https://api.github.com/repos/{owner}/{repo}/issues",
            headers=headers,
            params={"state": "all", "per_page": 100, "sort": "updated"}
        )
        response.raise_for_status()
        issues = response.json()

        # 获取 README
        readme_response = await client.get(
            f"https://api.github.com/repos/{owner}/{repo}/readme",
            headers=headers,
            params={"ref": "main"}
        )
        if readme_response.status_code == 200:
            readme_data = readme_response.json()
            readme_content = base64.b64decode(readme_data["content"]).decode("utf-8")

        return issues, readme_content
```

### 博客文章抓取
```python
# Source: 常见爬虫模式
import httpx
from bs4 import BeautifulSoup
from typing import List, Dict

async def fetch_blog_article(url: str) -> Dict:
    async with httpx.AsyncClient() as client:
        response = await client.get(
            url,
            headers={"User-Agent": "Mozilla/5.0"},
            timeout=30.0
        )
        response.raise_for_status()

        soup = BeautifulSoup(response.text, "html.parser")

        # 提取标题
        title = soup.find("h1").text if soup.find("h1") else ""

        # 提取主要内容（移除脚本、样式等）
        for script in soup(["script", "style", "nav", "footer"]):
            script.decompose()

        content = soup.find("article") or soup.find("main") or soup.body
        article_text = content.get_text(separator="\n", strip=True)

        return {
            "url": url,
            "title": title,
            "content": article_text
        }
```

### Hugo Markdown 输出
```python
# Source: Hugo 官方文档 Front Matter 格式
from datetime import datetime
from pathlib import Path

def save_as_hugo_markdown(article: Dict, front_matter: Dict, output_dir: Path):
    """保存为 Hugo Markdown 格式"""
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    # 生成文件名（标题 slug）
    slug = article["title"].lower()
    slug = "".join(c if c.isalnum() or c in "- " else "" for c in slug)
    slug = "-".join(slug.split())[:50]

    filepath = output_dir / f"{slug}.md"

    # 构建 Front Matter
    fm_lines = ["---"]
    fm_lines.append(f'title: "{front_matter.get("title", article["title"])}"')
    fm_lines.append(f'date: {front_matter.get("date", datetime.now().strftime("%Y-%m-%d"))}')

    if front_matter.get("categories"):
        fm_lines.append("categories:")
        for cat in front_matter["categories"]:
            fm_lines.append(f"  - {cat}")

    if front_matter.get("tags"):
        fm_lines.append("tags:")
        for tag in front_matter["tags"]:
            fm_lines.append(f"  - {tag}")

    if front_matter.get("description"):
        fm_lines.append(f'description: "{front_matter["description"]}"')

    if front_matter.get("keywords"):
        fm_lines.append("keywords:")
        for kw in front_matter["keywords"]:
            fm_lines.append(f"  - {kw}")

    fm_lines.append("---\n")

    # 写入文件
    content = "\n".join(fm_lines) + article["content"]
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content)

    return filepath
```

---

## State of the Art

| Old Approach | Current Approach | When Changed | Impact |
|--------------|------------------|--------------|--------|
| requests 同步 | httpx 异步 | 2020 年 httpx 1.0 | 显著提升并发抓取效率 |
| 正则解析 HTML | BeautifulSoup4 | 2010 年代 | 更健壮的 HTML 处理 |
| 手动 API 调用 | openai SDK | 2023 年 | 简化集成，改善错误处理 |
| 数据库去重 | JSON 文件 | 本项目 | 轻量，无需额外依赖 |

**Deprecated/outdated:**
- `urllib.request`: 被 httpx 替代，功能不如 httpx 丰富
- `selenium`: 仅用于 JavaScript 渲染页面，本项目不需要

---

## Open Questions

1. **抓取来源配置**
   - What we know: 需要支持 GitHub Issues/PRs/README + 技术博客 URL
   - What's unclear: 具体要抓取哪些 GitHub 仓库？博客 URL 白名单？
   - Recommendation: 在 config.py 中定义可配置的来源列表

2. **分类 Categories 预定义**
   - What we know: 安装、进阶、常见问题、教程、源码解析
   - What's unclear: 是否需要增加其他分类？
   - Recommendation:  保持现有5 个分类，AI 负责映射

3. **OpenAI API 成本控制**
   - What we know: GPT-4 费用较高
   - What's unclear: 每日/每月抓取量预算？
   - Recommendation: 初期使用 gpt-4o-mini 降低成本，后续按需升级

---

## Validation Architecture

> Skip this section entirely if workflow.nyquist_validation is explicitly set to false in .planning/config.json. If the key is absent, treat as enabled.

### Test Framework
| Property | Value |
|----------|-------|
| Framework | pytest 8.x |
| Config file | pytest.ini (or pyproject.toml) |
| Quick run command | `pytest tests/ -x -v` |
| Full suite command | `pytest tests/ --cov=scripts --cov-report=html` |

### Phase Requirements -> Test Map
| Req ID | Behavior | Test Type | Automated Command | File Exists? |
|--------|----------|-----------|-------------------|-------------|
| FETCH-01 | GitHub Issues 抓取 | unit + integration | `pytest tests/test_github_fetcher.py -x` | 需要创建 |
| FETCH-02 | 博客文章抓取 | unit | `pytest tests/test_blog_fetcher.py -x` | 需要创建 |
| FETCH-03 | OpenAI 格式化 | unit (mock) | `pytest tests/test_formatter.py -x` | 需要创建 |
| FETCH-05 | URL 去重 | unit | `pytest tests/test_url_store.py -x` | 需要创建 |
| FETCH-06 | CLI 入口 | integration | `pytest tests/test_cli.py -x` | 需要创建 |

### Sampling Rate
- **Per task commit:** `pytest tests/ -x -v` (快速验证)
- **Per wave merge:** `pytest tests/ --cov=scripts` (完整覆盖)
- **Phase gate:** Full suite green before `/gsd:verify-work`

### Wave 0 Gaps
- [ ] `tests/test_github_fetcher.py` — 覆盖 FETCH-01
- [ ] `tests/test_blog_fetcher.py` — 覆盖 FETCH-02
- [ ] `tests/test_formatter.py` — 覆盖 FETCH-03
- [ ] `tests/test_url_store.py` — 覆盖 FETCH-05
- [ ] `tests/test_cli.py` — 覆盖 FETCH-06
- [ ] `tests/conftest.py` — 共享 fixtures
- [ ] Framework install: `pip install pytest pytest-asyncio pytest-cov` — 如果未安装

---

## Sources

### Primary (HIGH confidence)
- [GitHub REST API](https://docs.github.com/en/rest) - Issues、README API 端点
- [httpx 官方文档](https://www.python-httpx.org/) - 异步 HTTP 客户端
- [BeautifulSoup4 文档](https://www.crummy.com/software/BeautifulSoup/bs4/doc/) - HTML 解析
- [OpenAI Python SDK](https://github.com/openai/openai-python) - API 调用
- [Hugo Front Matter](https://gohugo.io/content-management/front-matter/) - 格式规范

### Secondary (MEDIUM confidence)
- [Python 爬虫最佳实践](https://realpython.com/python-web-scraping/) - 模式参考

### Tertiary (LOW confidence)
- 社区博客: 各种爬虫实现模式

---

## Metadata

**Confidence breakdown:**
- Standard stack: HIGH - 使用的都是主流 Python 库，有明确的版本号
- Architecture: HIGH - 基于常见设计模式，有明确的代码示例
- Pitfalls: HIGH - 基于官方文档和常见问题的总结
- Validation: MEDIUM - 测试策略基于 pytest 最佳实践

**Research date:** 2026-03-08
**Valid until:** 2026-04-08 (30 天)
