# Agent-Extract: Universal Document Intelligence Platform

> High-accuracy, multi-format document extraction with AI - Inspired by Landing.AI

[![Python 3.12+](https://img.shields.io/badge/python-3.12+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](CONTRIBUTING.md)
[![GitHub issues](https://img.shields.io/github/issues/g-sree-jith/agent-extract)](https://github.com/g-sree-jith/agent-extract/issues)
[![GitHub stars](https://img.shields.io/github/stars/g-sree-jith/agent-extract)](https://github.com/g-sree-jith/agent-extract/stargazers)

## 🎯 Overview

**Agent-Extract** is an intelligent document extraction platform that uses AI to accurately extract structured data from various document formats. Unlike traditional OCR tools, Agent-Extract understands document context and structure to provide high-accuracy extraction.

### Key Features

- ✅ **Multiple Format Support**: PDF, DOCX, images (PNG, JPG, TIFF), and more
- 🤖 **AI-Powered**: Uses LLMs and vision models for intelligent extraction
- 📊 **Table Extraction**: Accurately extracts complex tables with relationships
- 🎨 **Flexible Output**: Export as JSON or Markdown
- 🔧 **Easy to Use**: Simple CLI interface and Python API
- 🏠 **Privacy-First**: Process documents locally, no cloud upload required
- ⚡ **Fast Processing**: Optimized for speed without sacrificing accuracy

## 🚀 Quick Start

### Installation

```bash
# Install with uv (recommended)
uv sync

# Or with pip
pip install -e .
```

### Basic Usage

```bash
# Extract data from a PDF
agent-extract document.pdf

# Save as JSON
agent-extract document.pdf --output result.json

# Extract as Markdown
agent-extract document.pdf --format markdown --output result.md

# Batch process multiple documents
agent-extract batch ./documents ./output --format json

# Show supported formats
agent-extract info
```

### Python API

```python
from pathlib import Path
from agent_extract.readers.factory import ReaderFactory
from agent_extract.ocr.ocr_manager import OCRManager
from agent_extract.outputs.json_formatter import JSONFormatter

# Initialize OCR and reader factory
ocr_engine = OCRManager.from_config()
factory = ReaderFactory(ocr_engine=ocr_engine)

# Extract from a document
reader = factory.get_reader(Path("document.pdf"))
result = reader.read(Path("document.pdf"))

# Format as JSON
formatter = JSONFormatter()
json_output = formatter.format(result)
print(json_output)
```

## 📦 Supported Formats

| Format | Extensions | Status |
|--------|-----------|---------|
| PDF | `.pdf` | ✅ Supported |
| Word | `.docx` | ✅ Supported |
| Images | `.png`, `.jpg`, `.jpeg`, `.tiff` | ✅ Supported |
| Excel | `.xlsx`, `.csv` | 🔄 Coming in Phase 2 |
| PowerPoint | `.pptx` | 🔄 Coming in Phase 2 |
| HTML | `.html` | 🔄 Coming in Phase 2 |

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     CLI / Python API                         │
└─────────────────────────────────────────────────────────────┘
                              │
┌─────────────────────────────────────────────────────────────┐
│               Document Readers (PDF, DOCX, Image)            │
└─────────────────────────────────────────────────────────────┘
                              │
         ┌────────────────────┴────────────────────┐
         │                                         │
┌────────▼────────────┐                 ┌─────────▼──────────┐
│   OCR Engines       │                 │  AI Agents         │
│   (PaddleOCR)       │                 │  (Phase 2)         │
└─────────────────────┘                 └────────────────────┘
                              │
┌─────────────────────────────────────────────────────────────┐
│              Output Formatters (JSON, Markdown)              │
└─────────────────────────────────────────────────────────────┘
```

## 🔧 Configuration

Create a `.env` file in your project root:

```env
# OCR Settings
OCR_ENGINE=paddle
OCR_LANGUAGE=en

# LLM Settings (for Phase 2)
LLM_MODEL=llama3.1
LLM_VISION_MODEL=llama3.2-vision
LLM_BASE_URL=http://localhost:11434

# Processing
MAX_FILE_SIZE_MB=50
DEFAULT_OUTPUT_FORMAT=json
```

## 📚 Documentation

- [Project Plan](PROJECT_PLAN.md) - Complete project roadmap
- [API Documentation](docs/api.md) - Coming soon
- [Examples](docs/examples.md) - Coming soon

## 🧪 Development

### Setup Development Environment

```bash
# Install with dev dependencies
uv sync --all-extras

# Or with pip
pip install -e ".[dev]"
```

### Run Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=src/agent_extract

# Run specific test file
pytest tests/unit/test_readers.py
```

### Code Quality

```bash
# Format code
black src/ tests/

# Lint code
ruff check src/ tests/

# Type checking
mypy src/
```

## 📋 Project Status

### Phase 1: Foundation & Core Extraction (✅ COMPLETED)
- ✅ Project structure and configuration
- ✅ PDF, DOCX, and Image readers
- ✅ OCR integration (PaddleOCR + Tesseract)
- ✅ JSON and Markdown formatters
- ✅ CLI interface
- ✅ Unit tests

### Phase 2: AI Intelligence Layer (🔄 Next)
- 🔄 LangGraph agent orchestration
- 🔄 Document type detection
- 🔄 Advanced table extraction
- 🔄 Vision model integration

### Phase 3: Production Features (📅 Planned)
- 📅 REST API
- 📅 Batch processing optimization
- 📅 Caching system
- 📅 Comprehensive testing

### Phase 4: Optimization (📅 Planned)
- 📅 Performance optimization
- 📅 Additional format support
- 📅 Custom schema support
- 📅 Deployment guides

## 🤝 Contributing

Contributions are welcome! Please read our contributing guidelines and submit pull requests.

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- Inspired by [Landing.AI](https://landing.ai/) Document Intelligence
- Built with [LangChain](https://www.langchain.com/) and [LangGraph](https://github.com/langchain-ai/langgraph)
- OCR powered by [PaddleOCR](https://github.com/PaddlePaddle/PaddleOCR)

## 📞 Support

- 🐛 **Issues**: [GitHub Issues](https://github.com/g-sree-jith/agent-extract/issues)
- 💬 **Discussions**: [GitHub Discussions](https://github.com/g-sree-jith/agent-extract/discussions)
- 📖 **Documentation**: Check out [USAGE_GUIDE.md](USAGE_GUIDE.md) and [PROJECT_PLAN.md](PROJECT_PLAN.md)

## 🤝 Contributing

We welcome contributions! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

### Quick Contribution Guide

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 🌟 Star History

If you find this project useful, please consider giving it a star! ⭐

## 📜 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

**Made with ❤️ by [Sreejith G](https://github.com/g-sree-jith)**

*Inspired by [Landing.AI](https://landing.ai/) - Built for the community*


