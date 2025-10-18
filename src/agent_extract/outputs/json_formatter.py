"""JSON output formatter for extraction results."""

import json
from pathlib import Path
from typing import Any, Dict, Optional
from datetime import datetime

from agent_extract.core.types import ExtractionResult, OutputFormat
from agent_extract.core.exceptions import ValidationError


class JSONFormatter:
    """Format extraction results as JSON."""

    def __init__(self, indent: int = 2, ensure_ascii: bool = False):
        """
        Initialize JSON formatter.

        Args:
            indent: Number of spaces for indentation
            ensure_ascii: Whether to escape non-ASCII characters
        """
        self.indent = indent
        self.ensure_ascii = ensure_ascii

    def format(self, result: ExtractionResult) -> str:
        """
        Format extraction result as JSON string.

        Args:
            result: ExtractionResult to format

        Returns:
            JSON string

        Raises:
            ValidationError: If formatting fails
        """
        try:
            # Convert Pydantic model to dict
            data = self._prepare_data(result)
            
            # Serialize to JSON
            json_str = json.dumps(
                data,
                indent=self.indent,
                ensure_ascii=self.ensure_ascii,
                default=self._json_serializer,
            )
            
            return json_str

        except Exception as e:
            raise ValidationError(f"Failed to format as JSON: {str(e)}") from e

    def format_to_file(self, result: ExtractionResult, output_path: Path) -> None:
        """
        Format and save extraction result to a JSON file.

        Args:
            result: ExtractionResult to format
            output_path: Path to save the JSON file

        Raises:
            ValidationError: If formatting or saving fails
        """
        try:
            json_str = self.format(result)
            output_path.write_text(json_str, encoding="utf-8")
        except Exception as e:
            raise ValidationError(f"Failed to save JSON to file: {str(e)}") from e

    def _prepare_data(self, result: ExtractionResult) -> Dict[str, Any]:
        """
        Prepare extraction result data for JSON serialization.

        Args:
            result: ExtractionResult to prepare

        Returns:
            Dictionary ready for JSON serialization
        """
        # Convert to dict using Pydantic's model_dump
        data = result.model_dump()
        
        # Add format metadata
        data["output_format"] = OutputFormat.JSON.value
        data["generated_at"] = datetime.now().isoformat()
        
        return data

    @staticmethod
    def _json_serializer(obj):
        """Custom JSON serializer for complex types."""
        if isinstance(obj, datetime):
            return obj.isoformat()
        elif isinstance(obj, Path):
            return str(obj)
        elif hasattr(obj, "__dict__"):
            return obj.__dict__
        else:
            return str(obj)

    def format_compact(self, result: ExtractionResult) -> str:
        """
        Format extraction result as compact JSON (no indentation).

        Args:
            result: ExtractionResult to format

        Returns:
            Compact JSON string
        """
        data = self._prepare_data(result)
        return json.dumps(data, ensure_ascii=self.ensure_ascii, default=self._json_serializer)

    def format_pretty(self, result: ExtractionResult) -> str:
        """
        Format extraction result as pretty-printed JSON.

        Args:
            result: ExtractionResult to format

        Returns:
            Pretty-printed JSON string
        """
        data = self._prepare_data(result)
        return json.dumps(
            data,
            indent=4,
            ensure_ascii=self.ensure_ascii,
            default=self._json_serializer,
            sort_keys=True,
        )


