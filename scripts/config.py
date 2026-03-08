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
    github_repos: List[dict] = field(default_factory=lambda: [
        {"owner": "example", "repo": "tech-blog"},
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
