"""
URL storage for deduplication.
"""
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Set


class URLStore:
    """Store and track fetched URLs to avoid duplicates."""

    def __init__(self, path: str = "data/fetched_urls.json"):
        self.path = Path(path)
        self.urls: Set[str] = set()
        self._load()

    def _load(self) -> None:
        """Load URLs from JSON file."""
        if self.path.exists():
            try:
                with open(self.path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    self.urls = set(data.get("urls", []))
            except (json.JSONDecodeError, IOError):
                self.urls = set()
        else:
            self.urls = set()

    def is_fetched(self, url: str) -> bool:
        """Check if URL has been fetched."""
        return url in self.urls

    def add(self, url: str) -> None:
        """Add URL to the store."""
        self.urls.add(url)

    def save(self) -> None:
        """Save URLs to JSON file."""
        self.path.parent.mkdir(parents=True, exist_ok=True)
        data = {
            "urls": sorted(list(self.urls)),
            "updated": datetime.now(timezone.utc).isoformat(),
        }
        with open(self.path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
