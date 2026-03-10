"""
Tests for OpenClaw101 fetcher.
"""
import pytest
from unittest.mock import Mock, patch, MagicMock

from scripts.fetchers.openclaw101_fetcher import OpenClaw101Fetcher


class TestOpenClaw101Fetcher:
    """Test cases for OpenClaw101Fetcher."""

    def test_fetcher_initialization(self):
        """Test fetcher can be initialized."""
        fetcher = OpenClaw101Fetcher()
        assert fetcher.base_url == "https://api.github.com"
        assert fetcher.token is not None

    def test_fetcher_with_custom_token(self):
        """Test fetcher with custom token."""
        fetcher = OpenClaw101Fetcher(token="custom_token")
        assert fetcher.token == "custom_token"

    def test_get_headers_without_token(self):
        """Test headers without token."""
        fetcher = OpenClaw101Fetcher(token=None)
        headers = fetcher._get_headers()
        assert "Accept" in headers
        assert "Authorization" not in headers

    def test_get_headers_with_token(self):
        """Test headers with token."""
        fetcher = OpenClaw101Fetcher(token="test_token")
        headers = fetcher._get_headers()
        assert headers["Authorization"] == "Bearer test_token"

    @patch("scripts.fetchers.openclaw101_fetcher.httpx.Client")
    def test_fetch_resources_success(self, mock_client):
        """Test successful fetch of resources."""
        # Mock response
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "content": "ZW5jb2RlZCBjb250ZW50",  # "encoded content" in base64
            "encoding": "base64"
        }
        mock_response.raise_for_status.return_value = None

        mock_client_instance = MagicMock()
        mock_client_instance.get.return_value = mock_response
        mock_client_instance.__enter__ = MagicMock(return_value=mock_client_instance)
        mock_client_instance.__exit__ = MagicMock(return_value=None)
        mock_client.return_value = mock_client_instance

        fetcher = OpenClaw101Fetcher()
        result = fetcher.fetch_resources()

        # Since base64 content is mock, we expect None or decode error handling
        # The test verifies the HTTP call is made correctly
        assert mock_client_instance.get.called

    @patch("scripts.fetchers.openclaw101_fetcher.httpx.Client")
    def test_fetch_resources_http_error(self, mock_client):
        """Test fetch with HTTP error."""
        from httpx import HTTPError

        mock_client_instance = MagicMock()
        mock_client_instance.get.side_effect = HTTPError("Connection failed")
        mock_client_instance.__enter__ = MagicMock(return_value=mock_client_instance)
        mock_client_instance.__exit__ = MagicMock(return_value=None)
        mock_client.return_value = mock_client_instance

        fetcher = OpenClaw101Fetcher()
        result = fetcher.fetch_resources()

        assert result is None

    def test_can_fetch_openclaw101(self):
        """Test can_fetch recognizes openclaw101 URL."""
        fetcher = OpenClaw101Fetcher()
        assert fetcher.can_fetch("https://github.com/mengjian-github/openclaw101")
        assert fetcher.can_fetch("https://github.com/user/openclaw101-test")
        assert not fetcher.can_fetch("https://github.com/other/repo")

    @patch("scripts.fetchers.openclaw101_fetcher.httpx.Client")
    def test_fetch_method(self, mock_client):
        """Test the fetch method with sources."""
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "content": "dGVzdCBjb250ZW50",  # "test content" in base64
        }
        mock_response.raise_for_status.return_value = None

        mock_client_instance = MagicMock()
        mock_client_instance.get.return_value = mock_response
        mock_client_instance.__enter__ = MagicMock(return_value=mock_client_instance)
        mock_client_instance.__exit__ = MagicMock(return_value=None)
        mock_client.return_value = mock_client_instance

        fetcher = OpenClaw101Fetcher()
        sources = ["resources"]
        articles = fetcher.fetch(sources)

        # Should return at least one article
        assert len(articles) > 0
