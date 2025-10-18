"""Unit tests for output formatters."""

import pytest
import json
from pathlib import Path

from agent_extract.outputs.json_formatter import JSONFormatter
from agent_extract.outputs.markdown_formatter import MarkdownFormatter
from agent_extract.core.types import (
    ExtractionResult,
    DocumentMetadata,
    DocumentType,
    ExtractedTable,
)


@pytest.fixture
def sample_extraction_result():
    """Create a sample extraction result for testing."""
    metadata = DocumentMetadata(
        filename="test.pdf",
        file_size=1024,
        document_type=DocumentType.PDF,
        page_count=2,
    )

    table = ExtractedTable(
        headers=["Name", "Age", "City"],
        rows=[
            ["Alice", "30", "NYC"],
            ["Bob", "25", "LA"],
        ],
    )

    return ExtractionResult(
        metadata=metadata,
        raw_text="This is a test document.\n\nIt has multiple paragraphs.",
        tables=[table],
        structured_data={"key": "value"},
    )


class TestJSONFormatter:
    """Tests for JSONFormatter."""

    def test_format_basic(self, sample_extraction_result):
        """Test basic JSON formatting."""
        formatter = JSONFormatter()
        result = formatter.format(sample_extraction_result)
        
        assert isinstance(result, str)
        assert len(result) > 0
        
        # Validate it's valid JSON
        data = json.loads(result)
        assert data["metadata"]["filename"] == "test.pdf"
        assert data["raw_text"] == "This is a test document.\n\nIt has multiple paragraphs."

    def test_format_compact(self, sample_extraction_result):
        """Test compact JSON formatting."""
        formatter = JSONFormatter()
        result = formatter.format_compact(sample_extraction_result)
        
        assert isinstance(result, str)
        assert "\n" not in result  # No newlines in compact format

    def test_format_pretty(self, sample_extraction_result):
        """Test pretty JSON formatting."""
        formatter = JSONFormatter()
        result = formatter.format_pretty(sample_extraction_result)
        
        assert isinstance(result, str)
        assert "    " in result  # Has indentation


class TestMarkdownFormatter:
    """Tests for MarkdownFormatter."""

    def test_format_basic(self, sample_extraction_result):
        """Test basic Markdown formatting."""
        formatter = MarkdownFormatter()
        result = formatter.format(sample_extraction_result)
        
        assert isinstance(result, str)
        assert len(result) > 0
        assert "# test.pdf" in result  # Title
        assert "## Content" in result  # Content section
        assert "## Tables" in result  # Tables section

    def test_format_without_metadata(self, sample_extraction_result):
        """Test Markdown formatting without metadata."""
        formatter = MarkdownFormatter(include_metadata=False)
        result = formatter.format(sample_extraction_result)
        
        assert "## Metadata" not in result

    def test_table_formatting(self, sample_extraction_result):
        """Test that tables are formatted correctly."""
        formatter = MarkdownFormatter()
        result = formatter.format(sample_extraction_result)
        
        # Check for markdown table syntax
        assert "| Name | Age | City |" in result
        assert "| --- | --- | --- |" in result
        assert "| Alice | 30 | NYC |" in result


