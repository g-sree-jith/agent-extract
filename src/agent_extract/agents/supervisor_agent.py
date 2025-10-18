"""Supervisor agent - orchestrates the overall extraction workflow."""

import json
from typing import Dict, Any, List, Literal

from agent_extract.agents.base_agent import BaseAgent
from agent_extract.agents.state import AgentState


class SupervisorAgent(BaseAgent):
    """
    Supervisor agent that orchestrates the extraction workflow.
    
    Decides which sub-agents to invoke and in what order.
    Uses qwen3:0.6b with tool calling to make routing decisions.
    """

    def __init__(self):
        """Initialize supervisor agent with qwen3 (tool calling)."""
        super().__init__()

    async def process(self, state: AgentState) -> AgentState:
        """
        Analyze state and decide next steps.

        Args:
            state: Current agent state

        Returns:
            Updated state with routing decision
        """
        current_step = len(state.get("processing_steps", []))
        document_type = state.get("document_type")
        has_structured_data = bool(state.get("structured_data"))
        has_entities = bool(state.get("entities"))
        
        # Create supervision prompt
        system_prompt = """You are a supervisor AI that coordinates document extraction agents.

Available agents:
1. planner - Creates extraction plan
2. vision - Analyzes image layout (for images only)
3. schema - Detects document type
4. extraction - Extracts key-value pairs
5. table_parser - Parses tables
6. critic - Evaluates extraction quality
7. complete - Finishes workflow

Based on current state, decide which agent should run next.

Respond with JSON:
{
  "next_agent": "agent_name",
  "reason": "why this agent",
  "priority": "high/medium/low"
}"""

        state_summary = self._summarize_state(state)
        user_prompt = f"""Current workflow state:
{state_summary}

Which agent should execute next to best extract data from this document?"""

        try:
            messages = self._create_prompt(system_prompt, user_prompt)
            response = await self._invoke_llm(messages)
            
            decision = self._parse_supervisor_decision(response)
            next_agent = decision.get("next_agent", "complete")
            
            return self._update_state(
                state,
                {
                    "next_action": next_agent,
                },
                f"Routing to {next_agent}: {decision.get('reason', 'Continue extraction')}",
            )

        except Exception as e:
            # Fallback routing logic
            next_agent = self._fallback_routing(state)
            
            return self._update_state(
                state,
                {
                    "next_action": next_agent,
                },
                f"Fallback routing to {next_agent}",
            )

    def _summarize_state(self, state: AgentState) -> str:
        """Create a summary of current state for supervisor."""
        summary_parts = []
        
        summary_parts.append(f"File: {state.get('file_path', 'unknown')}")
        summary_parts.append(f"Steps completed: {len(state.get('processing_steps', []))}")
        
        if state.get("document_type"):
            summary_parts.append(f"Document type: {state['document_type']}")
        else:
            summary_parts.append("Document type: NOT YET DETECTED")
        
        if state.get("structured_data"):
            summary_parts.append(f"Structured fields: {len(state['structured_data'])} extracted")
        else:
            summary_parts.append("Structured data: NOT YET EXTRACTED")
        
        if state.get("entities"):
            summary_parts.append(f"Entities: {len(state['entities'])} found")
        
        if state.get("tables"):
            summary_parts.append(f"Tables: {len(state['tables'])} detected")
        
        if state.get("confidence_score", 0) > 0:
            summary_parts.append(f"Confidence: {state['confidence_score']:.1%}")
        
        return "\n".join(summary_parts)

    def _parse_supervisor_decision(self, response: str) -> Dict[str, Any]:
        """Parse supervisor's routing decision."""
        try:
            if "```json" in response:
                json_str = response.split("```json")[1].split("```")[0].strip()
            elif "{" in response and "}" in response:
                start = response.index("{")
                end = response.rindex("}") + 1
                json_str = response[start:end]
            else:
                return {"next_agent": self._extract_agent_name(response)}

            return json.loads(json_str)

        except Exception:
            return {"next_agent": self._extract_agent_name(response)}

    def _extract_agent_name(self, text: str) -> str:
        """Extract agent name from text."""
        text_lower = text.lower()
        agents = ["planner", "vision", "schema", "extraction", "table_parser", "critic", "complete"]
        
        for agent in agents:
            if agent in text_lower:
                return agent
        
        return "complete"

    def _fallback_routing(self, state: AgentState) -> str:
        """Fallback routing logic if LLM fails."""
        steps = len(state.get("processing_steps", []))
        
        # Simple state machine fallback
        if steps == 0:
            return "planner"
        elif not state.get("document_type"):
            return "schema"
        elif not state.get("structured_data"):
            return "extraction"
        elif state.get("tables") and steps < 6:
            return "table_parser"
        elif not state.get("confidence_score") or state["confidence_score"] == 0:
            return "critic"
        else:
            return "complete"

