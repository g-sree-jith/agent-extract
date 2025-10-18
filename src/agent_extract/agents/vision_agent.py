"""Vision agent - uses gemma3:4b for image understanding."""

import json
import base64
from pathlib import Path
from typing import Dict, Any, List

from agent_extract.agents.base_agent import VisionAgent
from agent_extract.agents.state import AgentState
from agent_extract.core.types import ExtractedEntity


class DocumentVisionAgent(VisionAgent):
    """Agent that uses vision model (gemma3:4b) for image understanding."""

    def __init__(self):
        """Initialize vision agent with gemma3:4b."""
        super().__init__()

    async def process(self, state: AgentState) -> AgentState:
        """
        Analyze document image using vision model.

        Args:
            state: Current agent state

        Returns:
            Updated state with vision-based extraction
        """
        file_path = state.get("file_path", "")
        
        if not file_path:
            return self._update_state(
                state,
                {"next_action": "extract_content"},
                "No image to analyze",
            )

        # Check if it's an image file
        path = Path(file_path)
        if path.suffix.lower() not in [".png", ".jpg", ".jpeg", ".tiff", ".tif", ".bmp"]:
            # Not an image, skip vision analysis
            return self._update_state(
                state,
                {"next_action": "extract_content"},
                "Not an image file, skipping vision analysis",
            )

        try:
            # Analyze image for structure and content
            vision_data = await self._analyze_document_layout(file_path)
            
            # Update state with vision insights
            return self._update_state(
                state,
                {
                    "structured_data": {
                        **state.get("structured_data", {}),
                        "vision_analysis": vision_data,
                    },
                    "next_action": "extract_content",
                },
                f"Vision analysis complete: {vision_data.get('layout_type', 'unknown')} layout detected",
            )

        except Exception as e:
            if "errors" not in state:
                state["errors"] = []
            state["errors"].append(f"Vision analysis failed: {str(e)}")
            
            return self._update_state(
                state,
                {"next_action": "extract_content"},
                "Vision analysis failed, proceeding with OCR",
            )

    async def _analyze_document_layout(self, image_path: str) -> Dict[str, Any]:
        """
        Analyze document layout using vision model.

        Args:
            image_path: Path to the image file

        Returns:
            Dictionary with layout analysis
        """
        prompt = """Analyze this document image and identify:
1. Document type (form, invoice, receipt, letter, table, etc.)
2. Layout structure (single column, multi-column, has tables, has forms)
3. Key regions (header, footer, main content, tables, signature area)
4. Text orientation (portrait, landscape, rotated)
5. Quality (clear, blurry, skewed)

Respond in JSON format:
{
  "document_type": "type",
  "layout_type": "single_column/multi_column/form/table",
  "has_tables": true/false,
  "has_forms": true/false,
  "text_regions": ["header", "body", "table", "footer"],
  "quality": "clear/blurry/skewed",
  "requires_preprocessing": true/false
}"""

        try:
            # For now, use text-based analysis since vision API integration
            # depends on specific Ollama vision model capabilities
            # This is a placeholder that will work with gemma3:4b
            
            response = await self._invoke_vision_llm(image_path, prompt)
            
            # Parse response
            analysis = self._parse_vision_response(response)
            return analysis

        except Exception as e:
            # Fallback to basic analysis
            return {
                "document_type": "unknown",
                "layout_type": "unknown",
                "has_tables": False,
                "has_forms": False,
                "quality": "unknown",
                "error": str(e),
            }

    def _parse_vision_response(self, response: str) -> Dict[str, Any]:
        """Parse vision model response."""
        try:
            if "```json" in response:
                json_str = response.split("```json")[1].split("```")[0].strip()
            elif "```" in response:
                json_str = response.split("```")[1].split("```")[0].strip()
            elif "{" in response and "}" in response:
                start = response.index("{")
                end = response.rindex("}") + 1
                json_str = response[start:end]
            else:
                return self._parse_text_vision_response(response)

            return json.loads(json_str)

        except Exception:
            return self._parse_text_vision_response(response)

    def _parse_text_vision_response(self, text: str) -> Dict[str, Any]:
        """Fallback: parse vision analysis from plain text."""
        text_lower = text.lower()
        
        return {
            "document_type": self._detect_type_from_text(text_lower),
            "layout_type": "single_column",  # Default
            "has_tables": "table" in text_lower,
            "has_forms": "form" in text_lower or "field" in text_lower,
            "quality": "clear" if "clear" in text_lower else "unknown",
        }

    def _detect_type_from_text(self, text: str) -> str:
        """Detect document type from text."""
        types = ["invoice", "receipt", "form", "letter", "contract", "report"]
        for doc_type in types:
            if doc_type in text:
                return doc_type
        return "unknown"

