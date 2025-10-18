"""Unit tests for core modules."""

import pytest
from pathlib import Path

from agent_extract.core.config import Config
from agent_extract.core.exceptions import (
    AgentExtractError,
    DocumentReadError,
    OCRError,
    ExtractionError,
    ValidationError,
)
from agent_extract.core.types import DocumentType, OutputFormat


class TestConfig:
    """Tests for Config class."""

    def test_default_config(self):
        """Test default configuration."""
        config = Config()
        assert config.app_name == "agent-extract"
        assert config.version == "0.1.0"
        assert config.ocr_engine == "paddle"

    def test_custom_config(self):
        """Test custom configuration."""
        config = Config(
            debug=True,
            max_file_size_mb=100,
            ocr_engine="tesseract",
        )
        assert config.debug is True
        assert config.max_file_size_mb == 100
        assert config.ocr_engine == "tesseract"

    def test_max_file_size_bytes(self):
        """Test max file size conversion to bytes."""
        config = Config(max_file_size_mb=10)
        assert config.max_file_size_bytes == 10 * 1024 * 1024


class TestExceptions:
    """Tests for custom exceptions."""

    def test_base_exception(self):
        """Test base AgentExtractError."""
        with pytest.raises(AgentExtractError):
            raise AgentExtractError("Test error")

    def test_document_read_error(self):
        """Test DocumentReadError."""
        with pytest.raises(DocumentReadError):
            raise DocumentReadError("Failed to read document")

    def test_ocr_error(self):
        """Test OCRError."""
        with pytest.raises(OCRError):
            raise OCRError("OCR failed")

    def test_extraction_error(self):
        """Test ExtractionError."""
        with pytest.raises(ExtractionError):
            raise ExtractionError("Extraction failed")

    def test_validation_error(self):
        """Test ValidationError."""
        with pytest.raises(ValidationError):
            raise ValidationError("Validation failed")


class TestTypes:
    """Tests for type definitions."""

    def test_document_type_enum(self):
        """Test DocumentType enum."""
        assert DocumentType.PDF.value == "pdf"
        assert DocumentType.DOCX.value == "docx"
        assert DocumentType.IMAGE.value == "image"

    def test_output_format_enum(self):
        """Test OutputFormat enum."""
        assert OutputFormat.JSON.value == "json"
        assert OutputFormat.MARKDOWN.value == "markdown"


