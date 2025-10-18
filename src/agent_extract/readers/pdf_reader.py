"""PDF document reader using PyMuPDF and pdfplumber."""

import time
from pathlib import Path
from typing import List, Optional
import fitz  # PyMuPDF
import pdfplumber

from agent_extract.core.types import (
    DocumentType,
    ExtractionResult,
    ExtractedTable,
    BoundingBox,
)
from agent_extract.core.exceptions import DocumentReadError
from agent_extract.readers.base import BaseReader


class PDFReader(BaseReader):
    """Reader for PDF documents."""

    def __init__(self):
        """Initialize the PDF reader."""
        super().__init__()
        self.supported_extensions = {".pdf"}
        self.supported_mime_types = {"application/pdf"}

    def read(self, file_path: Path) -> ExtractionResult:
        """
        Read and extract content from a PDF document.

        Args:
            file_path: Path to the PDF file

        Returns:
            ExtractionResult containing extracted data

        Raises:
            DocumentReadError: If the PDF cannot be read
        """
        start_time = time.time()
        self._validate_file(file_path)

        try:
            # Extract text using PyMuPDF (faster)
            raw_text = self._extract_text_pymupdf(file_path)
            
            # Extract tables using pdfplumber (more accurate for tables)
            tables = self._extract_tables_pdfplumber(file_path)
            
            # Get metadata
            metadata = self._get_pdf_metadata(file_path)
            
            processing_time = time.time() - start_time

            return ExtractionResult(
                metadata=metadata,
                raw_text=raw_text,
                tables=tables,
                processing_time=processing_time,
                extraction_method="pdf_hybrid",
            )

        except Exception as e:
            raise DocumentReadError(f"Failed to read PDF {file_path}: {str(e)}") from e

    def _extract_text_pymupdf(self, file_path: Path) -> str:
        """Extract text from PDF using PyMuPDF."""
        text_parts = []

        try:
            with fitz.open(file_path) as doc:
                for page_num, page in enumerate(doc, start=1):
                    text = page.get_text()
                    if text.strip():
                        text_parts.append(f"--- Page {page_num} ---\n{text}")

            return "\n\n".join(text_parts)

        except Exception as e:
            raise DocumentReadError(f"PyMuPDF extraction failed: {str(e)}") from e

    def _extract_tables_pdfplumber(self, file_path: Path) -> List[ExtractedTable]:
        """Extract tables from PDF using pdfplumber."""
        tables = []

        try:
            with pdfplumber.open(file_path) as pdf:
                for page_num, page in enumerate(pdf.pages, start=1):
                    page_tables = page.extract_tables()
                    
                    for table_data in page_tables:
                        if not table_data or len(table_data) < 2:
                            continue

                        # First row as headers
                        headers = [str(cell) if cell else "" for cell in table_data[0]]
                        
                        # Remaining rows as data
                        rows = [
                            [str(cell) if cell else "" for cell in row]
                            for row in table_data[1:]
                        ]

                        tables.append(
                            ExtractedTable(
                                headers=headers,
                                rows=rows,
                                page=page_num,
                            )
                        )

            return tables

        except Exception as e:
            # Table extraction is optional, don't fail if it doesn't work
            print(f"Warning: Table extraction failed: {str(e)}")
            return []

    def _get_pdf_metadata(self, file_path: Path) -> "DocumentMetadata":
        """Get metadata from PDF."""
        try:
            with fitz.open(file_path) as doc:
                metadata_dict = doc.metadata
                page_count = len(doc)

                return self._create_metadata(
                    file_path=file_path,
                    document_type=DocumentType.PDF,
                    page_count=page_count,
                    title=metadata_dict.get("title"),
                    author=metadata_dict.get("author"),
                )

        except Exception as e:
            # Fallback to basic metadata if extraction fails
            return self._create_metadata(
                file_path=file_path,
                document_type=DocumentType.PDF,
            )


