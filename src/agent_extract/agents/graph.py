"""LangGraph workflow with Supervisor-Planner-Critic architecture."""

from typing import Literal
from langgraph.graph import StateGraph, END
from langchain_core.runnables import RunnableConfig

from agent_extract.agents.state import AgentState
from agent_extract.agents.supervisor_agent import SupervisorAgent
from agent_extract.agents.planner_agent import PlannerAgent
from agent_extract.agents.critic_agent import CriticAgent
from agent_extract.agents.schema_agent import SchemaDetectionAgent
from agent_extract.agents.extraction_agent import ContentExtractionAgent
from agent_extract.agents.table_agent import TableParserAgent
from agent_extract.agents.vision_agent import DocumentVisionAgent


class DocumentExtractionGraph:
    """
    LangGraph-based multi-agent extraction workflow.
    
    Architecture: Supervisor-Planner-Critic with specialized sub-agents
    """

    def __init__(self, use_vision: bool = True):
        """
        Initialize the extraction graph.

        Args:
            use_vision: Whether to use vision model for image analysis
        """
        self.use_vision = use_vision
        
        # Initialize all agents
        self.supervisor_agent = SupervisorAgent()
        self.planner_agent = PlannerAgent()
        self.critic_agent = CriticAgent()
        self.schema_agent = SchemaDetectionAgent()
        self.extraction_agent = ContentExtractionAgent()
        self.table_agent = TableParserAgent()
        self.vision_agent = DocumentVisionAgent() if use_vision else None
        
        # Build graph
        self.graph = self._build_graph()

    def _build_graph(self) -> StateGraph:
        """Build the Supervisor-Planner-Critic workflow."""
        workflow = StateGraph(AgentState)

        # Add all agent nodes
        workflow.add_node("planner", self._planner_node)
        workflow.add_node("supervisor", self._supervisor_node)
        workflow.add_node("schema", self._schema_node)
        workflow.add_node("extraction", self._extraction_node)
        workflow.add_node("table_parser", self._table_node)
        workflow.add_node("critic", self._critic_node)
        
        if self.use_vision and self.vision_agent:
            workflow.add_node("vision", self._vision_node)

        # Define workflow edges
        # Start with Planner
        workflow.set_entry_point("planner")
        
        # Planner -> Supervisor
        workflow.add_edge("planner", "supervisor")
        
        # Supervisor routes to sub-agents or critic
        supervisor_routes = {
            "schema": "schema",
            "extraction": "extraction",
            "table_parser": "table_parser",
            "critic": "critic",
            "complete": END,
        }
        
        if self.use_vision and self.vision_agent:
            supervisor_routes["vision"] = "vision"
        
        workflow.add_conditional_edges(
            "supervisor",
            self._route_from_supervisor,
            supervisor_routes,
        )
        
        # All sub-agents return to Supervisor for next decision
        workflow.add_edge("schema", "supervisor")
        workflow.add_edge("extraction", "supervisor")
        workflow.add_edge("table_parser", "supervisor")
        
        if self.use_vision and self.vision_agent:
            workflow.add_edge("vision", "supervisor")
        
        # Critic can route back to supervisor or end
        workflow.add_conditional_edges(
            "critic",
            self._route_from_critic,
            {
                "supervisor": "supervisor",  # Re-extraction needed
                "complete": END,             # All good, finish
            },
        )

        return workflow.compile()

    async def _planner_node(self, state: AgentState) -> AgentState:
        """Planner creates extraction strategy."""
        return await self.planner_agent.process(state)

    async def _supervisor_node(self, state: AgentState) -> AgentState:
        """Supervisor decides next agent to run."""
        return await self.supervisor_agent.process(state)

    async def _schema_node(self, state: AgentState) -> AgentState:
        """Schema detection sub-agent."""
        return await self.schema_agent.process(state)

    async def _extraction_node(self, state: AgentState) -> AgentState:
        """Content extraction sub-agent."""
        return await self.extraction_agent.process(state)

    async def _table_node(self, state: AgentState) -> AgentState:
        """Table parsing sub-agent."""
        return await self.table_agent.process(state)

    async def _vision_node(self, state: AgentState) -> AgentState:
        """Vision analysis sub-agent."""
        return await self.vision_agent.process(state)

    async def _critic_node(self, state: AgentState) -> AgentState:
        """Critic evaluates extraction quality."""
        return await self.critic_agent.process(state)

    def _route_from_supervisor(self, state: AgentState) -> str:
        """Route from supervisor to next agent."""
        next_action = state.get("next_action", "complete")
        
        # Safety: prevent infinite loops
        max_steps = 10
        if len(state.get("processing_steps", [])) > max_steps:
            return "critic"  # Force completion via critic
        
        return next_action

    def _route_from_critic(self, state: AgentState) -> str:
        """Route from critic - either complete or re-extract."""
        next_action = state.get("next_action", "complete")
        
        # Safety: prevent re-extraction loops
        if next_action == "extraction" and len(state.get("processing_steps", [])) > 8:
            return "complete"  # Force completion
        
        if next_action == "complete":
            return "complete"
        
        return "supervisor"

    async def extract(self, initial_state: AgentState) -> AgentState:
        """
        Run the extraction workflow.

        Args:
            initial_state: Initial state with document data

        Returns:
            Final state with all extractions
        """
        # Set initial values (use setdefault to avoid duplication)
        initial_state.setdefault("processing_steps", [])
        initial_state.setdefault("errors", [])
        initial_state.setdefault("structured_data", {})
        initial_state.setdefault("tables", [])
        initial_state.setdefault("entities", [])
        initial_state.setdefault("confidence_score", 0.0)
        initial_state.setdefault("extraction_method", "ai_agents_supervised")

        # Run the graph with proper config
        config = RunnableConfig(
            recursion_limit=20,  # Allow more steps for supervisor pattern
            max_concurrency=1
        )
        
        try:
            final_state = await self.graph.ainvoke(initial_state, config)
            return final_state
        except Exception as e:
            # Add error to state and return
            initial_state["errors"].append(f"Workflow error: {str(e)}")
            initial_state["processing_steps"].append(f"Workflow failed: {str(e)}")
            return initial_state
