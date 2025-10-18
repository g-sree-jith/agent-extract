"""Factory for creating appropriate document readers."""

from pathlib import Path
from typing import Optional

from agent_extract.readers.base import BaseReader
from agent_extract.readers.pdf_reader import PDFReader
from agent_extract.readers.docx_reader import DOCXReader
from agent_extract.readers.image_reader import ImageReader
from agent_extract.core.exceptions import UnsupportedFormatError


class ReaderFactory:
    """Factory for creating document readers based on file type."""

    def __init__(self, ocr_engine=None):
        """
        Initialize the reader factory.
        
        Args:
            ocr_engine: OCR engine instance for image reading
        """
        self.ocr_engine = ocr_engine
        self._readers = [
            PDFReader(),
            DOCXReader(),
            ImageReader(ocr_engine=ocr_engine),
        ]

    def get_reader(self, file_path: Path) -> BaseReader:
        """
        Get appropriate reader for the given file.

        Args:
            file_path: Path to the document file

        Returns:
            BaseReader instance that can handle the file

        Raises:
            UnsupportedFormatError: If no reader can handle the file
        """
        if not isinstance(file_path, Path):
            file_path = Path(file_path)

        for reader in self._readers:
            if reader.can_read(file_path):
                return reader

        raise UnsupportedFormatError(
            f"No reader found for file: {file_path}. "
            f"Supported extensions: {self._get_supported_extensions()}"
        )

    def _get_supported_extensions(self) -> set[str]:
        """Get all supported file extensions."""
        extensions = set()
        for reader in self._readers:
            extensions.update(reader.supported_extensions)
        return extensions

    def get_supported_formats(self) -> dict[str, list[str]]:
        """
        Get information about supported formats.

        Returns:
            Dictionary mapping reader types to supported extensions
        """
        return {
            "PDF": list(PDFReader().supported_extensions),
            "DOCX": list(DOCXReader().supported_extensions),
            "Image": list(ImageReader().supported_extensions),
        }


