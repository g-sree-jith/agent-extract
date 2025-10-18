"""Custom exceptions for agent-extract."""


class AgentExtractError(Exception):
    """Base exception for all agent-extract errors."""

    pass


class DocumentReadError(AgentExtractError):
    """Raised when a document cannot be read or parsed."""

    pass


class OCRError(AgentExtractError):
    """Raised when OCR processing fails."""

    pass


class ExtractionError(AgentExtractError):
    """Raised when data extraction fails."""

    pass


class ValidationError(AgentExtractError):
    """Raised when output validation fails."""

    pass


class UnsupportedFormatError(AgentExtractError):
    """Raised when document format is not supported."""

    pass


class ConfigurationError(AgentExtractError):
    """Raised when configuration is invalid."""

    pass


