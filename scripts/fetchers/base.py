"""
Base fetcher abstract class and data models.
"""
from abc import ABC, abstractmethod
from dataclasses import dataclass
from datetime import datetime
from typing import List, Optional


@dataclass
class Article:
    """Article data model."""

    url: str
    title: str
    content: str
    source: str
    created_at: Optional[datetime] = None


class BaseFetcher(ABC):
    """Abstract base class for content fetchers."""

    @abstractmethod
    def fetch(self, sources: List[str]) -> List[Article]:
        """Fetch articles from sources."""
        pass

    @abstractmethod
    def can_fetch(self, url: str) -> bool:
        """Check if this fetcher can handle the given URL."""
        pass
