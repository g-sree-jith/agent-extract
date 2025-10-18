"""Base agent class for all extraction agents."""

from abc import ABC, abstractmethod
from typing import Dict, Any, Optional
from langchain_ollama import ChatOllama
from langchain_core.messages import SystemMessage, HumanMessage

from agent_extract.core.config import config
from agent_extract.agents.state import AgentState


class BaseAgent(ABC):
    """Abstract base class for all extraction agents."""

    def __init__(
        self,
        model_name: Optional[str] = None,
        temperature: float = 0.1,
        base_url: Optional[str] = None,
    ):
        """
        Initialize the base agent.

        Args:
            model_name: Ollama model name (defaults to config.llm_model)
            temperature: LLM temperature
            base_url: Ollama base URL
        """
        self.model_name = model_name or config.llm_model
        self.temperature = temperature
        self.base_url = base_url or config.llm_base_url
        
        # Initialize LLM
        self.llm = ChatOllama(
            model=self.model_name,
            temperature=self.temperature,
            base_url=self.base_url,
        )
        
        self.agent_name = self.__class__.__name__

    @abstractmethod
    async def process(self, state: AgentState) -> AgentState:
        """
        Process the state and return updated state.

        Args:
            state: Current agent state

        Returns:
            Updated agent state
        """
        pass

    def _create_prompt(self, system_msg: str, user_msg: str) -> list:
        """Create a prompt for the LLM."""
        return [
            SystemMessage(content=system_msg),
            HumanMessage(content=user_msg),
        ]

    async def _invoke_llm(self, messages: list) -> str:
        """Invoke the LLM and return the response."""
        try:
            response = await self.llm.ainvoke(messages)
            return response.content
        except Exception as e:
            raise RuntimeError(f"LLM invocation failed: {str(e)}") from e

    def _update_state(
        self,
        state: AgentState,
        updates: Dict[str, Any],
        step_description: str,
    ) -> AgentState:
        """
        Update state with new data and track processing step.

        Args:
            state: Current state
            updates: Dictionary of updates to apply
            step_description: Description of the processing step

        Returns:
            Updated state
        """
        # Update with new data
        new_state = {**state, **updates}
        
        # Track processing step
        if "processing_steps" not in new_state:
            new_state["processing_steps"] = []
        new_state["processing_steps"].append(
            f"[{self.agent_name}] {step_description}"
        )
        
        # Update current agent
        new_state["current_agent"] = self.agent_name
        
        return new_state


class VisionAgent(BaseAgent):
    """Base agent for vision-based extraction using multimodal models."""

    def __init__(
        self,
        model_name: Optional[str] = None,
        temperature: float = 0.1,
        base_url: Optional[str] = None,
    ):
        """
        Initialize vision agent.

        Args:
            model_name: Vision model name (defaults to config.llm_vision_model)
            temperature: LLM temperature
            base_url: Ollama base URL
        """
        # Use vision model by default
        vision_model = model_name or config.llm_vision_model
        super().__init__(
            model_name=vision_model,
            temperature=temperature,
            base_url=base_url,
        )

    async def _invoke_vision_llm(
        self,
        image_path: str,
        prompt: str,
    ) -> str:
        """
        Invoke vision model with image and text prompt.

        Args:
            image_path: Path to the image file
            prompt: Text prompt for the vision model

        Returns:
            Model response
        """
        try:
            # For vision models, we'll use the image understanding capabilities
            messages = self._create_prompt(
                system_msg="You are a document analysis expert. Analyze images and extract information.",
                user_msg=f"{prompt}\n\nImage path: {image_path}",
            )
            response = await self.llm.ainvoke(messages)
            return response.content
        except Exception as e:
            raise RuntimeError(f"Vision LLM invocation failed: {str(e)}") from e

