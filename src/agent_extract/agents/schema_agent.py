"""Schema detection agent - identifies document type and structure."""

import json
from typing import Dict, Any

from agent_extract.agents.base_agent import BaseAgent
from agent_extract.agents.state import AgentState
from agent_extract.core.types import DocumentType


class SchemaDetectionAgent(BaseAgent):
    """Agent that detects document type and identifies schema."""

    def __init__(self):
        """Initialize schema detection agent with qwen3 (tool calling)."""
        super().__init__()

    async def process(self, state: AgentState) -> AgentState:
        """
        Detect document type and schema from raw text.

        Args:
            state: Current agent state

        Returns:
            Updated state with detected document type and schema
        """
        # Skip if already detected
        if state.get("detected_schema") and state.get("document_type"):
            return self._update_state(
                state,
                {"next_action": "extraction"},
                "Schema already detected, skipping",
            )
        
        raw_text = state.get("raw_text", "")
        file_name = state.get("file_path", "")

        # Create prompt for document classification
        system_prompt = """You are a document classification expert. Analyze the text and determine:
1. Document type (invoice, receipt, form, contract, letter, report, admission ticket, etc.)
2. Key fields that should be extracted
3. Document structure

Respond in JSON format with:
{
  "document_type": "type here",
  "confidence": 0.0-1.0,
  "key_fields": ["field1", "field2"],
  "has_tables": true/false,
  "has_forms": true/false,
  "language": "en/other"
}"""

        user_prompt = f"""Analyze this document and classify it:

Filename: {file_name}

Text preview (first 1000 characters):
{raw_text[:1000]}

Identify the document type and key fields to extract."""

        try:
            # Invoke LLM for classification
            messages = self._create_prompt(system_prompt, user_prompt)
            response = await self._invoke_llm(messages)

            # Parse response
            schema = self._parse_schema_response(response)

            # Determine document type enum
            doc_type = self._map_to_document_type(schema.get("document_type", "unknown"))

            # Update state
            return self._update_state(
                state,
                {
                    "document_type": doc_type,
                    "confidence_score": schema.get("confidence", 0.7),
                    "detected_schema": schema,
                    "next_action": "extract_content",
                },
                f"Detected document type: {schema.get('document_type')} "
                f"(confidence: {schema.get('confidence', 0):.2%})",
            )

        except Exception as e:
            # Fallback to unknown type
            if "errors" not in state:
                state["errors"] = []
            state["errors"].append(f"Schema detection failed: {str(e)}")
            
            return self._update_state(
                state,
                {
                    "document_type": DocumentType.UNKNOWN,
                    "confidence_score": 0.5,
                    "detected_schema": {"document_type": "unknown"},
                    "next_action": "extract_content",
                },
                f"Schema detection failed, using fallback",
            )

    def _parse_schema_response(self, response: str) -> Dict[str, Any]:
        """Parse LLM response to extract schema."""
        try:
            # Try to extract JSON from response
            # LLM might wrap it in markdown code blocks
            if "```json" in response:
                json_str = response.split("```json")[1].split("```")[0].strip()
            elif "```" in response:
                json_str = response.split("```")[1].split("```")[0].strip()
            else:
                json_str = response.strip()

            schema = json.loads(json_str)
            return schema

        except Exception as e:
            # Fallback: parse from text
            return {
                "document_type": self._extract_type_from_text(response),
                "confidence": 0.5,
                "key_fields": [],
                "has_tables": "table" in response.lower(),
                "has_forms": "form" in response.lower(),
                "language": "en",
            }

    def _extract_type_from_text(self, text: str) -> str:
        """Extract document type from text response."""
        text_lower = text.lower()
        
        types = {
            "invoice": ["invoice", "bill"],
            "receipt": ["receipt"],
            "form": ["form", "application"],
            "contract": ["contract", "agreement"],
            "letter": ["letter", "correspondence"],
            "report": ["report", "analysis"],
            "admission_ticket": ["admission", "ticket", "exam"],
            "resume": ["resume", "cv", "curriculum vitae"],
        }
        
        for doc_type, keywords in types.items():
            if any(keyword in text_lower for keyword in keywords):
                return doc_type
        
        return "unknown"

    def _map_to_document_type(self, type_str: str) -> DocumentType:
        """Map string to DocumentType enum."""
        type_mapping = {
            "pdf": DocumentType.PDF,
            "docx": DocumentType.DOCX,
            "word": DocumentType.DOCX,
            "image": DocumentType.IMAGE,
            "excel": DocumentType.EXCEL,
            "spreadsheet": DocumentType.EXCEL,
            "csv": DocumentType.CSV,
            "html": DocumentType.HTML,
            "text": DocumentType.TXT,
        }
        
        type_lower = type_str.lower()
        for key, doc_type in type_mapping.items():
            if key in type_lower:
                return doc_type
        
        return DocumentType.UNKNOWN

