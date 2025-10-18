"""AI-powered document extractor using LangGraph agents."""

import asyncio
from pathlib import Path
from typing import Optional
import time

from agent_extract.core.types import ExtractionResult, DocumentMetadata, DocumentType
from agent_extract.core.config import config
from agent_extract.readers.factory import ReaderFactory
from agent_extract.ocr.ocr_manager import OCRManager
from agent_extract.agents.graph import DocumentExtractionGraph
from agent_extract.agents.state import AgentState


class AIDocumentExtractor:
    """
    AI-powered document extractor using multi-agent workflow.
    
    Uses qwen3:0.6b for extraction and gemma3:4b for vision understanding.
    """

    def __init__(
        self,
        use_vision: bool = True,
        use_basic_extraction: bool = True,
    ):
        """
        Initialize AI document extractor.

        Args:
            use_vision: Use vision model (gemma3:4b) for images
            use_basic_extraction: Use basic readers first, then enhance with AI
        """
        self.use_vision = use_vision and config.enable_vision_model
        self.use_basic_extraction = use_basic_extraction
        
        # Initialize basic components
        self.ocr_manager = OCRManager.from_config()
        self.reader_factory = ReaderFactory(ocr_engine=self.ocr_manager)
        
        # Initialize AI agent graph
        self.agent_graph = DocumentExtractionGraph(use_vision=self.use_vision)

    async def extract(self, file_path: Path) -> ExtractionResult:
        """
        Extract data from document using AI agents.

        Args:
            file_path: Path to the document

        Returns:
            ExtractionResult with AI-enhanced data
        """
        start_time = time.time()

        # Step 1: Basic extraction (OCR, text, tables)
        if self.use_basic_extraction:
            basic_result = await self._basic_extraction(file_path)
        else:
            basic_result = None

        # Step 2: Prepare state for agents
        initial_state = self._prepare_agent_state(file_path, basic_result)

        # Step 3: Run AI agent workflow
        final_state = await self.agent_graph.extract(initial_state)

        # Step 4: Build final extraction result
        processing_time = time.time() - start_time
        result = self._build_extraction_result(
            file_path,
            basic_result,
            final_state,
            processing_time,
        )

        return result

    def extract_sync(self, file_path: Path) -> ExtractionResult:
        """
        Synchronous wrapper for extract method.

        Args:
            file_path: Path to the document

        Returns:
            ExtractionResult
        """
        return asyncio.run(self.extract(file_path))

    async def _basic_extraction(self, file_path: Path) -> ExtractionResult:
        """Run basic extraction (Phase 1 readers)."""
        reader = self.reader_factory.get_reader(file_path)
        
        # Run in executor to avoid blocking
        loop = asyncio.get_event_loop()
        result = await loop.run_in_executor(None, reader.read, file_path)
        
        return result

    def _prepare_agent_state(
        self,
        file_path: Path,
        basic_result: Optional[ExtractionResult],
    ) -> AgentState:
        """Prepare initial state for agent workflow."""
        if basic_result:
            # Use basic extraction as starting point
            state: AgentState = {
                "file_path": str(file_path),
                "raw_text": basic_result.raw_text,
                "ocr_text": basic_result.raw_text if basic_result.extraction_method == "image_ocr" else None,
                "image_data": None,
                "document_type": None,
                "confidence_score": 0.0,
                "detected_schema": None,
                "structured_data": basic_result.structured_data or {},
                "tables": basic_result.tables or [],
                "entities": basic_result.entities or [],
                "extraction_method": "ai_hybrid",
                "processing_steps": ["Basic extraction completed"],
                "errors": [],
                "current_agent": "init",
                "next_action": None,
                "extraction_result": None,
            }
        else:
            # Start from scratch
            state: AgentState = {
                "file_path": str(file_path),
                "raw_text": "",
                "ocr_text": None,
                "image_data": None,
                "document_type": None,
                "confidence_score": 0.0,
                "detected_schema": None,
                "structured_data": {},
                "tables": [],
                "entities": [],
                "extraction_method": "ai_only",
                "processing_steps": [],
                "errors": [],
                "current_agent": "init",
                "next_action": None,
                "extraction_result": None,
            }

        return state

    def _build_extraction_result(
        self,
        file_path: Path,
        basic_result: Optional[ExtractionResult],
        final_state: AgentState,
        processing_time: float,
    ) -> ExtractionResult:
        """Build final extraction result from agent state."""
        # Use basic metadata if available, otherwise create new
        if basic_result:
            metadata = basic_result.metadata
        else:
            stat = file_path.stat()
            metadata = DocumentMetadata(
                filename=file_path.name,
                file_size=stat.st_size,
                document_type=final_state.get("document_type", DocumentType.UNKNOWN),
                page_count=None,
            )

        # Build result
        result = ExtractionResult(
            metadata=metadata,
            raw_text=final_state.get("raw_text", ""),
            structured_data=final_state.get("structured_data", {}),
            tables=final_state.get("tables", []),
            entities=final_state.get("entities", []),
            confidence_score=final_state.get("confidence_score"),
            processing_time=processing_time,
            extraction_method=final_state.get("extraction_method", "ai_agents"),
        )

        # Add processing metadata
        result.structured_data["ai_processing"] = {
            "agents_used": final_state.get("processing_steps", []),
            "detected_document_type": final_state.get("detected_schema", {}).get("document_type"),
            "errors": final_state.get("errors", []),
        }

        return result

