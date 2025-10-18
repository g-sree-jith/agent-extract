"""Planner agent - creates extraction strategy based on document analysis."""

import json
from typing import Dict, Any, List

from agent_extract.agents.base_agent import BaseAgent
from agent_extract.agents.state import AgentState


class PlannerAgent(BaseAgent):
    """
    Planner agent that analyzes document and creates extraction plan.
    
    Uses qwen3:0.6b to understand document and plan extraction strategy.
    """

    def __init__(self):
        """Initialize planner agent with qwen3."""
        super().__init__()

    async def process(self, state: AgentState) -> AgentState:
        """
        Analyze document and create extraction plan.

        Args:
            state: Current agent state

        Returns:
            Updated state with extraction plan
        """
        raw_text = state.get("raw_text", "")
        file_path = state.get("file_path", "")

        # Create planning prompt
        system_prompt = """You are an extraction planning expert. Analyze documents and create optimal extraction strategies.

Your task:
1. Quick-scan the document to understand its nature
2. Identify what data needs to be extracted
3. Determine the best approach (OCR-only, OCR+AI, Vision+AI)
4. List specific fields to extract
5. Estimate extraction complexity

Respond in JSON:
{
  "document_category": "invoice/form/letter/report/ticket/etc",
  "extraction_approach": "basic/advanced/vision",
  "key_fields_to_extract": ["field1", "field2"],
  "has_tabular_data": true/false,
  "has_form_fields": true/false,
  "complexity": "simple/medium/complex",
  "recommended_agents": ["schema", "extraction", "table_parser"],
  "estimated_accuracy": 0.0-1.0,
  "notes": "any special considerations"
}"""

        user_prompt = f"""Create an extraction plan for this document:

File: {file_path}

Document preview (first 800 chars):
{raw_text[:800]}

What's the best strategy to extract all relevant data?"""

        try:
            messages = self._create_prompt(system_prompt, user_prompt)
            response = await self._invoke_llm(messages)
            
            plan = self._parse_plan_response(response)
            
            # Store plan in state
            return self._update_state(
                state,
                {
                    "structured_data": {
                        **state.get("structured_data", {}),
                        "extraction_plan": plan,
                    },
                    "next_action": "schema",  # Start with schema detection
                },
                f"Created extraction plan: {plan.get('extraction_approach', 'basic')} "
                f"approach for {plan.get('document_category', 'unknown')} document",
            )

        except Exception as e:
            if "errors" not in state:
                state["errors"] = []
            state["errors"].append(f"Planning failed: {str(e)}")
            
            # Use default plan
            return self._update_state(
                state,
                {
                    "structured_data": {
                        **state.get("structured_data", {}),
                        "extraction_plan": self._default_plan(),
                    },
                    "next_action": "schema",
                },
                "Using default extraction plan",
            )

    def _parse_plan_response(self, response: str) -> Dict[str, Any]:
        """Parse planner's response."""
        try:
            if "```json" in response:
                json_str = response.split("```json")[1].split("```")[0].strip()
            elif "{" in response and "}" in response:
                start = response.index("{")
                end = response.rindex("}") + 1
                json_str = response[start:end]
            else:
                return self._default_plan()

            plan = json.loads(json_str)
            return plan

        except Exception:
            return self._default_plan()

    def _default_plan(self) -> Dict[str, Any]:
        """Return default extraction plan."""
        return {
            "document_category": "unknown",
            "extraction_approach": "advanced",
            "key_fields_to_extract": [],
            "has_tabular_data": False,
            "has_form_fields": False,
            "complexity": "medium",
            "recommended_agents": ["schema", "extraction", "critic"],
            "estimated_accuracy": 0.8,
            "notes": "Default plan - will adapt as we learn more",
        }

