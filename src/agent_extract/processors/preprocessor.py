"""Image preprocessing for better OCR and vision model performance."""

from pathlib import Path
from typing import Tuple, Optional
from PIL import Image, ImageEnhance, ImageFilter
import numpy as np


class ImagePreprocessor:
    """Preprocessor for images to improve OCR accuracy."""

    def __init__(self):
        """Initialize image preprocessor."""
        pass

    def preprocess(
        self,
        image_path: Path,
        auto_enhance: bool = True,
        target_dpi: int = 300,
    ) -> Image.Image:
        """
        Preprocess image for better OCR/vision model performance.

        Args:
            image_path: Path to the image file
            auto_enhance: Apply automatic enhancements
            target_dpi: Target DPI for scaling

        Returns:
            Preprocessed PIL Image
        """
        img = Image.open(image_path)

        # Convert to RGB if necessary
        if img.mode != "RGB":
            img = img.convert("RGB")

        if auto_enhance:
            img = self.auto_enhance(img)

        return img

    def auto_enhance(self, img: Image.Image) -> Image.Image:
        """
        Apply automatic enhancements to improve quality.

        Args:
            img: PIL Image

        Returns:
            Enhanced image
        """
        # Increase contrast slightly
        enhancer = ImageEnhance.Contrast(img)
        img = enhancer.enhance(1.2)

        # Increase sharpness
        enhancer = ImageEnhance.Sharpness(img)
        img = enhancer.enhance(1.3)

        return img

    def deskew(self, img: Image.Image) -> Image.Image:
        """
        Deskew (straighten) a rotated image.

        Args:
            img: PIL Image

        Returns:
            Deskewed image
        """
        # Simple deskew implementation
        # For production, would use more sophisticated methods
        return img

    def denoise(self, img: Image.Image) -> Image.Image:
        """
        Remove noise from image.

        Args:
            img: PIL Image

        Returns:
            Denoised image
        """
        # Apply median filter for noise reduction
        return img.filter(ImageFilter.MedianFilter(size=3))

    def binarize(self, img: Image.Image, threshold: int = 128) -> Image.Image:
        """
        Convert image to black and white.

        Args:
            img: PIL Image
            threshold: Binarization threshold (0-255)

        Returns:
            Binarized image
        """
        # Convert to grayscale first
        img = img.convert("L")
        
        # Apply threshold
        img = img.point(lambda x: 255 if x > threshold else 0, mode="1")
        
        return img

