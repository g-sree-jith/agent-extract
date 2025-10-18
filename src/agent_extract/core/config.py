"""Configuration management for agent-extract."""

import os
from pathlib import Path
from typing import Optional
from pydantic_settings import BaseSettings
from pydantic import Field


# Get API keys from environment with provider-specific fallbacks
def _get_api_key_for_provider(provider: str) -> Optional[str]:
    """Get API key for specified provider."""
    provider_key_map = {
        "openai": "OPENAI_API_KEY",
        "gemini": "GEMINI_API_KEY",
        "groq": "GROQ_API_KEY",
        "anthropic": "ANTHROPIC_API_KEY",
    }
    key_name = provider_key_map.get(provider.lower())
    if key_name:
        return os.getenv(key_name) or os.getenv("LLM_API_KEY")
    return os.getenv("LLM_API_KEY")


class Config(BaseSettings):
    """Application configuration."""

    # Application settings
    app_name: str = "agent-extract"
    version: str = "0.1.0"
    debug: bool = Field(default=False, description="Enable debug mode")

    # Document processing settings
    max_file_size_mb: int = Field(default=50, description="Maximum file size in MB")
    default_output_format: str = Field(default="json", description="Default output format")
    
    # OCR settings
    ocr_engine: str = Field(default="tesseract", description="Default OCR engine")
    ocr_language: str = Field(default="eng", description="OCR language (tesseract: eng, paddle: en)")
    ocr_confidence_threshold: float = Field(default=0.5, description="Minimum OCR confidence")
    
    # LLM settings (supports local and cloud providers)
    llm_provider: str = Field(
        default="ollama",
        description="LLM provider: ollama (local), openai, gemini, groq, anthropic"
    )
    llm_model: str = Field(
        default="qwen3:0.6b",
        description="Model name (qwen3:0.6b for ollama, gpt-4o-mini for openai, etc.)"
    )
    llm_vision_model: str = Field(
        default="gemma3:4b",
        description="Vision model (gemma3:4b for ollama, gpt-4o for openai, etc.)"
    )
    llm_base_url: str = Field(default="http://localhost:11434", description="Ollama base URL")
    llm_temperature: float = Field(default=0.1, description="LLM temperature")
    llm_max_tokens: int = Field(default=4096, description="Max tokens for LLM")
    
    # API Keys for cloud providers (optional)
    llm_api_key: Optional[str] = Field(default=None, description="API key for cloud providers")
    openai_api_key: Optional[str] = Field(default=None, description="OpenAI API key")
    gemini_api_key: Optional[str] = Field(default=None, description="Google Gemini API key")
    groq_api_key: Optional[str] = Field(default=None, description="Groq API key")
    anthropic_api_key: Optional[str] = Field(default=None, description="Anthropic API key")
    
    # Processing settings
    enable_table_extraction: bool = Field(default=True, description="Enable table extraction")
    enable_entity_extraction: bool = Field(default=True, description="Enable entity extraction")
    enable_vision_model: bool = Field(default=True, description="Enable vision model")
    parallel_processing: bool = Field(default=False, description="Enable parallel processing")
    
    # Cache settings
    enable_cache: bool = Field(default=True, description="Enable result caching")
    cache_ttl_seconds: int = Field(default=3600, description="Cache TTL in seconds")
    
    # Paths
    data_dir: Path = Field(default=Path("data"), description="Data directory")
    cache_dir: Path = Field(default=Path(".cache"), description="Cache directory")
    models_dir: Path = Field(default=Path("models"), description="Models directory")
    
    # API settings (for Phase 3)
    api_host: str = Field(default="0.0.0.0", description="API host")
    api_port: int = Field(default=8000, description="API port")
    api_workers: int = Field(default=1, description="API workers")
    
    model_config = {
        "env_file": ".env",
        "env_file_encoding": "utf-8",
        "case_sensitive": False,
        "extra": "ignore",  # Ignore extra fields, don't error
        "populate_by_name": True,  # Allow field population by name
    }

    def __init__(self, **kwargs):
        """Initialize config and create necessary directories."""
        super().__init__(**kwargs)
        self._create_directories()

    def _create_directories(self):
        """Create necessary directories if they don't exist."""
        self.data_dir.mkdir(parents=True, exist_ok=True)
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        self.models_dir.mkdir(parents=True, exist_ok=True)

    @property
    def max_file_size_bytes(self) -> int:
        """Get max file size in bytes."""
        return self.max_file_size_mb * 1024 * 1024


# Load .env BEFORE creating config
from dotenv import load_dotenv
load_dotenv(override=True)

# Global config instance
config = Config()


