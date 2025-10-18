"""
Agent-Extract: Universal Document Intelligence Platform

A high-accuracy, multi-format document extraction system that intelligently
extracts structured data from various document types and outputs in JSON/Markdown formats.
"""

__version__ = "0.1.0"
__author__ = "Agent-Extract Team"

from agent_extract.core.config import Config
from agent_extract.core.exceptions import (
    AgentExtractError,
    DocumentReadError,
    OCRError,
    ExtractionError,
    ValidationError,
)

__all__ = [
    "Config",
    "AgentExtractError",
    "DocumentReadError",
    "OCRError",
    "ExtractionError",
    "ValidationError",
]


