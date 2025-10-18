"""Base reader abstract class for all document readers."""

from abc import ABC, abstractmethod
from pathlib import Path
from typing import Optional
import mimetypes
from datetime import datetime

from agent_extract.core.types import (
    DocumentType,
    DocumentMetadata,
    ExtractionResult,
)
from agent_extract.core.exceptions import DocumentReadError


class BaseReader(ABC):
    """Abstract base class for document readers."""

    def __init__(self):
        """Initialize the reader."""
        self.supported_extensions: set[str] = set()
        self.supported_mime_types: set[str] = set()

    @abstractmethod
    def read(self, file_path: Path) -> ExtractionResult:
        """
        Read and extract content from a document.

        Args:
            file_path: Path to the document file

        Returns:
            ExtractionResult containing extracted data

        Raises:
            DocumentReadError: If the document cannot be read
        """
        pass

    def can_read(self, file_path: Path) -> bool:
        """
        Check if this reader can handle the given file.

        Args:
            file_path: Path to the document file

        Returns:
            True if this reader can handle the file, False otherwise
        """
        extension = file_path.suffix.lower()
        mime_type = self._get_mime_type(file_path)

        return (
            extension in self.supported_extensions
            or mime_type in self.supported_mime_types
        )

    def _get_mime_type(self, file_path: Path) -> Optional[str]:
        """Get MIME type of the file."""
        mime_type, _ = mimetypes.guess_type(str(file_path))
        return mime_type

    def _validate_file(self, file_path: Path) -> None:
        """
        Validate that the file exists and is readable.

        Args:
            file_path: Path to the document file

        Raises:
            DocumentReadError: If the file is invalid
        """
        if not file_path.exists():
            raise DocumentReadError(f"File not found: {file_path}")

        if not file_path.is_file():
            raise DocumentReadError(f"Not a file: {file_path}")

        if not file_path.stat().st_size > 0:
            raise DocumentReadError(f"File is empty: {file_path}")

    def _create_metadata(
        self,
        file_path: Path,
        document_type: DocumentType,
        page_count: Optional[int] = None,
        **kwargs,
    ) -> DocumentMetadata:
        """
        Create document metadata.

        Args:
            file_path: Path to the document file
            document_type: Type of the document
            page_count: Number of pages in the document
            **kwargs: Additional metadata fields

        Returns:
            DocumentMetadata object
        """
        stat = file_path.stat()
        mime_type = self._get_mime_type(file_path)

        return DocumentMetadata(
            filename=file_path.name,
            file_size=stat.st_size,
            document_type=document_type,
            mime_type=mime_type,
            page_count=page_count,
            modified_date=datetime.fromtimestamp(stat.st_mtime),
            **kwargs,
        )


