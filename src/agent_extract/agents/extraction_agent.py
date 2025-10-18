"""Content extraction agent - extracts structured data using LLM."""

import json
from typing import Dict, Any, List

from agent_extract.agents.base_agent import BaseAgent
from agent_extract.agents.state import AgentState
from agent_extract.core.types import ExtractedEntity


class ContentExtractionAgent(BaseAgent):
    """Agent that extracts structured content using LLM understanding."""

    def __init__(self):
        """Initialize content extraction agent with qwen3."""
        super().__init__()

    async def process(self, state: AgentState) -> AgentState:
        """
        Extract structured content from document.

        Args:
            state: Current agent state

        Returns:
            Updated state with extracted structured data
        """
        raw_text = state.get("raw_text", "")
        detected_schema = state.get("detected_schema", {})
        document_type = detected_schema.get("document_type", "unknown")
        key_fields = detected_schema.get("key_fields", [])

        # Create extraction prompt based on document type
        system_prompt = self._create_extraction_prompt(document_type)
        
        user_prompt = f"""Extract structured information from this {document_type} document.

Focus on extracting these key fields if present: {', '.join(key_fields) if key_fields else 'all relevant fields'}

Document text:
{raw_text[:3000]}  

Respond in JSON format with extracted data."""

        try:
            # Invoke LLM for extraction
            messages = self._create_prompt(system_prompt, user_prompt)
            response = await self._invoke_llm(messages)

            # Parse extracted data
            extracted_data = self._parse_extraction_response(response)
            
            # Extract entities
            entities = self._extract_entities(extracted_data)

            # Update state
            return self._update_state(
                state,
                {
                    "structured_data": {**state.get("structured_data", {}), **extracted_data},
                    "entities": entities,
                    "next_action": "parse_tables" if detected_schema.get("has_tables") else "validate",
                },
                f"Extracted {len(extracted_data)} fields and {len(entities)} entities",
            )

        except Exception as e:
            if "errors" not in state:
                state["errors"] = []
            state["errors"].append(f"Content extraction failed: {str(e)}")
            
            return self._update_state(
                state,
                {
                    "next_action": "validate",
                },
                "Content extraction failed, proceeding to validation",
            )

    def _create_extraction_prompt(self, document_type: str) -> str:
        """Create extraction prompt based on document type."""
        base_prompt = "You are an expert at extracting structured data from documents. "
        
        type_specific = {
            "invoice": """For invoices, extract:
- invoice_number, invoice_date, due_date
- vendor_name, vendor_address
- customer_name, customer_address
- line_items (list of items with description, quantity, price)
- subtotal, tax, total
- payment_terms""",
            
            "receipt": """For receipts, extract:
- merchant_name, merchant_address
- transaction_date, transaction_time
- items purchased (list)
- subtotal, tax, total
- payment_method""",
            
            "form": """For forms, extract all filled fields as key-value pairs.
Identify: form_title, form_number, submission_date, applicant information.""",
            
            "admission_ticket": """For admission tickets, extract:
- candidate_name, candidate_address
- exam_name, exam_type
- register_number, roll_number
- exam_date, exam_time, exam_session
- exam_centre, centre_address
- language_opted
- special_instructions""",
            
            "contract": """For contracts, extract:
- parties involved, effective_date, expiration_date
- terms and conditions summary
- key obligations, payment terms""",
            
            "letter": """For letters, extract:
- sender_name, sender_address
- recipient_name, recipient_address
- date, subject
- key points from body""",
        }
        
        return base_prompt + type_specific.get(document_type, 
            "Extract all key information as structured key-value pairs.")

    def _parse_extraction_response(self, response: str) -> Dict[str, Any]:
        """Parse LLM extraction response."""
        try:
            # Try to extract JSON
            if "```json" in response:
                json_str = response.split("```json")[1].split("```")[0].strip()
            elif "```" in response:
                json_str = response.split("```")[1].split("```")[0].strip()
            elif "{" in response and "}" in response:
                # Find JSON object in response
                start = response.index("{")
                end = response.rindex("}") + 1
                json_str = response[start:end]
            else:
                return self._parse_text_response(response)

            data = json.loads(json_str)
            return data

        except Exception as e:
            # Fallback to text parsing
            return self._parse_text_response(response)

    def _parse_text_response(self, text: str) -> Dict[str, Any]:
        """Fallback: parse extraction from plain text."""
        data = {}
        lines = text.split("\n")
        
        for line in lines:
            if ":" in line:
                parts = line.split(":", 1)
                if len(parts) == 2:
                    key = parts[0].strip().lower().replace(" ", "_")
                    value = parts[1].strip()
                    if key and value:
                        data[key] = value
        
        return data

    def _extract_entities(self, data: Dict[str, Any]) -> List[ExtractedEntity]:
        """Extract entities from structured data."""
        entities = []
        
        # Common entity types
        entity_keywords = {
            "person": ["name", "candidate", "applicant", "customer", "vendor"],
            "date": ["date", "time"],
            "location": ["address", "city", "state", "country", "centre"],
            "organization": ["company", "organization", "school", "institution"],
            "number": ["number", "id", "phone", "registration"],
            "money": ["amount", "price", "total", "tax", "subtotal"],
        }
        
        for key, value in data.items():
            if not isinstance(value, str):
                continue
                
            # Determine entity type
            key_lower = key.lower()
            entity_type = "other"
            
            for ent_type, keywords in entity_keywords.items():
                if any(kw in key_lower for kw in keywords):
                    entity_type = ent_type
                    break
            
            entities.append(
                ExtractedEntity(
                    text=str(value),
                    entity_type=entity_type,
                    confidence=0.8,
                )
            )
        
        return entities

