"""Integration tests for AI-powered extraction."""

import pytest
import asyncio
from pathlib import Path

from agent_extract.ai_extractor import AIDocumentExtractor
from agent_extract.agents.graph import DocumentExtractionGraph
from agent_extract.agents.state import AgentState


@pytest.mark.asyncio
class TestAIExtraction:
    """Tests for AI document extraction."""

    async def test_extraction_graph_creation(self):
        """Test that extraction graph can be created."""
        graph = DocumentExtractionGraph(use_vision=True)
        assert graph is not None
        assert graph.schema_agent is not None
        assert graph.extraction_agent is not None
        assert graph.table_agent is not None
        assert graph.validation_agent is not None

    async def test_basic_agent_workflow(self):
        """Test basic agent workflow with sample state."""
        graph = DocumentExtractionGraph(use_vision=False)
        
        initial_state: AgentState = {
            "file_path": "test.pdf",
            "raw_text": "Invoice #12345 dated 2025-01-15. Amount: $100.",
            "ocr_text": None,
            "image_data": None,
            "document_type": None,
            "confidence_score": 0.0,
            "detected_schema": None,
            "structured_data": {},
            "tables": [],
            "entities": [],
            "extraction_method": "ai_agents",
            "processing_steps": [],
            "errors": [],
            "current_agent": "init",
            "next_action": None,
            "extraction_result": None,
        }

        # Run workflow
        final_state = await graph.extract(initial_state)

        # Verify workflow completed
        assert final_state is not None
        assert "processing_steps" in final_state
        assert len(final_state["processing_steps"]) > 0

    async def test_schema_detection(self):
        """Test schema detection agent."""
        from agent_extract.agents.schema_agent import SchemaDetectionAgent

        agent = SchemaDetectionAgent()
        state: AgentState = {
            "file_path": "invoice.pdf",
            "raw_text": "Invoice #12345\nDate: 2025-01-15\nAmount: $100\nCustomer: John Doe",
            "ocr_text": None,
            "image_data": None,
            "document_type": None,
            "confidence_score": 0.0,
            "detected_schema": None,
            "structured_data": {},
            "tables": [],
            "entities": [],
            "extraction_method": "ai_agents",
            "processing_steps": [],
            "errors": [],
            "current_agent": "init",
            "next_action": None,
            "extraction_result": None,
        }

        result_state = await agent.process(state)

        # Check schema detection occurred
        assert result_state["detected_schema"] is not None
        assert "document_type" in result_state["detected_schema"]
        assert result_state["confidence_score"] > 0


@pytest.mark.asyncio
class TestAIDocumentExtractor:
    """Tests for AIDocumentExtractor class."""

    def test_extractor_initialization(self):
        """Test AI extractor can be initialized."""
        extractor = AIDocumentExtractor(use_vision=True)
        assert extractor is not None
        assert extractor.agent_graph is not None

    def test_extractor_initialization_no_vision(self):
        """Test AI extractor without vision."""
        extractor = AIDocumentExtractor(use_vision=False)
        assert extractor is not None
        assert extractor.agent_graph is not None


# Sync tests for pytest compatibility
class TestAIExtractionSync:
    """Synchronous tests for AI extraction."""

    def test_can_create_extractor(self):
        """Test that AI extractor can be created."""
        extractor = AIDocumentExtractor()
        assert extractor is not None

    def test_has_required_components(self):
        """Test that extractor has all required components."""
        extractor = AIDocumentExtractor()
        assert extractor.ocr_manager is not None
        assert extractor.reader_factory is not None
        assert extractor.agent_graph is not None

