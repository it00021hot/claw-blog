"""
Configuration module for content fetcher.
"""
import os
from dataclasses import dataclass, field
from typing import List
from dotenv import load_dotenv

load_dotenv()


@dataclass
class Config:
    """Configuration for content fetcher."""

    openai_api_key: str = field(default_factory=lambda: os.getenv("OPENAI_API_KEY", ""))
    openai_api_base: str = field(default_factory=lambda: os.getenv("OPENAI_API_BASE", ""))
    openai_model: str = field(default_factory=lambda: os.getenv("OPENAI_MODEL", "gpt-4o-mini"))
    github_token: str = field(default_factory=lambda: os.getenv("GITHUB_TOKEN", ""))
    output_tech: str = field(default_factory=lambda: os.getenv("OUTPUT_TECH", "content/tech/"))
    output_fiction: str = field(default_factory=lambda: os.getenv("OUTPUT_FICTION", "content/fiction/"))

    # GitHub repositories to fetch
    # 使用真实存在且有技术内容的仓库
    github_repos: List[dict] = field(default_factory=lambda: [
        {"owner": "kamranahmedse", "repo": "developer-roadmap"},  # 开发者路线图
        {"owner": "public-apis", "repo": "public-apis"},  # 免费 API 列表
        {"owner": "awesome-selfhosted", "repo": "awesome-selfhosted"},  # 自托管软件列表
        {"owner": "trimstray", "repo": "the-book-of-secret-knowledge"},  # 秘密知识手册
    ])

    # Specific blog article URLs to fetch
    # 真实的技术博客文章 URL
    blog_urls: List[str] = field(default_factory=lambda: [
        # Dev.to 热门文章
        "https://dev.to/mostafaedipour/building-a-rest-api-with-go-gin-and-postgresql-4bpb",
        "https://dev.to/clarke3326/understanding-react-server-components-1j0b",
        "https://dev.to/rajarshc-de/advanced-typescript-patterns-4-34m",
    ])

    # Blog URLs whitelist
    blog_whitelist: List[str] = field(default_factory=lambda: [
        "medium.com",
        "dev.to",
        "blog.dev",
        "zhihu.com",
    ])

    def validate(self) -> bool:
        """Validate required configuration."""
        if not self.openai_api_key:
            raise ValueError("OPENAI_API_KEY is required")
        return True


# Default config instance
config = Config()
