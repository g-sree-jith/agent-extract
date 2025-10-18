"""Unit tests for document readers."""

import pytest
from pathlib import Path

from agent_extract.readers.base import BaseReader
from agent_extract.readers.pdf_reader import PDFReader
from agent_extract.readers.docx_reader import DOCXReader
from agent_extract.readers.image_reader import ImageReader
from agent_extract.readers.factory import ReaderFactory
from agent_extract.core.exceptions import DocumentReadError, UnsupportedFormatError


class TestBaseReader:
    """Tests for BaseReader abstract class."""

    def test_supported_extensions(self):
        """Test that readers have supported extensions."""
        pdf_reader = PDFReader()
        assert ".pdf" in pdf_reader.supported_extensions

        docx_reader = DOCXReader()
        assert ".docx" in docx_reader.supported_extensions

        image_reader = ImageReader()
        assert ".png" in image_reader.supported_extensions


class TestPDFReader:
    """Tests for PDFReader."""

    def test_can_read_pdf(self):
        """Test that PDFReader can identify PDF files."""
        reader = PDFReader()
        pdf_path = Path("test.pdf")
        assert reader.can_read(pdf_path)

    def test_cannot_read_non_pdf(self):
        """Test that PDFReader rejects non-PDF files."""
        reader = PDFReader()
        docx_path = Path("test.docx")
        assert not reader.can_read(docx_path)


class TestDOCXReader:
    """Tests for DOCXReader."""

    def test_can_read_docx(self):
        """Test that DOCXReader can identify DOCX files."""
        reader = DOCXReader()
        docx_path = Path("test.docx")
        assert reader.can_read(docx_path)

    def test_cannot_read_non_docx(self):
        """Test that DOCXReader rejects non-DOCX files."""
        reader = DOCXReader()
        pdf_path = Path("test.pdf")
        assert not reader.can_read(pdf_path)


class TestImageReader:
    """Tests for ImageReader."""

    def test_can_read_images(self):
        """Test that ImageReader can identify image files."""
        reader = ImageReader()
        assert reader.can_read(Path("test.png"))
        assert reader.can_read(Path("test.jpg"))
        assert reader.can_read(Path("test.jpeg"))

    def test_cannot_read_non_images(self):
        """Test that ImageReader rejects non-image files."""
        reader = ImageReader()
        assert not reader.can_read(Path("test.pdf"))


class TestReaderFactory:
    """Tests for ReaderFactory."""

    def test_get_pdf_reader(self):
        """Test getting PDF reader from factory."""
        factory = ReaderFactory()
        reader = factory.get_reader(Path("test.pdf"))
        assert isinstance(reader, PDFReader)

    def test_get_docx_reader(self):
        """Test getting DOCX reader from factory."""
        factory = ReaderFactory()
        reader = factory.get_reader(Path("test.docx"))
        assert isinstance(reader, DOCXReader)

    def test_get_image_reader(self):
        """Test getting image reader from factory."""
        factory = ReaderFactory()
        reader = factory.get_reader(Path("test.png"))
        assert isinstance(reader, ImageReader)

    def test_unsupported_format_error(self):
        """Test that unsupported formats raise error."""
        factory = ReaderFactory()
        with pytest.raises(UnsupportedFormatError):
            factory.get_reader(Path("test.xyz"))

    def test_get_supported_formats(self):
        """Test getting supported formats."""
        factory = ReaderFactory()
        formats = factory.get_supported_formats()
        assert "PDF" in formats
        assert "DOCX" in formats
        assert "Image" in formats


