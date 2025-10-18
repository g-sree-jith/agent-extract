"""Image document reader with OCR support."""

import time
from pathlib import Path
from typing import Optional
from PIL import Image

from agent_extract.core.types import (
    DocumentType,
    ExtractionResult,
)
from agent_extract.core.exceptions import DocumentReadError
from agent_extract.readers.base import BaseReader


class ImageReader(BaseReader):
    """Reader for image documents with OCR."""

    def __init__(self, ocr_engine=None):
        """
        Initialize the image reader.
        
        Args:
            ocr_engine: OCR engine instance (will be set up in Phase 1)
        """
        super().__init__()
        self.supported_extensions = {".png", ".jpg", ".jpeg", ".tiff", ".tif", ".bmp", ".webp"}
        self.supported_mime_types = {
            "image/png",
            "image/jpeg",
            "image/tiff",
            "image/bmp",
            "image/webp",
        }
        self.ocr_engine = ocr_engine

    def read(self, file_path: Path) -> ExtractionResult:
        """
        Read and extract content from an image document.

        Args:
            file_path: Path to the image file

        Returns:
            ExtractionResult containing extracted data

        Raises:
            DocumentReadError: If the image cannot be read
        """
        start_time = time.time()
        self._validate_file(file_path)

        try:
            # Load image
            image = Image.open(file_path)
            
            # Basic image info
            width, height = image.size
            mode = image.mode
            
            # Extract text using OCR if available
            raw_text = ""
            if self.ocr_engine:
                raw_text = self.ocr_engine.extract_text(file_path)
            else:
                raw_text = "[OCR not initialized - text extraction skipped]"
            
            # Get metadata
            metadata = self._create_metadata(
                file_path=file_path,
                document_type=DocumentType.IMAGE,
                page_count=1,
            )
            
            processing_time = time.time() - start_time

            # Store basic image info in structured_data
            structured_data = {
                "image_width": width,
                "image_height": height,
                "image_mode": mode,
                "image_format": image.format,
            }

            return ExtractionResult(
                metadata=metadata,
                raw_text=raw_text,
                structured_data=structured_data,
                processing_time=processing_time,
                extraction_method="image_ocr",
            )

        except Exception as e:
            raise DocumentReadError(f"Failed to read image {file_path}: {str(e)}") from e


