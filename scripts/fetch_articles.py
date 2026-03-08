"""
Main fetch orchestration script.
"""
import asyncio
import logging
import sys
from typing import List, Optional

from scripts.config import config
from scripts.fetchers.github_fetcher import GitHubFetcher
from scripts.fetchers.blog_fetcher import BlogFetcher
from scripts.formatters.openai_formatter import (
    OpenAIFormatter,
    save_as_hugo_markdown,
)
from scripts.storage.url_store import URLStore

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)


class FetchResult:
    """Result of fetch operation."""

    def __init__(self):
        self.success_count = 0
        self.skip_count = 0
        self.error_count = 0
        self.errors: List[str] = []

    def summary(self) -> str:
        return (
            f"Fetch complete: {self.success_count} succeeded, "
            f"{self.skip_count} skipped, {self.errors} errors"
        )


async def fetch_github_articles(
    url_store: URLStore,
    formatter: OpenAIFormatter,
    output_dir: str,
    dry_run: bool = False,
    verbose: bool = False,
) -> FetchResult:
    """Fetch articles from GitHub repositories."""
    result = FetchResult()

    fetcher = GitHubFetcher(token=config.github_token)

    for repo in config.github_repos:
        repo_url = f"https://github.com/{repo['owner']}/{repo['repo']}"

        # Fetch Issues
        try:
            if verbose:
                logger.info(f"Fetching issues from {repo_url}")
            articles = fetcher.fetch_issues(repo["owner"], repo["repo"])

            for article in articles:
                if url_store.is_fetched(article.url):
                    result.skip_count += 1
                    if verbose:
                        logger.info(f"Skipping already fetched: {article.url}")
                    continue

                try:
                    # Generate front matter
                    front_matter = formatter.format_article(article)

                    if not dry_run:
                        save_as_hugo_markdown(article, front_matter, output_dir)

                    url_store.add(article.url)
                    result.success_count += 1
                    if verbose:
                        logger.info(f"Fetched: {article.title}")
                except Exception as e:
                    result.error_count += 1
                    result.errors.append(f"Error processing {article.url}: {e}")
                    logger.error(f"Error processing {article.url}: {e}")
        except Exception as e:
            result.error_count += 1
            result.errors.append(f"Error fetching issues from {repo_url}: {e}")
            logger.error(f"Error fetching issues from {repo_url}: {e}")

        # Fetch README
        try:
            if verbose:
                logger.info(f"Fetching README from {repo_url}")
            readme = fetcher.fetch_readme(repo["owner"], repo["repo"])

            if readme and not url_store.is_fetched(readme.url):
                try:
                    front_matter = formatter.format_article(readme)

                    if not dry_run:
                        save_as_hugo_markdown(readme, front_matter, output_dir)

                    url_store.add(readme.url)
                    result.success_count += 1
                    if verbose:
                        logger.info(f"Fetched README: {readme.title}")
                except Exception as e:
                    result.error_count += 1
                    result.errors.append(f"Error processing README: {e}")
                    logger.error(f"Error processing README: {e}")
            elif readme:
                result.skip_count += 1
        except Exception as e:
            result.error_count += 1
            result.errors.append(f"Error fetching README: {e}")
            logger.error(f"Error fetching README: {e}")

    return result


async def fetch_blog_articles(
    url_store: URLStore,
    formatter: OpenAIFormatter,
    output_dir: str,
    dry_run: bool = False,
    verbose: bool = False,
) -> FetchResult:
    """Fetch articles from blogs."""
    result = FetchResult()

    fetcher = BlogFetcher()

    # Use configured specific blog URLs
    sources = config.blog_urls

    for url in sources:
        try:
            if verbose:
                logger.info(f"Fetching from {url}")

            articles = fetcher.fetch([url])

            for article in articles:
                if url_store.is_fetched(article.url):
                    result.skip_count += 1
                    if verbose:
                        logger.info(f"Skipping already fetched: {article.url}")
                    continue

                try:
                    front_matter = formatter.format_article(article)

                    if not dry_run:
                        save_as_hugo_markdown(article, front_matter, output_dir)

                    url_store.add(article.url)
                    result.success_count += 1
                    if verbose:
                        logger.info(f"Fetched: {article.title}")
                except Exception as e:
                    result.error_count += 1
                    result.errors.append(f"Error processing {article.url}: {e}")
                    logger.error(f"Error processing {article.url}: {e}")
        except Exception as e:
            result.error_count += 1
            result.errors.append(f"Error fetching from {url}: {e}")
            logger.error(f"Error fetching from {url}: {e}")

    return result


async def main(
    tech_only: bool = False,
    fiction_only: bool = False,
    dry_run: bool = False,
    verbose: bool = False,
) -> FetchResult:
    """Main async function to orchestrate all fetchers and formatters."""
    if verbose:
        logger.setLevel(logging.DEBUG)

    # Validate config
    try:
        config.validate()
    except ValueError as e:
        logger.error(f"Configuration error: {e}")
        sys.exit(1)

    # Initialize URL store
    url_store = URLStore()

    # Initialize formatter
    formatter = OpenAIFormatter()

    # Determine output directories
    tech_output = config.output_tech
    fiction_output = config.output_fiction

    total_result = FetchResult()

    # Fetch from GitHub repositories
    if not fiction_only:
        logger.info("Fetching from GitHub repositories...")
        tech_result = await fetch_github_articles(
            url_store, formatter, tech_output, dry_run, verbose
        )
        total_result.success_count += tech_result.success_count
        total_result.skip_count += tech_result.skip_count
        total_result.error_count += tech_result.error_count
        total_result.errors.extend(tech_result.errors)

    # Fetch from blogs (default to tech)
    if not fiction_only:
        logger.info("Fetching from blogs...")
        blog_result = await fetch_blog_articles(
            url_store, formatter, tech_output, dry_run, verbose
        )
        total_result.success_count += blog_result.success_count
        total_result.skip_count += blog_result.skip_count
        total_result.error_count += blog_result.error_count
        total_result.errors.extend(blog_result.errors)

    # Save URL store
    if not dry_run:
        url_store.save()
        logger.info("URL store saved")

    # Print summary
    logger.info(total_result.summary())

    return total_result


if __name__ == "__main__":
    asyncio.run(main())
