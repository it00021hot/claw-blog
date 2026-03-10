"""
Tests for resource formatter.
"""
import pytest
from unittest.mock import patch, MagicMock

from scripts.formatters.resource_formatter import (
    ResourceFormatter,
    map_category,
    CATEGORY_MAP,
    generate_slug,
    save_resource_as_markdown,
)
from scripts.parsers.typescript_parser import Resource


class TestMapCategory:
    """Test cases for map_category function."""

    def test_official_category(self):
        """Test mapping official category."""
        assert map_category("official") == ["官方资源"]

    def test_getting_started_category(self):
        """Test mapping getting-started category."""
        assert map_category("getting-started") == ["安装", "教程"]

    def test_channel_integration_category(self):
        """Test mapping channel-integration category."""
        assert map_category("channel-integration") == ["进阶"]

    def test_deep_dive_category(self):
        """Test mapping deep-dive category."""
        assert map_category("deep-dive") == ["源码解析"]

    def test_unknown_category(self):
        """Test mapping unknown category returns default."""
        assert map_category("unknown-category") == ["教程"]


class TestGenerateSlug:
    """Test cases for generate_slug function."""

    def test_simple_title(self):
        """Test generating slug from simple title."""
        slug = generate_slug("Hello World")
        assert slug == "hello-world"

    def test_title_with_special_chars(self):
        """Test generating slug from title with special characters."""
        slug = generate_slug("Hello, World! How are you?")
        assert "hello" in slug
        assert "world" in slug

    def test_title_with_chinese(self):
        """Test generating slug from title with Chinese characters."""
        slug = generate_slug("中文标题")
        assert len(slug) > 0
        # Should have hash prefix for Chinese
        assert "-" in slug or len(slug) == 8

    def test_title_length_limit(self):
        """Test slug is limited to 50 characters."""
        long_title = "A" * 100
        slug = generate_slug(long_title)
        assert len(slug) <= 50


class TestResourceFormatter:
    """Test cases for ResourceFormatter class."""

    def test_formatter_initialization(self):
        """Test formatter can be initialized."""
        formatter = ResourceFormatter()
        assert formatter is not None

    def test_format_resource_basic(self):
        """Test formatting a basic resource."""
        resource = Resource(
            title="Test Resource",
            desc="Test description",
            url="https://example.com",
            source="Example"
        )

        formatter = ResourceFormatter()
        front_matter = formatter.format_resource(resource)

        assert front_matter["title"] == "Test Resource"
        assert front_matter["description"] == "Test description"
        assert front_matter["original_url"] == "https://example.com"
        assert front_matter["source"] == "Example"
        assert front_matter["lang"] == "en"

    def test_format_resource_with_category(self):
        """Test formatting resource with category."""
        resource = Resource(
            title="Test Resource",
            desc="Test description",
            url="https://example.com",
            source="Example",
            category="deep-dive"
        )

        formatter = ResourceFormatter()
        front_matter = formatter.format_resource(resource)

        assert "源码解析" in front_matter["categories"]

    def test_format_resource_with_tags(self):
        """Test formatting resource with tags."""
        resource = Resource(
            title="Test Resource",
            desc="Test description",
            url="https://example.com",
            source="Example",
            tags=["tag1", "tag2"]
        )

        formatter = ResourceFormatter()
        front_matter = formatter.format_resource(resource)

        assert "tag1" in front_matter["tags"]
        assert "tag2" in front_matter["tags"]
        assert "Example" in front_matter["tags"]  # Source is also added as tag

    def test_format_resource_featured(self):
        """Test formatting resource with featured flag."""
        resource = Resource(
            title="Test Resource",
            desc="Test description",
            url="https://example.com",
            source="Example",
            featured=True
        )

        formatter = ResourceFormatter()
        front_matter = formatter.format_resource(resource)

        assert front_matter["featured"] == True

    def test_extract_keywords(self):
        """Test keyword extraction."""
        formatter = ResourceFormatter()
        keywords = formatter._extract_keywords(
            "OpenClaw AI Assistant Tutorial",
            "Learn how to build an AI assistant with OpenClaw"
        )

        # Should contain relevant tech keywords
        assert len(keywords) > 0
        assert any("OpenClaw" in kw or "AI" in kw or "Assistant" in kw for kw in keywords)


class TestSaveResourceAsMarkdown:
    """Test cases for save_resource_as_markdown function."""

    @patch("pathlib.Path.mkdir")
    @patch("pathlib.Path.exists")
    @patch("pathlib.Path.write_text")
    def test_save_basic_resource(self, mock_write, mock_exists, mock_mkdir):
        """Test saving a basic resource."""
        mock_exists.return_value = False

        resource = Resource(
            title="Test Resource",
            desc="Test description",
            url="https://example.com",
            source="Example"
        )

        front_matter = {
            "title": "Test Resource",
            "date": "2026-03-08",
            "categories": ["教程"],
        }

        result = save_resource_as_markdown(resource, front_matter, "/tmp/output")

        assert result is not None
        assert mock_write.called

    @patch("pathlib.Path.mkdir")
    @patch("pathlib.Path.exists")
    @patch("pathlib.Path.write_text")
    def test_save_with_duplicate_filename(self, mock_write, mock_exists, mock_mkdir):
        """Test saving resource with duplicate filename handling."""
        mock_exists.side_effect = [True, False]  # First exists, second doesn't

        resource = Resource(
            title="Test Resource",
            desc="Test description",
            url="https://example.com",
            source="Example"
        )

        front_matter = {"title": "Test Resource"}

        result = save_resource_as_markdown(resource, front_matter, "/tmp/output")

        assert result is not None
        # Should have been called with counter suffix
        assert mock_write.called
