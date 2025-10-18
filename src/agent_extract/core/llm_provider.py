"""LLM provider abstraction for multiple backends (Ollama, OpenAI, Gemini, Groq)."""

from typing import Optional, Literal
from enum import Enum

from langchain_core.language_models import BaseChatModel
from agent_extract.core.config import config
from agent_extract.core.exceptions import ConfigurationError


class LLMProvider(str, Enum):
    """Available LLM providers."""

    OLLAMA = "ollama"
    OPENAI = "openai"
    GEMINI = "gemini"
    GROQ = "groq"
    ANTHROPIC = "anthropic"


class LLMFactory:
    """Factory for creating LLM instances from different providers."""

    @staticmethod
    def create_llm(
        provider: Optional[str] = None,
        model_name: Optional[str] = None,
        temperature: float = 0.1,
        api_key: Optional[str] = None,
        is_vision: bool = False,
    ) -> BaseChatModel:
        """
        Create an LLM instance from the specified provider.

        Args:
            provider: LLM provider (ollama, openai, gemini, groq)
            model_name: Model name
            temperature: LLM temperature
            api_key: API key for cloud providers
            is_vision: Whether this is a vision model

        Returns:
            BaseChatModel instance

        Raises:
            ConfigurationError: If provider is not supported or misconfigured
        """
        # Use defaults from config if not specified
        provider = provider or config.llm_provider
        
        if is_vision:
            model_name = model_name or config.llm_vision_model
        else:
            model_name = model_name or config.llm_model
        
        # Get API key for the provider
        if not api_key:
            if provider == "openai":
                api_key = config.openai_api_key or config.llm_api_key
            elif provider == "gemini":
                api_key = config.gemini_api_key or config.llm_api_key
            elif provider == "groq":
                api_key = config.groq_api_key or config.llm_api_key
            elif provider == "anthropic":
                api_key = config.anthropic_api_key or config.llm_api_key

        # Create LLM based on provider
        if provider == LLMProvider.OLLAMA:
            return LLMFactory._create_ollama(model_name, temperature)
        
        elif provider == LLMProvider.OPENAI:
            return LLMFactory._create_openai(model_name, temperature, api_key, is_vision)
        
        elif provider == LLMProvider.GEMINI:
            return LLMFactory._create_gemini(model_name, temperature, api_key, is_vision)
        
        elif provider == LLMProvider.GROQ:
            return LLMFactory._create_groq(model_name, temperature, api_key)
        
        elif provider == LLMProvider.ANTHROPIC:
            return LLMFactory._create_anthropic(model_name, temperature, api_key, is_vision)
        
        else:
            raise ConfigurationError(
                f"Unsupported LLM provider: {provider}. "
                f"Supported: {[p.value for p in LLMProvider]}"
            )

    @staticmethod
    def _create_ollama(model_name: str, temperature: float) -> BaseChatModel:
        """Create Ollama LLM."""
        try:
            from langchain_ollama import ChatOllama

            return ChatOllama(
                model=model_name,
                temperature=temperature,
                base_url=config.llm_base_url,
            )
        except ImportError as e:
            raise ConfigurationError(
                "langchain-ollama not installed. Install with: pip install langchain-ollama"
            ) from e

    @staticmethod
    def _create_openai(
        model_name: str,
        temperature: float,
        api_key: Optional[str],
        is_vision: bool,
    ) -> BaseChatModel:
        """Create OpenAI LLM."""
        try:
            from langchain_openai import ChatOpenAI

            if not api_key:
                raise ConfigurationError("OpenAI API key not provided. Set OPENAI_API_KEY in environment.")

            # Default models if not specified
            if not model_name or model_name in ["qwen3:0.6b", "gemma3:4b"]:
                if is_vision:
                    model_name = "gpt-4-vision-preview"  # Or "gpt-4o" for newer
                else:
                    model_name = "gpt-4o-mini"  # Fast and cost-effective

            return ChatOpenAI(
                model=model_name,
                temperature=temperature,
                api_key=api_key,
            )
        except ImportError as e:
            raise ConfigurationError(
                "langchain-openai not installed. Install with: pip install langchain-openai"
            ) from e

    @staticmethod
    def _create_gemini(
        model_name: str,
        temperature: float,
        api_key: Optional[str],
        is_vision: bool,
    ) -> BaseChatModel:
        """Create Google Gemini LLM."""
        try:
            from langchain_google_genai import ChatGoogleGenerativeAI

            if not api_key:
                raise ConfigurationError("Gemini API key not provided. Set GEMINI_API_KEY in environment.")

            # Default models - use correct Gemini naming
            if not model_name or model_name in ["qwen3:0.6b", "gemma3:4b"]:
                # Use gemini-pro for both text and vision
                model_name = "gemini-pro"
            elif model_name == "gemini-1.5-flash":
                # Map to correct name
                model_name = "gemini-pro"

            return ChatGoogleGenerativeAI(
                model=model_name,
                temperature=temperature,
                google_api_key=api_key,
            )
        except ImportError as e:
            raise ConfigurationError(
                "langchain-google-genai not installed. Install with: pip install langchain-google-genai"
            ) from e

    @staticmethod
    def _create_groq(
        model_name: str,
        temperature: float,
        api_key: Optional[str],
    ) -> BaseChatModel:
        """Create Groq LLM."""
        try:
            from langchain_groq import ChatGroq

            if not api_key:
                raise ConfigurationError("Groq API key not provided. Set GROQ_API_KEY in environment.")

            # Default model if not specified
            if not model_name or model_name in ["qwen3:0.6b", "gemma3:4b"]:
                model_name = "llama-3.3-70b-versatile"  # Fast and powerful

            return ChatGroq(
                model=model_name,
                temperature=temperature,
                api_key=api_key,
            )
        except ImportError as e:
            raise ConfigurationError(
                "langchain-groq not installed. Install with: pip install langchain-groq"
            ) from e

    @staticmethod
    def _create_anthropic(
        model_name: str,
        temperature: float,
        api_key: Optional[str],
        is_vision: bool,
    ) -> BaseChatModel:
        """Create Anthropic Claude LLM."""
        try:
            from langchain_anthropic import ChatAnthropic

            if not api_key:
                raise ConfigurationError("Anthropic API key not provided. Set ANTHROPIC_API_KEY in environment.")

            # Default models
            if not model_name or model_name in ["qwen3:0.6b", "gemma3:4b"]:
                if is_vision:
                    model_name = "claude-3-5-sonnet-20241022"  # Supports vision
                else:
                    model_name = "claude-3-5-haiku-20241022"  # Fast

            return ChatAnthropic(
                model=model_name,
                temperature=temperature,
                api_key=api_key,
            )
        except ImportError as e:
            raise ConfigurationError(
                "langchain-anthropic not installed. Install with: pip install langchain-anthropic"
            ) from e


def get_default_llm(is_vision: bool = False) -> BaseChatModel:
    """
    Get default LLM based on configuration.

    Args:
        is_vision: Whether to get vision model

    Returns:
        Configured LLM instance
    """
    return LLMFactory.create_llm(is_vision=is_vision)

