"""OCR Manager to handle multiple OCR engines with fallback."""

from pathlib import Path
from typing import Optional, List, Tuple

from agent_extract.core.exceptions import OCRError
from agent_extract.core.config import config
from agent_extract.ocr.paddle_ocr import PaddleOCREngine
from agent_extract.ocr.tesseract_ocr import TesseractOCREngine


class OCRManager:
    """Manager for OCR engines with automatic fallback."""

    def __init__(
        self,
        primary_engine: str = "paddle",
        fallback_engine: str = "tesseract",
        lang: str = "en",
    ):
        """
        Initialize OCR manager.

        Args:
            primary_engine: Primary OCR engine to use ('paddle' or 'tesseract')
            fallback_engine: Fallback OCR engine
            lang: Language code
        """
        self.primary_engine_name = primary_engine
        self.fallback_engine_name = fallback_engine
        self.lang = lang

        self.primary_engine: Optional[PaddleOCREngine | TesseractOCREngine] = None
        self.fallback_engine: Optional[PaddleOCREngine | TesseractOCREngine] = None

        self._initialize_engines()

    def _initialize_engines(self):
        """Initialize OCR engines."""
        # Initialize primary engine
        try:
            if self.primary_engine_name == "paddle":
                self.primary_engine = PaddleOCREngine(lang=self.lang)
            elif self.primary_engine_name == "tesseract":
                lang_code = "eng" if self.lang == "en" else self.lang
                self.primary_engine = TesseractOCREngine(lang=lang_code)
        except Exception as e:
            print(f"Warning: Failed to initialize primary OCR engine: {e}")

        # Initialize fallback engine
        try:
            if self.fallback_engine_name == "tesseract" and self.primary_engine_name != "tesseract":
                lang_code = "eng" if self.lang == "en" else self.lang
                self.fallback_engine = TesseractOCREngine(lang=lang_code)
            elif self.fallback_engine_name == "paddle" and self.primary_engine_name != "paddle":
                self.fallback_engine = PaddleOCREngine(lang=self.lang)
        except Exception as e:
            print(f"Warning: Failed to initialize fallback OCR engine: {e}")

    def extract_text(self, image_path: Path) -> str:
        """
        Extract text from an image using available OCR engines.

        Args:
            image_path: Path to the image file

        Returns:
            Extracted text as a string

        Raises:
            OCRError: If all OCR engines fail
        """
        # Try primary engine
        if self.primary_engine:
            try:
                return self.primary_engine.extract_text(image_path)
            except Exception as e:
                print(f"Primary OCR engine failed: {e}. Trying fallback...")

        # Try fallback engine
        if self.fallback_engine:
            try:
                return self.fallback_engine.extract_text(image_path)
            except Exception as e:
                print(f"Fallback OCR engine failed: {e}")

        raise OCRError("All OCR engines failed to extract text from the image")

    def extract_with_boxes(
        self, image_path: Path
    ) -> List[Tuple[str, float, Tuple[float, float, float, float]]]:
        """
        Extract text with bounding boxes.

        Args:
            image_path: Path to the image file

        Returns:
            List of tuples: (text, confidence, (x, y, width, height))

        Raises:
            OCRError: If extraction fails
        """
        # Try primary engine (prefer PaddleOCR for boxes)
        if self.primary_engine and hasattr(self.primary_engine, 'extract_with_boxes'):
            try:
                return self.primary_engine.extract_with_boxes(image_path)
            except Exception as e:
                print(f"Primary OCR engine (with boxes) failed: {e}")

        # Fallback: return simple text without boxes
        text = self.extract_text(image_path)
        if text:
            return [(text, 1.0, (0, 0, 0, 0))]
        return []

    @staticmethod
    def from_config() -> "OCRManager":
        """
        Create OCR manager from global config.

        Returns:
            OCRManager instance
        """
        return OCRManager(
            primary_engine=config.ocr_engine,
            fallback_engine="tesseract" if config.ocr_engine != "tesseract" else "paddle",
            lang=config.ocr_language,
        )


