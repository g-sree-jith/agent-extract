"""Markdown output formatter for extraction results."""

from pathlib import Path
from typing import List
from datetime import datetime

from agent_extract.core.types import ExtractionResult, ExtractedTable, OutputFormat
from agent_extract.core.exceptions import ValidationError


class MarkdownFormatter:
    """Format extraction results as Markdown."""

    def __init__(self, include_metadata: bool = True):
        """
        Initialize Markdown formatter.

        Args:
            include_metadata: Whether to include metadata section
        """
        self.include_metadata = include_metadata

    def format(self, result: ExtractionResult) -> str:
        """
        Format extraction result as Markdown string.

        Args:
            result: ExtractionResult to format

        Returns:
            Markdown string

        Raises:
            ValidationError: If formatting fails
        """
        try:
            sections = []

            # Title
            title = result.metadata.title or result.metadata.filename
            sections.append(f"# {title}\n")

            # Metadata section
            if self.include_metadata:
                sections.append(self._format_metadata(result))

            # Main content
            if result.raw_text:
                sections.append("## Content\n")
                sections.append(result.raw_text)
                sections.append("\n")

            # Tables
            if result.tables:
                sections.append("## Tables\n")
                for i, table in enumerate(result.tables, start=1):
                    sections.append(f"### Table {i}\n")
                    sections.append(self._format_table(table))
                    sections.append("\n")

            # Structured data
            if result.structured_data:
                sections.append("## Structured Data\n")
                sections.append(self._format_structured_data(result.structured_data))
                sections.append("\n")

            # Entities
            if result.entities:
                sections.append("## Extracted Entities\n")
                sections.append(self._format_entities(result))
                sections.append("\n")

            # Footer
            sections.append(self._format_footer(result))

            return "\n".join(sections)

        except Exception as e:
            raise ValidationError(f"Failed to format as Markdown: {str(e)}") from e

    def format_to_file(self, result: ExtractionResult, output_path: Path) -> None:
        """
        Format and save extraction result to a Markdown file.

        Args:
            result: ExtractionResult to format
            output_path: Path to save the Markdown file

        Raises:
            ValidationError: If formatting or saving fails
        """
        try:
            markdown_str = self.format(result)
            output_path.write_text(markdown_str, encoding="utf-8")
        except Exception as e:
            raise ValidationError(f"Failed to save Markdown to file: {str(e)}") from e

    def _format_metadata(self, result: ExtractionResult) -> str:
        """Format metadata section."""
        lines = ["## Metadata\n"]
        metadata = result.metadata

        fields = [
            ("Filename", metadata.filename),
            ("Document Type", metadata.document_type.value.upper()),
            ("File Size", f"{metadata.file_size:,} bytes"),
            ("Pages", metadata.page_count),
            ("Author", metadata.author),
            ("Language", metadata.language),
            ("Processing Time", f"{result.processing_time:.2f}s" if result.processing_time else None),
            ("Extraction Method", result.extraction_method),
        ]

        for label, value in fields:
            if value is not None:
                lines.append(f"- **{label}**: {value}")

        lines.append("\n")
        return "\n".join(lines)

    def _format_table(self, table: ExtractedTable) -> str:
        """Format a single table in Markdown."""
        if not table.rows:
            return "*Empty table*\n"

        lines = []

        # Headers
        if table.headers:
            lines.append("| " + " | ".join(table.headers) + " |")
            lines.append("| " + " | ".join(["---"] * len(table.headers)) + " |")

        # Rows
        for row in table.rows:
            lines.append("| " + " | ".join(str(cell) for cell in row) + " |")

        return "\n".join(lines) + "\n"

    def _format_structured_data(self, data: dict) -> str:
        """Format structured data as a list."""
        lines = []
        for key, value in data.items():
            if isinstance(value, (list, dict)):
                lines.append(f"- **{key}**:")
                lines.append(f"  ```json")
                import json
                lines.append(f"  {json.dumps(value, indent=2)}")
                lines.append(f"  ```")
            else:
                lines.append(f"- **{key}**: {value}")
        return "\n".join(lines)

    def _format_entities(self, result: ExtractionResult) -> str:
        """Format extracted entities."""
        lines = []
        for entity in result.entities:
            confidence = f" ({entity.confidence:.2%})" if entity.confidence else ""
            lines.append(f"- **{entity.entity_type}**: {entity.text}{confidence}")
        return "\n".join(lines)

    def _format_footer(self, result: ExtractionResult) -> str:
        """Format footer with generation info."""
        lines = [
            "---\n",
            f"*Generated by Agent-Extract on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*",
        ]
        
        if result.confidence_score:
            lines.append(f"*Confidence Score: {result.confidence_score:.2%}*")
        
        return "\n".join(lines)


