"""Critic agent - evaluates and improves extraction quality."""

import json
from typing import Dict, Any, List

from agent_extract.agents.base_agent import BaseAgent
from agent_extract.agents.state import AgentState


class CriticAgent(BaseAgent):
    """
    Critic agent that evaluates extraction quality and suggests improvements.
    
    Uses qwen3:0.6b to critically analyze extractions and provide feedback.
    """

    def __init__(self):
        """Initialize critic agent with qwen3."""
        super().__init__()

    async def process(self, state: AgentState) -> AgentState:
        """
        Critique the extraction and suggest improvements.

        Args:
            state: Current agent state

        Returns:
            Updated state with critique and improvements
        """
        raw_text = state.get("raw_text", "")[:1500]
        structured_data = state.get("structured_data", {})
        entities = state.get("entities", [])
        tables = state.get("tables", [])
        extraction_plan = structured_data.get("extraction_plan", {})

        # Create critique prompt
        system_prompt = """You are a quality assurance expert that critiques document extractions.

Your responsibilities:
1. Evaluate completeness - are all important fields extracted?
2. Check accuracy - does extracted data match the original text?
3. Verify consistency - are data formats correct?
4. Identify gaps - what's missing?
5. Suggest corrections - how to improve?

Respond in JSON:
{
  "overall_quality": "excellent/good/fair/poor",
  "confidence_score": 0.0-1.0,
  "completeness": 0.0-1.0,
  "accuracy": 0.0-1.0,
  "issues_found": ["issue1", "issue2"],
  "missing_fields": ["field1", "field2"],
  "corrections": {"field": "corrected_value"},
  "recommendations": ["recommendation1"],
  "final_verdict": "approve/request_reextraction/needs_review"
}"""

        user_prompt = f"""Critique this document extraction:

ORIGINAL TEXT (excerpt):
{raw_text}

EXTRACTED DATA:
{json.dumps({k: v for k, v in structured_data.items() if k != "ai_processing"}, indent=2)}

ENTITIES FOUND: {len(entities)}
TABLES FOUND: {len(tables)}

EXPECTED (from plan): {extraction_plan.get('key_fields_to_extract', [])}

Evaluate the quality and suggest improvements."""

        try:
            messages = self._create_prompt(system_prompt, user_prompt)
            response = await self._invoke_llm(messages)
            
            critique = self._parse_critique_response(response)
            
            # Apply corrections if high confidence
            if critique.get("corrections") and critique.get("confidence_score", 0) > 0.8:
                for field, value in critique["corrections"].items():
                    structured_data[field] = value

            # Determine if we need re-extraction
            final_verdict = critique.get("final_verdict", "approve")
            
            if final_verdict == "approve":
                next_action = "complete"
            elif final_verdict == "request_reextraction" and len(state.get("processing_steps", [])) < 10:
                next_action = "extraction"  # Re-extract
            else:
                next_action = "complete"  # Accept as-is

            # Update state
            return self._update_state(
                state,
                {
                    "structured_data": {
                        **structured_data,
                        "quality_critique": critique,
                    },
                    "confidence_score": critique.get("confidence_score", 0.8),
                    "next_action": next_action,
                },
                f"Critique complete: {critique.get('overall_quality', 'good')} "
                f"(confidence: {critique.get('confidence_score', 0.8):.2%})",
            )

        except Exception as e:
            if "errors" not in state:
                state["errors"] = []
            state["errors"].append(f"Critique failed: {str(e)}")
            
            return self._update_state(
                state,
                {
                    "confidence_score": 0.75,  # Moderate confidence if critique fails
                    "next_action": "complete",
                },
                "Critique failed, accepting extraction as-is",
            )

    def _parse_critique_response(self, response: str) -> Dict[str, Any]:
        """Parse critic's response."""
        try:
            if "```json" in response:
                json_str = response.split("```json")[1].split("```")[0].strip()
            elif "{" in response and "}" in response:
                start = response.index("{")
                end = response.rindex("}") + 1
                json_str = response[start:end]
            else:
                return self._default_critique(response)

            critique = json.loads(json_str)
            return critique

        except Exception:
            return self._default_critique(response)

    def _default_critique(self, text: str = "") -> Dict[str, Any]:
        """Return default critique if parsing fails."""
        # Try to infer quality from text
        text_lower = text.lower()
        
        if any(word in text_lower for word in ["excellent", "complete", "accurate"]):
            quality = "good"
            confidence = 0.85
        elif any(word in text_lower for word in ["poor", "incomplete", "missing"]):
            quality = "fair"
            confidence = 0.65
        else:
            quality = "good"
            confidence = 0.75

        return {
            "overall_quality": quality,
            "confidence_score": confidence,
            "completeness": confidence,
            "accuracy": confidence,
            "issues_found": [],
            "missing_fields": [],
            "corrections": {},
            "recommendations": [],
            "final_verdict": "approve",
        }

