"""
GitHub fetcher for Issues and README.
"""
import base64
import logging
from datetime import datetime
from typing import List, Optional

import httpx

from scripts.fetchers.base import Article, BaseFetcher
from scripts.config import config

logger = logging.getLogger(__name__)


class GitHubFetcher(BaseFetcher):
    """Fetch content from GitHub repositories."""

    def __init__(self, token: Optional[str] = None):
        self.token = token or config.github_token
        self.base_url = "https://api.github.com"

    def _get_headers(self) -> dict:
        """Get request headers."""
        headers = {
            "Accept": "application/vnd.github+json",
            "X-GitHub-Api-Version": "2022-11-28",
        }
        if self.token:
            headers["Authorization"] = f"Bearer {self.token}"
        return headers

    def can_fetch(self, url: str) -> bool:
        """Check if URL is a GitHub repository."""
        return "github.com" in url

    def fetch(self, sources: List[str]) -> List[Article]:
        """Fetch from GitHub sources."""
        articles = []
        for source in sources:
            try:
                # Parse owner/repo from URL
                parts = source.strip("/").split("/")
                if len(parts) >= 2:
                    owner, repo = parts[-2], parts[-1]
                    # Remove .git suffix
                    repo = repo.replace(".git", "")
                    articles.extend(self.fetch_issues(owner, repo))
            except Exception as e:
                logger.error(f"Error fetching {source}: {e}")
        return articles

    def fetch_issues(
        self, owner: str, repo: str, state: str = "all", per_page: int = 100
    ) -> List[Article]:
        """Fetch issues from a repository."""
        articles = []
        url = f"{self.base_url}/repos/{owner}/{repo}/issues"
        params = {"state": state, "per_page": per_page, "sort": "updated"}

        try:
            with httpx.Client(timeout=30.0) as client:
                response = client.get(url, headers=self._get_headers(), params=params)
                response.raise_for_status()
                issues = response.json()

                for issue in issues:
                    if "pull_request" in issue:
                        continue  # Skip PRs
                    article = Article(
                        url=issue.get("html_url", ""),
                        title=issue.get("title", ""),
                        content=issue.get("body", ""),
                        source=f"github:{owner}/{repo}",
                        created_at=datetime.fromisoformat(
                            issue.get("created_at", "").replace("Z", "+00:00")
                        )
                        if issue.get("created_at")
                        else None,
                    )
                    articles.append(article)
        except httpx.HTTPError as e:
            logger.error(f"HTTP error fetching issues: {e}")
        except Exception as e:
            logger.error(f"Error fetching issues: {e}")

        return articles

    def fetch_readme(self, owner: str, repo: str) -> Optional[Article]:
        """Fetch README from a repository."""
        url = f"{self.base_url}/repos/{owner}/{repo}/readme"

        try:
            with httpx.Client(timeout=30.0) as client:
                response = client.get(url, headers=self._get_headers())
                response.raise_for_status()
                data = response.json()

                # Decode base64 content
                content = base64.b64decode(data.get("content", "")).decode("utf-8")

                return Article(
                    url=f"https://github.com/{owner}/{repo}#readme",
                    title=f"{repo} README",
                    content=content,
                    source=f"github:{owner}/{repo}",
                    created_at=datetime.now(),
                )
        except httpx.HTTPError as e:
            logger.error(f"HTTP error fetching README: {e}")
        except Exception as e:
            logger.error(f"Error fetching README: {e}")

        return None
