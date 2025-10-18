"""Validation agent - ensures extraction quality and consistency."""

import json
from typing import Dict, Any, List

from agent_extract.agents.base_agent import BaseAgent
from agent_extract.agents.state import AgentState


class ValidationAgent(BaseAgent):
    """Agent that validates and improves extraction quality."""

    def __init__(self):
        """Initialize validation agent with qwen3."""
        super().__init__()

    async def process(self, state: AgentState) -> AgentState:
        """
        Validate extracted data and suggest corrections.

        Args:
            state: Current agent state

        Returns:
            Updated state with validated data
        """
        structured_data = state.get("structured_data", {})
        raw_text = state.get("raw_text", "")[:1000]  # Context
        
        if not structured_data:
            # Nothing to validate
            return self._update_state(
                state,
                {"next_action": "complete"},
                "No structured data to validate",
            )

        # Create validation prompt
        system_prompt = """You are a data quality expert. Review the extracted data and:
1. Check for missing required fields
2. Verify data format consistency
3. Flag any suspicious or incorrect values
4. Suggest corrections if needed

Respond in JSON:
{
  "is_valid": true/false,
  "confidence": 0.0-1.0,
  "issues": ["issue1", "issue2"],
  "corrections": {"field": "corrected_value"},
  "completeness_score": 0.0-1.0
}"""

        user_prompt = f"""Validate this extracted data:

Extracted Data:
{json.dumps(structured_data, indent=2)}

Original Text Context:
{raw_text}

Check for accuracy and completeness."""

        try:
            messages = self._create_prompt(system_prompt, user_prompt)
            response = await self._invoke_llm(messages)

            # Parse validation result
            validation = self._parse_validation_response(response)

            # Apply corrections if any
            if validation.get("corrections"):
                structured_data.update(validation["corrections"])

            # Calculate overall confidence
            confidence = validation.get("confidence", state.get("confidence_score", 0.8))
            
            # Update state
            return self._update_state(
                state,
                {
                    "structured_data": structured_data,
                    "confidence_score": confidence,
                    "next_action": "complete",
                },
                f"Validation complete (confidence: {confidence:.2%}, "
                f"issues: {len(validation.get('issues', []))})",
            )

        except Exception as e:
            # If validation fails, still mark as complete
            if "errors" not in state:
                state["errors"] = []
            state["errors"].append(f"Validation failed: {str(e)}")
            
            return self._update_state(
                state,
                {
                    "confidence_score": 0.7,  # Lower confidence if validation failed
                    "next_action": "complete",
                },
                "Validation failed, proceeding with extracted data",
            )

    def _parse_validation_response(self, response: str) -> Dict[str, Any]:
        """Parse validation response."""
        try:
            if "```json" in response:
                json_str = response.split("```json")[1].split("```")[0].strip()
            elif "```" in response:
                json_str = response.split("```")[1].split("```")[0].strip()
            else:
                # Try to find JSON in response
                if "{" in response and "}" in response:
                    start = response.index("{")
                    end = response.rindex("}") + 1
                    json_str = response[start:end]
                else:
                    return self._default_validation()

            validation = json.loads(json_str)
            return validation

        except Exception:
            return self._default_validation()

    def _default_validation(self) -> Dict[str, Any]:
        """Return default validation result if parsing fails."""
        return {
            "is_valid": True,
            "confidence": 0.7,
            "issues": [],
            "corrections": {},
            "completeness_score": 0.7,
        }

