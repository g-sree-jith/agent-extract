"""DOCX document reader using python-docx."""

import time
from pathlib import Path
from typing import List
from docx import Document
from docx.table import Table as DocxTable
from docx.oxml.table import CT_Tbl
from docx.oxml.text.paragraph import CT_P

from agent_extract.core.types import (
    DocumentType,
    ExtractionResult,
    ExtractedTable,
)
from agent_extract.core.exceptions import DocumentReadError
from agent_extract.readers.base import BaseReader


class DOCXReader(BaseReader):
    """Reader for DOCX documents."""

    def __init__(self):
        """Initialize the DOCX reader."""
        super().__init__()
        self.supported_extensions = {".docx"}
        self.supported_mime_types = {
            "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
        }

    def read(self, file_path: Path) -> ExtractionResult:
        """
        Read and extract content from a DOCX document.

        Args:
            file_path: Path to the DOCX file

        Returns:
            ExtractionResult containing extracted data

        Raises:
            DocumentReadError: If the DOCX cannot be read
        """
        start_time = time.time()
        self._validate_file(file_path)

        try:
            doc = Document(file_path)
            
            # Extract text and tables in document order
            raw_text, tables = self._extract_content(doc)
            
            # Get metadata
            metadata = self._get_docx_metadata(file_path, doc)
            
            processing_time = time.time() - start_time

            return ExtractionResult(
                metadata=metadata,
                raw_text=raw_text,
                tables=tables,
                processing_time=processing_time,
                extraction_method="docx",
            )

        except Exception as e:
            raise DocumentReadError(f"Failed to read DOCX {file_path}: {str(e)}") from e

    def _extract_content(self, doc: Document) -> tuple[str, List[ExtractedTable]]:
        """Extract text and tables in document order."""
        text_parts = []
        tables = []
        
        # Iterate through document elements in order
        for element in doc.element.body:
            if isinstance(element, CT_P):
                # Paragraph
                para = element
                text = para.text if hasattr(para, 'text') else ""
                if text.strip():
                    text_parts.append(text)
                    
            elif isinstance(element, CT_Tbl):
                # Table
                table = DocxTable(element, doc)
                extracted_table = self._extract_table(table)
                if extracted_table:
                    tables.append(extracted_table)
                    text_parts.append(f"\n[Table with {len(extracted_table.rows)} rows]\n")

        raw_text = "\n".join(text_parts)
        return raw_text, tables

    def _extract_table(self, table: DocxTable) -> ExtractedTable:
        """Extract a single table."""
        if not table.rows:
            return None

        # First row as headers
        headers = [cell.text.strip() for cell in table.rows[0].cells]
        
        # Remaining rows as data
        rows = []
        for row in table.rows[1:]:
            row_data = [cell.text.strip() for cell in row.cells]
            rows.append(row_data)

        if not rows:
            return None

        return ExtractedTable(
            headers=headers,
            rows=rows,
        )

    def _get_docx_metadata(self, file_path: Path, doc: Document) -> "DocumentMetadata":
        """Get metadata from DOCX."""
        try:
            core_props = doc.core_properties
            
            # DOCX doesn't have pages in the same way, estimate from content
            paragraph_count = len(doc.paragraphs)
            estimated_pages = max(1, paragraph_count // 30)  # Rough estimate

            return self._create_metadata(
                file_path=file_path,
                document_type=DocumentType.DOCX,
                page_count=estimated_pages,
                title=core_props.title,
                author=core_props.author,
                created_date=core_props.created,
                modified_date=core_props.modified,
            )

        except Exception as e:
            # Fallback to basic metadata if extraction fails
            return self._create_metadata(
                file_path=file_path,
                document_type=DocumentType.DOCX,
            )


