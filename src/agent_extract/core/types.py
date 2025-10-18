"""Type definitions and enums for agent-extract."""

from enum import Enum
from typing import Any, Dict, List, Optional
from datetime import datetime
from pydantic import BaseModel, Field


class DocumentType(str, Enum):
    """Supported document types."""

    PDF = "pdf"
    DOCX = "docx"
    IMAGE = "image"
    EXCEL = "excel"
    CSV = "csv"
    HTML = "html"
    TXT = "txt"
    UNKNOWN = "unknown"


class OutputFormat(str, Enum):
    """Supported output formats."""

    JSON = "json"
    MARKDOWN = "markdown"


class OCREngine(str, Enum):
    """Available OCR engines."""

    PADDLE = "paddle"
    TESSERACT = "tesseract"


class DocumentMetadata(BaseModel):
    """Metadata about the document."""

    filename: str
    file_size: int = Field(description="File size in bytes")
    document_type: DocumentType
    mime_type: Optional[str] = None
    page_count: Optional[int] = None
    created_date: Optional[datetime] = None
    modified_date: Optional[datetime] = None
    author: Optional[str] = None
    title: Optional[str] = None
    language: Optional[str] = "en"


class BoundingBox(BaseModel):
    """Bounding box coordinates."""

    x: float
    y: float
    width: float
    height: float
    page: Optional[int] = None


class ExtractedText(BaseModel):
    """Extracted text with metadata."""

    text: str
    confidence: Optional[float] = None
    bbox: Optional[BoundingBox] = None
    page: Optional[int] = None


class ExtractedTable(BaseModel):
    """Extracted table data."""

    headers: List[str]
    rows: List[List[str]]
    page: Optional[int] = None
    bbox: Optional[BoundingBox] = None


class ExtractedEntity(BaseModel):
    """Extracted named entity."""

    text: str
    entity_type: str
    confidence: Optional[float] = None


class ExtractionResult(BaseModel):
    """Complete extraction result."""

    metadata: DocumentMetadata
    raw_text: str
    structured_data: Dict[str, Any] = Field(default_factory=dict)
    tables: List[ExtractedTable] = Field(default_factory=list)
    entities: List[ExtractedEntity] = Field(default_factory=list)
    images: List[str] = Field(default_factory=list, description="Base64 encoded images")
    confidence_score: Optional[float] = None
    processing_time: Optional[float] = None
    extraction_method: Optional[str] = None

    class Config:
        """Pydantic config."""

        json_encoders = {datetime: lambda v: v.isoformat()}


