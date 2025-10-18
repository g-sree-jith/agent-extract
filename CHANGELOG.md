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

## [Unreleased] - Phase 2 (Planned)

### Planned - AI Intelligence Layer

- LangGraph multi-agent orchestration
- Schema detection agent
- Content extraction agent
- Table parser agent
- Validation agent
- Vision model integration for layout analysis
- Named entity recognition
- Form field detection

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

