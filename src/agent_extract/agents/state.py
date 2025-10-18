"""State management for LangGraph agent workflow."""

from typing import TypedDict, List, Dict, Any, Optional, Annotated
from operator import add

from agent_extract.core.types import (
    DocumentType,
    ExtractionResult,
    ExtractedTable,
    ExtractedEntity,
)


class AgentState(TypedDict):
    """State shared between agents in the extraction workflow."""

    # Input
    file_path: str
    raw_text: str
    ocr_text: Optional[str]
    image_data: Optional[bytes]
    
    # Document understanding
    document_type: Optional[DocumentType]
    confidence_score: float
    detected_schema: Optional[Dict[str, Any]]
    
    # Extracted data
    structured_data: Dict[str, Any]
    tables: Annotated[List[ExtractedTable], add]  # Can append tables
    entities: Annotated[List[ExtractedEntity], add]  # Can append entities
    
    # Processing metadata
    extraction_method: str
    processing_steps: Annotated[List[str], add]  # Track agent steps
    errors: Annotated[List[str], add]  # Track any errors
    
    # Agent communication
    current_agent: str
    next_action: Optional[str]
    
    # Final result
    extraction_result: Optional[ExtractionResult]


class DocumentContext(TypedDict):
    """Additional context for document understanding."""

    file_name: str
    file_size: int
    page_count: Optional[int]
    has_tables: bool
    has_images: bool
    language: str
    is_scanned: bool

