"""
Tests for TypeScript parser.
"""
import pytest

from scripts.parsers.typescript_parser import Resource, parse_resources


class TestParseResources:
    """Test cases for parse_resources function."""

    def test_parse_single_resource(self):
        """Test parsing a single resource object."""
        content = """
        export const resources = [
            {
                title: 'Test Resource',
                desc: 'This is a test description',
                url: 'https://example.com',
                source: 'Example',
                lang: 'en',
                category: 'official',
                featured: false,
                tags: ['test', 'example']
            }
        ];
        """

        resources = parse_resources(content)

        assert len(resources) == 1
        assert resources[0].title == "Test Resource"
        assert resources[0].desc == "This is a test description"
        assert resources[0].url == "https://example.com"
        assert resources[0].source == "Example"
        assert resources[0].lang == "en"
        assert resources[0].category == "official"
        assert resources[0].featured == False

    def test_parse_multiple_resources(self):
        """Test parsing multiple resource objects."""
        content = """
        const resources = [
            {
                title: 'First Resource',
                desc: 'First description',
                url: 'https://first.com',
                source: 'First',
            },
            {
                title: 'Second Resource',
                desc: 'Second description',
                url: 'https://second.com',
                source: 'Second',
            }
        ];
        """

        resources = parse_resources(content)

        assert len(resources) == 2
        assert resources[0].title == "First Resource"
        assert resources[1].title == "Second Resource"

    def test_parse_with_optional_fields(self):
        """Test parsing resources with optional fields missing."""
        content = """
        const resources = [
            {
                title: 'Minimal Resource',
                desc: 'Minimal description',
                url: 'https://minimal.com',
                source: 'Minimal',
            }
        ];
        """

        resources = parse_resources(content)

        assert len(resources) == 1
        assert resources[0].lang == "en"  # Default
        assert resources[0].category == "official"  # Default
        assert resources[0].featured == False  # Default
        assert resources[0].tags == []  # Empty list

    def test_parse_with_double_quotes(self):
        """Test parsing resources with double quotes."""
        content = '''
        const resources = [
            {
                title: "Double Quoted Title",
                desc: "Double quoted description",
                url: "https://example.com",
                source: "Example",
            }
        ];
        '''

        resources = parse_resources(content)

        assert len(resources) == 1
        assert resources[0].title == "Double Quoted Title"

    def test_parse_with_special_characters(self):
        """Test parsing resources with special characters in fields."""
        content = """
        const resources = [
            {
                title: 'Resource with \"quotes\"',
                desc: 'Description with apostrophe\'s test',
                url: 'https://example.com/path?param=value',
                source: 'Example & Co.',
            }
        ];
        """

        resources = parse_resources(content)

        assert len(resources) == 1
        assert "quotes" in resources[0].title
        assert "apostrophe" in resources[0].desc

    def test_parse_empty_content(self):
        """Test parsing empty content."""
        content = ""
        resources = parse_resources(content)
        assert resources == []

    def test_parse_no_matches(self):
        """Test parsing content with no valid resources."""
        content = """
        const data = {
            name: "test",
            value: 123
        };
        """
        resources = parse_resources(content)
        assert resources == []


class TestResourceDataclass:
    """Test cases for Resource dataclass."""

    def test_resource_creation(self):
        """Test creating a Resource object."""
        resource = Resource(
            title="Test",
            desc="Description",
            url="https://example.com",
            source="Example"
        )
        assert resource.title == "Test"
        assert resource.desc == "Description"
        assert resource.lang == "en"  # Default
        assert resource.tags == []  # Default empty list

    def test_resource_with_tags(self):
        """Test Resource with custom tags."""
        resource = Resource(
            title="Test",
            desc="Description",
            url="https://example.com",
            source="Example",
            tags=["tag1", "tag2"]
        )
        assert resource.tags == ["tag1", "tag2"]

    def test_resource_featured_default(self):
        """Test Resource featured field defaults to False."""
        resource = Resource(
            title="Test",
            desc="Description",
            url="https://example.com",
            source="Example"
        )
        assert resource.featured == False
