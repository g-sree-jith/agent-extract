"""Configuration management for agent-extract."""

import os
from pathlib import Path
from typing import Optional
from pydantic_settings import BaseSettings
from pydantic import Field


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
    
    # LLM settings (optimized for local models)
    llm_model: str = Field(default="qwen3:0.6b", description="Ollama model name (tool calling)")
    llm_vision_model: str = Field(default="gemma3:4b", description="Vision model name")
    llm_base_url: str = Field(default="http://localhost:11434", description="Ollama base URL")
    llm_temperature: float = Field(default=0.1, description="LLM temperature")
    llm_max_tokens: int = Field(default=4096, description="Max tokens for LLM")
    
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
    
    class Config:
        """Pydantic settings config."""

        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False

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


# Global config instance
config = Config()


