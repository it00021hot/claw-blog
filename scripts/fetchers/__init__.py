# Fetchers package
from scripts.fetchers.base import Article, BaseFetcher
from scripts.fetchers.blog_fetcher import BlogFetcher
from scripts.fetchers.github_fetcher import GitHubFetcher

__all__ = ["Article", "BaseFetcher", "BlogFetcher", "GitHubFetcher"]
