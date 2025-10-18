"""Table parser agent - enhanced table understanding with LLM."""

import json
from typing import List, Dict, Any

from agent_extract.agents.base_agent import BaseAgent
from agent_extract.agents.state import AgentState
from agent_extract.core.types import ExtractedTable


class TableParserAgent(BaseAgent):
    """Agent that enhances table extraction with LLM understanding."""

    def __init__(self):
        """Initialize table parser agent with qwen3."""
        super().__init__()

    async def process(self, state: AgentState) -> AgentState:
        """
        Enhance table extraction with LLM understanding.

        Args:
            state: Current agent state

        Returns:
            Updated state with enhanced table data
        """
        raw_text = state.get("raw_text", "")
        existing_tables = state.get("tables", [])
        
        # If we already have tables from basic extraction, enhance them
        if existing_tables:
            enhanced_tables = await self._enhance_existing_tables(existing_tables)
            
            return self._update_state(
                state,
                {
                    "tables": enhanced_tables,
                    "next_action": "validate",
                },
                f"Enhanced {len(enhanced_tables)} tables with AI understanding",
            )
        
        # Otherwise, try to detect tables from text
        detected_tables = await self._detect_tables_from_text(raw_text)
        
        return self._update_state(
            state,
            {
                "tables": detected_tables,
                "next_action": "validate",
            },
            f"Detected {len(detected_tables)} tables from text",
        )

    async def _enhance_existing_tables(
        self, tables: List[ExtractedTable]
    ) -> List[ExtractedTable]:
        """Enhance existing tables with AI understanding."""
        enhanced = []
        
        for table in tables:
            try:
                # Create prompt for table understanding
                system_prompt = """You are a table analysis expert. Analyze the table and:
1. Verify if headers are correctly identified
2. Suggest better header names if needed
3. Identify data types of columns
4. Flag any inconsistencies

Respond in JSON: {"headers": [...], "data_types": [...], "issues": [...]}"""

                table_text = self._table_to_text(table)
                user_prompt = f"Analyze this table:\n\n{table_text}"

                messages = self._create_prompt(system_prompt, user_prompt)
                response = await self._invoke_llm(messages)
                
                # Parse and apply enhancements
                analysis = self._parse_table_analysis(response)
                
                # Use improved headers if suggested
                if analysis.get("headers"):
                    table.headers = analysis["headers"]
                
                enhanced.append(table)
                
            except Exception as e:
                # If enhancement fails, keep original
                enhanced.append(table)
        
        return enhanced

    async def _detect_tables_from_text(self, text: str) -> List[ExtractedTable]:
        """Detect tables from plain text using LLM."""
        system_prompt = """You are a table detection expert. Identify tabular data in the text.
For each table found, respond with JSON:
{
  "tables": [
    {
      "headers": ["col1", "col2"],
      "rows": [["val1", "val2"]]
    }
  ]
}"""

        user_prompt = f"""Find any tabular data in this text:

{text[:2000]}

Extract tables with their headers and data."""

        try:
            messages = self._create_prompt(system_prompt, user_prompt)
            response = await self._invoke_llm(messages)
            
            data = self._parse_table_detection(response)
            tables = []
            
            for table_data in data.get("tables", []):
                tables.append(
                    ExtractedTable(
                        headers=table_data.get("headers", []),
                        rows=table_data.get("rows", []),
                    )
                )
            
            return tables

        except Exception as e:
            return []

    def _table_to_text(self, table: ExtractedTable) -> str:
        """Convert table to readable text format."""
        lines = []
        
        # Headers
        if table.headers:
            lines.append("| " + " | ".join(table.headers) + " |")
            lines.append("| " + " | ".join(["---"] * len(table.headers)) + " |")
        
        # Rows
        for row in table.rows[:10]:  # Limit to first 10 rows
            lines.append("| " + " | ".join(str(cell) for cell in row) + " |")
        
        if len(table.rows) > 10:
            lines.append(f"... ({len(table.rows) - 10} more rows)")
        
        return "\n".join(lines)

    def _parse_table_analysis(self, response: str) -> Dict[str, Any]:
        """Parse table analysis response."""
        try:
            if "```json" in response:
                json_str = response.split("```json")[1].split("```")[0].strip()
            elif "```" in response:
                json_str = response.split("```")[1].split("```")[0].strip()
            else:
                json_str = response.strip()

            return json.loads(json_str)

        except Exception:
            return {}

    def _parse_table_detection(self, response: str) -> Dict[str, Any]:
        """Parse table detection response."""
        return self._parse_table_analysis(response)

