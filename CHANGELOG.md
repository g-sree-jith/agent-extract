# Changelog

All notable changes to Agent-Extract will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.1.0] - 2025-10-18

### Added - Phase 1 Complete ✅

#### Core Features
- PDF extraction using PyMuPDF and pdfplumber
- DOCX extraction using python-docx
- Image extraction with OCR support
- Dual OCR engine support (PaddleOCR + Tesseract)
- JSON output formatter with Pydantic validation
- Markdown output formatter
- Reader factory with automatic format detection
- Configuration management with environment variables

#### CLI Interface
- `extract` command - Extract from single document
- `batch` command - Batch process multiple documents
- `info` command - Show supported formats and configuration
- `version` command - Show version information
- Rich console output with progress indicators

#### Testing & Quality
- Unit tests for core modules
- Unit tests for readers
- Unit tests for formatters
- Pytest configuration
- Code coverage setup

#### Documentation
- Comprehensive README with examples
- Complete PROJECT_PLAN with 8-week roadmap
- USAGE_GUIDE with API documentation
- QUICK_REFERENCE command cheat sheet
- INSTALLATION guide
- CONTRIBUTING guidelines
- LOCAL_MODELS guide for Ollama setup
- GETTING_STARTED quick guide

### Configuration
- Default LLM: qwen3:0.6b (lightweight, tool calling support)
- Default Vision Model: gemma3:4b (multimodal capabilities)
- Optimized for local processing
- Windows console compatibility

### Fixed
- Windows console encoding issues (charmap codec errors)
- Progress indicators compatible with Windows PowerShell
- Correct CLI command structure in documentation

### Changed
- Moved internal documentation to `docs/` folder
- Removed redundant publishing documentation
- Cleaned up root directory structure
- Updated .gitignore for better organization

### Security
- No API keys or secrets in code
- Personal documents excluded from repository
- Environment variables for sensitive configuration

## [0.2.0] - 2025-10-18

### Added - Phase 2: AI Intelligence Layer ✅

#### Supervisor-Planner-Critic Architecture
- **Supervisor Agent** - Intelligent workflow orchestration and routing
- **Planner Agent** - Creates extraction strategy per document
- **Critic Agent** - Quality assurance and validation

#### Specialized Sub-Agents
- **Schema Detection Agent** - Automatic document type classification
- **Content Extraction Agent** - Structured data and entity extraction  
- **Table Parser Agent** - AI-enhanced table understanding
- **Vision Agent** - Image layout analysis (gemma3:4b)

#### LangGraph Integration
- Multi-agent workflow orchestration
- State management for agent communication
- Conditional routing based on document type
- Self-correcting workflow with critic feedback
- Prevents infinite loops with safety checks

#### AI Models
- **qwen3:0.6b** (522 MB) - Primary LLM with tool calling
- **gemma3:4b** (3.3 GB) - Vision model for images

#### Features
- Automatic document type detection (invoices, forms, tickets, etc.)
- Named entity recognition (persons, dates, amounts, locations)
- Key-value pair extraction
- Confidence scoring
- Quality validation
- Adaptive extraction plans

### CLI Enhancements
- `--ai` flag for AI-powered extraction
- `--no-vision` flag to skip vision model
- Processing step tracking
- AI agent status in output

### Documentation
- AGENT_WORKFLOW.md with Mermaid diagram
- docs/PHASE2_AI_FEATURES.md guide
- agent-orch.png visual workflow
- Updated README with new architecture
- Updated QUICK_REFERENCE with AI commands

### Testing
- Integration tests for agent workflow
- Agent state management tests
- Routing logic tests

### Performance
- Simple documents: 3-5 seconds
- Complex forms: 8-12 seconds  
- Scanned images: 10-15 seconds

## [Unreleased] - Phase 2.1 (Optimizations)

### Planned - Performance Improvements

- Reduce agent workflow loops
- Optimize supervisor routing logic
- Cache LLM responses
- Parallel agent execution where possible

## [Unreleased] - Phase 3 (Planned)

### Planned - Production Features

- FastAPI REST API
- Batch processing optimization
- Result caching system
- Confidence scoring
- Error recovery and retry logic
- API documentation with OpenAPI

## [Unreleased] - Phase 4 (Planned)

### Planned - Optimization & Enhancement

- Performance optimization
- Async processing
- Additional format support (Excel, PowerPoint, HTML)
- Custom schema support
- Docker containerization
- Deployment guides

---

## Version History

- **v0.1.0** (2025-10-18) - Phase 1 Complete: Foundation & Core Extraction

