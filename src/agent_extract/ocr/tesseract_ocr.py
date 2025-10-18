"""Tesseract OCR implementation as fallback."""

from pathlib import Path
from typing import Optional
from PIL import Image

from agent_extract.core.exceptions import OCRError


class TesseractOCREngine:
    """Tesseract OCR engine as fallback option."""

    def __init__(self, lang: str = "eng"):
        """
        Initialize Tesseract OCR engine.

        Args:
            lang: Language code (default: 'eng' for English)
        """
        self.lang = lang
        self._initialized = False

    def _initialize(self):
        """Check if Tesseract is available."""
        if self._initialized:
            return

        try:
            import pytesseract

            # Try to get version to check if Tesseract is installed
            pytesseract.get_tesseract_version()
            self._initialized = True

        except ImportError as e:
            raise OCRError(
                "pytesseract not installed. Install with: pip install pytesseract"
            ) from e
        except Exception as e:
            raise OCRError(
                "Tesseract not found. Please install Tesseract OCR: "
                "https://github.com/tesseract-ocr/tesseract"
            ) from e

    def extract_text(self, image_path: Path) -> str:
        """
        Extract text from an image using Tesseract.

        Args:
            image_path: Path to the image file

        Returns:
            Extracted text as a string

        Raises:
            OCRError: If text extraction fails
        """
        self._initialize()

        try:
            import pytesseract

            image = Image.open(image_path)
            text = pytesseract.image_to_string(image, lang=self.lang)
            return text.strip()

        except Exception as e:
            raise OCRError(f"Tesseract extraction failed: {str(e)}") from e

    def extract_with_boxes(self, image_path: Path) -> dict:
        """
        Extract text with bounding boxes using Tesseract.

        Args:
            image_path: Path to the image file

        Returns:
            Dictionary containing OCR data with bounding boxes

        Raises:
            OCRError: If text extraction fails
        """
        self._initialize()

        try:
            import pytesseract

            image = Image.open(image_path)
            data = pytesseract.image_to_data(image, lang=self.lang, output_type=pytesseract.Output.DICT)
            return data

        except Exception as e:
            raise OCRError(f"Tesseract extraction with boxes failed: {str(e)}") from e

    def supports_language(self, lang: str) -> bool:
        """
        Check if a language is supported.

        Args:
            lang: Language code

        Returns:
            True if supported, False otherwise
        """
        # Common Tesseract language codes
        supported_langs = [
            "eng", "spa", "fra", "deu", "ita", "por", "rus", "jpn",
            "kor", "chi_sim", "chi_tra", "ara", "hin", "ben", "tha",
        ]
        return lang in supported_langs


