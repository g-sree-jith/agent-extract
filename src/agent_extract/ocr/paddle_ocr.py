"""PaddleOCR implementation for text extraction."""

from pathlib import Path
from typing import List, Tuple, Optional
import numpy as np
from PIL import Image

from agent_extract.core.exceptions import OCRError


class PaddleOCREngine:
    """PaddleOCR engine for text extraction from images."""

    def __init__(self, lang: str = "en", use_gpu: bool = False):
        """
        Initialize PaddleOCR engine.

        Args:
            lang: Language code (default: 'en')
            use_gpu: Whether to use GPU acceleration
        """
        self.lang = lang
        self.use_gpu = use_gpu
        self._ocr = None
        self._initialized = False

    def _initialize(self):
        """Lazy initialization of PaddleOCR."""
        if self._initialized:
            return

        try:
            from paddleocr import PaddleOCR

            self._ocr = PaddleOCR(
                use_angle_cls=True,
                lang=self.lang,
                use_gpu=self.use_gpu,
                show_log=False,
            )
            self._initialized = True

        except ImportError as e:
            raise OCRError(
                "PaddleOCR not installed. Install with: pip install paddleocr paddlepaddle"
            ) from e
        except Exception as e:
            raise OCRError(f"Failed to initialize PaddleOCR: {str(e)}") from e

    def extract_text(self, image_path: Path) -> str:
        """
        Extract text from an image.

        Args:
            image_path: Path to the image file

        Returns:
            Extracted text as a string

        Raises:
            OCRError: If text extraction fails
        """
        self._initialize()

        try:
            result = self._ocr.ocr(str(image_path), cls=True)

            if not result or not result[0]:
                return ""

            # Extract text from OCR results
            text_parts = []
            for line in result[0]:
                if line and len(line) >= 2:
                    text = line[1][0]  # Get text from (text, confidence) tuple
                    text_parts.append(text)

            return "\n".join(text_parts)

        except Exception as e:
            raise OCRError(f"PaddleOCR extraction failed: {str(e)}") from e

    def extract_with_boxes(
        self, image_path: Path
    ) -> List[Tuple[str, float, Tuple[float, float, float, float]]]:
        """
        Extract text with bounding boxes and confidence scores.

        Args:
            image_path: Path to the image file

        Returns:
            List of tuples: (text, confidence, (x, y, width, height))

        Raises:
            OCRError: If text extraction fails
        """
        self._initialize()

        try:
            result = self._ocr.ocr(str(image_path), cls=True)

            if not result or not result[0]:
                return []

            extracted_data = []
            for line in result[0]:
                if line and len(line) >= 2:
                    bbox = line[0]  # [[x1,y1], [x2,y2], [x3,y3], [x4,y4]]
                    text, confidence = line[1]

                    # Convert bbox to (x, y, width, height)
                    x_coords = [p[0] for p in bbox]
                    y_coords = [p[1] for p in bbox]
                    x = min(x_coords)
                    y = min(y_coords)
                    width = max(x_coords) - x
                    height = max(y_coords) - y

                    extracted_data.append((text, confidence, (x, y, width, height)))

            return extracted_data

        except Exception as e:
            raise OCRError(f"PaddleOCR extraction with boxes failed: {str(e)}") from e

    def supports_language(self, lang: str) -> bool:
        """
        Check if a language is supported.

        Args:
            lang: Language code

        Returns:
            True if supported, False otherwise
        """
        # PaddleOCR supports many languages
        supported_langs = [
            "en", "ch", "chinese_cht", "ta", "te", "ka", "latin", "arabic",
            "cyrillic", "devanagari", "fr", "de", "ja", "ko", "it", "es",
            "pt", "ru", "hi", "ar", "vi", "uk", "bg", "mr", "ne", "ur"
        ]
        return lang in supported_langs


