"""
Blog fetcher for technical articles.
"""
import logging
from typing import List, Optional
from urllib.parse import urlparse

import httpx
from bs4 import BeautifulSoup

from scripts.fetchers.base import Article, BaseFetcher
from scripts.config import config

logger = logging.getLogger(__name__)


class BlogFetcher(BaseFetcher):
    """Fetch articles from technical blogs."""

    def __init__(self):
        self.whitelist = config.blog_whitelist

    def can_fetch(self, url: str) -> bool:
        """Check if URL is in the whitelist."""
        try:
            parsed = urlparse(url)
            domain = parsed.netloc.lower()
            # Remove www. prefix
            if domain.startswith("www."):
                domain = domain[4:]
            return any(domain.endswith(allowed) for allowed in self.whitelist)
        except Exception:
            return False

    def fetch(self, sources: List[str]) -> List[Article]:
        """Fetch articles from blog URLs."""
        articles = []
        for url in sources:
            if self.can_fetch(url):
                article = self.fetch_article(url)
                if article:
                    articles.append(article)
        return articles

    def fetch_article(self, url: str) -> Optional[Article]:
        """Fetch a single article from URL."""
        headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        }

        try:
            with httpx.Client(timeout=30.0, follow_redirects=True) as client:
                response = client.get(url, headers=headers)
                response.raise_for_status()

                soup = BeautifulSoup(response.text, "html.parser")

                # Remove unwanted elements
                for tag in soup(["script", "style", "nav", "footer", "aside", "header"]):
                    tag.decompose()

                # Extract title
                title = ""
                h1 = soup.find("h1")
                if h1:
                    title = h1.get_text(strip=True)
                if not title:
                    title_tag = soup.find("title")
                    if title_tag:
                        title = title_tag.get_text(strip=True)

                # Extract content
                article_tag = soup.find("article") or soup.find("main") or soup.find("body")
                content = ""
                if article_tag:
                    content = article_tag.get_text(separator="\n", strip=True)
                    # Limit content length
                    content = content[:10000]

                if not title and not content:
                    logger.warning(f"No content extracted from {url}")
                    return None

                # Get domain as source
                parsed = urlparse(url)
                source = parsed.netloc

                return Article(
                    url=url,
                    title=title,
                    content=content,
                    source=source,
                )

        except httpx.HTTPError as e:
            logger.error(f"HTTP error fetching {url}: {e}")
        except Exception as e:
            logger.error(f"Error fetching {url}: {e}")

        return None
