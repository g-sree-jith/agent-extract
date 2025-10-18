# Universal Document Extractor - Project Plan
## Mimicking Landing.AI Document Intelligence

---

## 📋 Executive Summary

**Project Name:** Agent-Extract - Universal Document Intelligence Platform  
**Objective:** Build a high-accuracy, multi-format document extraction system that intelligently extracts structured data from various document types and outputs in JSON/Markdown formats.

**Inspiration:** Landing.AI's Document Intelligence capabilities  
**Core Value Proposition:** Single API to extract data from any document format with AI-powered understanding, not just OCR.

---

## 🎯 Project Vision & Goals

### Primary Goals
1. **Universal Format Support**: Handle PDF, DOCX, images (PNG, JPG), scanned documents, and more
2. **High Accuracy Extraction**: Use multi-modal AI models for intelligent extraction beyond simple OCR
3. **Structured Output**: Convert unstructured documents into structured JSON or formatted Markdown
4. **Flexible Output**: User-selectable output format (JSON/Markdown)
5. **Production Ready**: Scalable, maintainable, and well-tested architecture

### Success Metrics
- Support for 5+ document formats
- 95%+ accuracy on typed documents
- 85%+ accuracy on handwritten/scanned documents
- < 5 second processing time for standard documents
- Clean API with comprehensive error handling

---

## 🏗️ Technical Architecture

### System Architecture Overview

```
┌─────────────────────────────────────────────────────────────┐
│                     User Interface Layer                     │
│            (CLI / API / Web Interface - Future)              │
└─────────────────────────────────────────────────────────────┘
                              │
┌─────────────────────────────────────────────────────────────┐
│                   Orchestration Layer                        │
│         (LangGraph - Agent Workflow & Routing)               │
└─────────────────────────────────────────────────────────────┘
                              │
         ┌────────────────────┴────────────────────┐
         │                                         │
┌────────▼────────────┐                 ┌─────────▼──────────┐
│  Document Readers   │                 │   AI Processors    │
│  - PDF Reader       │                 │   - LLM Parser     │
│  - DOCX Reader      │                 │   - Vision Models  │
│  - Image Reader     │                 │   - Schema Agent   │
│  - OCR Engine       │                 │   - Validator      │
└─────────────────────┘                 └────────────────────┘
         │                                         │
         └────────────────────┬────────────────────┘
                              │
┌─────────────────────────────────────────────────────────────┐
│                    Processing Pipeline                       │
│  1. Detection  2. Extraction  3. Structure  4. Validation   │
└─────────────────────────────────────────────────────────────┘
                              │
┌─────────────────────────────────────────────────────────────┐
│                     Output Formatters                        │
│              JSON Builder | Markdown Builder                 │
└─────────────────────────────────────────────────────────────┘
```

### Core Components

#### 1. **Document Ingestion Module**
- **File Type Detection**: Auto-detect document format
- **Format-Specific Readers**:
  - PDF Reader (PyMuPDF/pdfplumber)
  - DOCX Reader (python-docx)
  - Image Reader (Pillow + OCR)
  - CSV/Excel Reader (pandas)
- **Preprocessing**: Image enhancement, orientation correction, noise reduction

#### 2. **OCR & Vision Module**
- **Multi-Engine OCR**:
  - Primary: PaddleOCR (offline, high accuracy)
  - Secondary: Tesseract (fallback)
  - Optional: Cloud OCR (Azure/AWS for production)
- **Layout Analysis**: Detect regions (text, tables, images, headers)
- **Table Extraction**: Specialized table detection and parsing

#### 3. **AI Intelligence Layer**
- **LangGraph Orchestration**: Multi-agent workflow
- **Extraction Agents**:
  - Schema Detection Agent (identifies document type)
  - Content Extraction Agent (extracts relevant data)
  - Table Parser Agent (handles complex tables)
  - Validation Agent (ensures accuracy)
- **LLM Integration**:
  - Local: Ollama (llama3.2-vision, llama3.1)
  - Cloud: OpenAI/Anthropic (optional for higher accuracy)

#### 4. **Output Generation Module**
- **JSON Generator**: Structured schema-based output
- **Markdown Generator**: Human-readable formatted output
- **Schema Validation**: Pydantic models for type safety

#### 5. **API & Interface Layer**
- **FastAPI REST API**: Production-ready endpoints
- **CLI Tool**: Command-line interface
- **Batch Processing**: Handle multiple documents

---

## 🛠️ Technology Stack

### Core Technologies

| Category | Technology | Purpose |
|----------|-----------|---------|
| **Language** | Python 3.12+ | Core development |
| **Framework** | FastAPI | REST API (Phase 3) |
| **AI Orchestration** | LangGraph | Agent workflow & routing |
| **LLM** | Ollama (local) | Document understanding |
| **Vision Models** | llama3.2-vision | Image-based extraction |
| **PDF Processing** | PyMuPDF, pdfplumber | PDF parsing & extraction |
| **OCR** | PaddleOCR, Tesseract | Text extraction from images |
| **Document Parsing** | python-docx, openpyxl | Office document support |
| **Table Extraction** | camelot-py, pdfplumber | Complex table parsing |
| **Image Processing** | Pillow, OpenCV | Image preprocessing |
| **Validation** | Pydantic | Schema validation |
| **Testing** | pytest, pytest-cov | Testing framework |
| **CLI** | typer | Command-line interface |

### Additional Libraries
- **unstructured**: Multi-format document parsing
- **layoutparser**: Document layout analysis
- **transformers**: Optional: Hugging Face models
- **tiktoken**: Token counting
- **rich**: Beautiful CLI output

---

## 📁 Project Structure

```
agent-extract/
├── src/
│   ├── agent_extract/
│   │   ├── __init__.py
│   │   ├── core/
│   │   │   ├── __init__.py
│   │   │   ├── config.py          # Configuration management
│   │   │   ├── exceptions.py      # Custom exceptions
│   │   │   └── types.py           # Type definitions
│   │   ├── readers/
│   │   │   ├── __init__.py
│   │   │   ├── base.py            # Abstract base reader
│   │   │   ├── pdf_reader.py      # PDF extraction
│   │   │   ├── docx_reader.py     # DOCX extraction
│   │   │   ├── image_reader.py    # Image + OCR
│   │   │   ├── excel_reader.py    # Excel/CSV
│   │   │   └── factory.py         # Reader factory pattern
│   │   ├── ocr/
│   │   │   ├── __init__.py
│   │   │   ├── paddle_ocr.py      # PaddleOCR implementation
│   │   │   ├── tesseract_ocr.py   # Tesseract implementation
│   │   │   └── layout_analyzer.py # Layout detection
│   │   ├── agents/
│   │   │   ├── __init__.py
│   │   │   ├── graph.py           # LangGraph workflow
│   │   │   ├── schema_agent.py    # Document type detection
│   │   │   ├── extraction_agent.py # Content extraction
│   │   │   ├── table_agent.py     # Table parsing
│   │   │   └── validation_agent.py # Output validation
│   │   ├── processors/
│   │   │   ├── __init__.py
│   │   │   ├── preprocessor.py    # Image preprocessing
│   │   │   ├── table_processor.py # Table extraction
│   │   │   └── structure_parser.py # Document structure
│   │   ├── outputs/
│   │   │   ├── __init__.py
│   │   │   ├── json_formatter.py  # JSON output
│   │   │   ├── markdown_formatter.py # Markdown output
│   │   │   └── schemas.py         # Pydantic models
│   │   ├── api/
│   │   │   ├── __init__.py
│   │   │   ├── main.py            # FastAPI app (Phase 3)
│   │   │   └── routes.py          # API endpoints
│   │   └── cli/
│   │       ├── __init__.py
│   │       └── main.py            # CLI interface
├── tests/
│   ├── unit/
│   ├── integration/
│   └── fixtures/                   # Test documents
├── data/                           # Sample documents
├── docs/                           # Documentation
├── notebooks/                      # Jupyter notebooks (nbs/)
├── scripts/                        # Utility scripts
├── pyproject.toml
├── README.md
├── .env.example
└── .gitignore
```

---

## 🚀 Implementation Roadmap

### Phase 1: Foundation & Core Extraction (Week 1-2)
**Goal:** Basic document reading and extraction capabilities

#### Deliverables:
1. **Project Setup**
   - [ ] Finalize project structure
   - [ ] Set up development environment
   - [ ] Configure dependencies in pyproject.toml
   - [ ] Set up testing framework

2. **Basic Document Readers**
   - [ ] Implement PDF reader (PyMuPDF)
   - [ ] Implement DOCX reader
   - [ ] Implement image reader with basic OCR
   - [ ] Create reader factory pattern
   - [ ] Unit tests for each reader

3. **OCR Integration**
   - [ ] Set up PaddleOCR
   - [ ] Set up Tesseract as fallback
   - [ ] Implement basic layout analysis
   - [ ] Test on sample documents

4. **Basic Output Formatters**
   - [ ] JSON formatter with basic structure
   - [ ] Markdown formatter with basic structure
   - [ ] Pydantic schemas for validation

**Success Criteria:**
- Can extract text from PDF, DOCX, and images
- Basic OCR working on printed text
- Output in JSON and Markdown formats

---

### Phase 2: AI Intelligence Layer (Week 3-4)
**Goal:** Implement intelligent extraction using LLMs and agents

#### Deliverables:
1. **LangGraph Agent Setup**
   - [ ] Design agent workflow graph
   - [ ] Implement state management
   - [ ] Set up Ollama integration
   - [ ] Create agent communication protocol

2. **Extraction Agents**
   - [ ] Schema Detection Agent (identify document type)
   - [ ] Content Extraction Agent (extract key-value pairs)
   - [ ] Table Parser Agent (handle complex tables)
   - [ ] Validation Agent (quality checks)

3. **Enhanced Processing**
   - [ ] Implement table extraction (camelot/pdfplumber)
   - [ ] Document structure analysis
   - [ ] Entity recognition and classification
   - [ ] Multi-page document handling

4. **Vision Model Integration**
   - [ ] Integrate llama3.2-vision for image understanding
   - [ ] Form understanding capabilities
   - [ ] Handwriting recognition (basic)

**Success Criteria:**
- LangGraph agents working in orchestrated workflow
- Can identify document types automatically
- Extract structured data from forms and tables
- Vision model can understand document layouts

---

### Phase 3: Production Features (Week 5-6)
**Goal:** Production-ready system with API and advanced features

#### Deliverables:
1. **REST API**
   - [ ] FastAPI application setup
   - [ ] Upload endpoint (single & batch)
   - [ ] Extraction endpoints with format selection
   - [ ] Status/health endpoints
   - [ ] API documentation (OpenAPI)

2. **CLI Tool**
   - [ ] Rich CLI with typer
   - [ ] Single file processing command
   - [ ] Batch processing command
   - [ ] Configuration management
   - [ ] Progress indicators

3. **Advanced Features**
   - [ ] Batch processing pipeline
   - [ ] Caching mechanism
   - [ ] Error recovery and retry logic
   - [ ] Confidence scoring for extractions
   - [ ] Multi-language support

4. **Quality & Testing**
   - [ ] Comprehensive unit tests (80%+ coverage)
   - [ ] Integration tests
   - [ ] Performance benchmarking
   - [ ] Error handling improvements
   - [ ] Logging and monitoring

**Success Criteria:**
- Working REST API with documentation
- CLI tool for easy usage
- Batch processing capabilities
- 80%+ test coverage

---

### Phase 4: Optimization & Enhancement (Week 7-8)
**Goal:** Performance optimization and advanced features

#### Deliverables:
1. **Performance Optimization**
   - [ ] Implement async processing
   - [ ] Parallel document processing
   - [ ] Caching strategy for repeated extractions
   - [ ] Model optimization (quantization if needed)

2. **Advanced Extraction**
   - [ ] Custom schema support (user-defined templates)
   - [ ] Semantic search within documents
   - [ ] Cross-document reference resolution
   - [ ] Named Entity Recognition (NER)

3. **Additional Format Support**
   - [ ] Email (EML, MSG) parsing
   - [ ] HTML/Web page extraction
   - [ ] PowerPoint (PPTX) support
   - [ ] Scanned document optimization

4. **Documentation & Deployment**
   - [ ] Comprehensive documentation
   - [ ] Usage examples and tutorials
   - [ ] Docker containerization
   - [ ] Deployment guide

**Success Criteria:**
- < 5s processing for standard documents
- Support for 7+ document formats
- Production-ready deployment artifacts
- Complete documentation

---

## 📊 Key Features Breakdown

### Document Type Support (Priority Order)
1. ✅ **PDF** - Text-based and scanned
2. ✅ **Images** - PNG, JPG, TIFF (via OCR)
3. ✅ **DOCX** - Microsoft Word documents
4. ⭐ **Excel/CSV** - Spreadsheets
5. ⭐ **Forms** - Structured forms with fields
6. ⭐ **Tables** - Complex table extraction
7. 🔄 **PPTX** - PowerPoint presentations
8. 🔄 **HTML** - Web pages
9. 🔄 **Email** - EML, MSG formats

### Extraction Capabilities
- **Text Extraction**: Raw text with formatting preservation
- **Structure Recognition**: Headers, paragraphs, lists, sections
- **Table Extraction**: Complex multi-cell tables with relationships
- **Form Field Extraction**: Key-value pairs from forms
- **Entity Recognition**: Dates, amounts, names, addresses
- **Metadata Extraction**: Author, creation date, title, etc.
- **Image/Chart Description**: Using vision models

### Output Formats
1. **JSON**
   - Structured schema-based output
   - Nested relationships preserved
   - Type validation with Pydantic
   - Confidence scores per field

2. **Markdown**
   - Human-readable format
   - Preserved document structure
   - Tables in markdown format
   - Metadata header section

---

## 🧪 Testing Strategy

### Test Coverage
- **Unit Tests**: Individual components (readers, formatters, agents)
- **Integration Tests**: End-to-end workflows
- **Performance Tests**: Processing speed benchmarks
- **Accuracy Tests**: Extraction quality metrics

### Test Documents
- Create diverse test dataset:
  - Clean PDFs (born-digital)
  - Scanned documents (various DPI)
  - Forms with tables
  - Multi-page documents
  - Handwritten notes (basic)
  - Different languages

---

## 📈 Success Metrics & KPIs

### Technical Metrics
- **Accuracy**: 95%+ on typed documents, 85%+ on scanned
- **Performance**: < 5s for standard docs, < 15s for complex
- **Coverage**: 80%+ test coverage
- **Reliability**: 99%+ uptime for API

### User Experience Metrics
- **Easy Integration**: < 10 lines of code to use
- **Clear Output**: Well-structured JSON/Markdown
- **Error Handling**: Informative error messages
- **Documentation**: Comprehensive with examples

---

## 🔐 Security & Privacy Considerations

### Data Privacy
- Process documents locally (no cloud upload by default)
- Option for cloud processing with explicit consent
- No data retention after processing
- Secure API endpoints with authentication (Phase 3)

### Security Measures
- Input validation and sanitization
- File type verification
- Resource limits (file size, processing time)
- Error handling without info leakage

---

## 🌟 Competitive Advantages

### vs. Landing.AI
- **Open Source**: Full transparency and customization
- **Local Processing**: Privacy-first approach
- **Multi-Model**: Mix local and cloud models
- **Extensible**: Easy to add new formats and extractors

### vs. Traditional OCR
- **AI Understanding**: Context-aware extraction
- **Structure Preservation**: Not just text, but meaning
- **Format Flexibility**: Multiple output formats
- **Accuracy**: LLM-powered validation and correction

---

## 💰 Resource Requirements

### Development Resources
- **Developer Time**: 6-8 weeks (single developer)
- **Compute**: Local GPU recommended (for vision models)
- **Storage**: ~5GB for models (local Ollama models)

### Runtime Resources
- **RAM**: 8GB minimum, 16GB recommended
- **GPU**: Optional but recommended (NVIDIA with CUDA)
- **Storage**: Depends on caching strategy

---

## 🎓 Learning & Documentation

### Documentation Deliverables
1. **README**: Quick start and overview
2. **API Documentation**: Complete API reference
3. **User Guide**: Step-by-step usage examples
4. **Architecture Doc**: System design details
5. **Contributing Guide**: For open-source contributors

### Example Use Cases
1. Invoice processing and data extraction
2. Resume parsing for HR systems
3. Legal document analysis
4. Scientific paper data extraction
5. Form digitization

---

## 🔄 Future Enhancements (Post-MVP)

### Advanced Features
- **Web UI**: Browser-based interface
- **Streaming Processing**: Real-time extraction for large docs
- **Custom Training**: Fine-tune models on specific document types
- **Workflow Templates**: Pre-built extraction templates
- **Multi-Document Analysis**: Cross-document intelligence
- **API Marketplace**: Pre-built extractors for common docs

### Integration Possibilities
- Zapier/Make.com integration
- Cloud storage connectors (S3, GDrive, Dropbox)
- Database export (PostgreSQL, MongoDB)
- Webhook notifications
- Slack/Teams bot integration

---

## ✅ Definition of Done

### Phase 1 Complete
- ✅ Basic extraction working for PDF, DOCX, images
- ✅ OCR functional with PaddleOCR
- ✅ JSON and Markdown output working
- ✅ Unit tests passing

### Phase 2 Complete
- ✅ LangGraph agents orchestrating extraction
- ✅ Document type auto-detection
- ✅ Table extraction working
- ✅ Vision model integrated

### Phase 3 Complete
- ✅ REST API deployed and documented
- ✅ CLI tool functional
- ✅ Batch processing working
- ✅ 80%+ test coverage

### Phase 4 Complete
- ✅ Performance optimized
- ✅ 7+ formats supported
- ✅ Complete documentation
- ✅ Production-ready deployment

---

## 🤝 Next Steps (Pending Approval)

1. **Review & Approve** this project plan
2. **Prioritize Features** if timeline needs adjustment
3. **Set Up Development Environment**
4. **Begin Phase 1 Implementation**

---

## 📝 Notes & Assumptions

### Assumptions
- Access to local GPU for optimal performance (optional)
- Ollama models can be downloaded locally
- Internet access for initial setup and dependencies
- Python 3.12+ environment available

### Constraints
- Focus on accuracy over speed initially
- Start with English language support
- Local-first approach (cloud optional)

### Dependencies
- Already in pyproject.toml: langchain, langgraph, pymupdf, pillow
- To be added: paddleocr, python-docx, camelot-py, fastapi, typer, pydantic

---

**Document Version**: 1.0  
**Last Updated**: October 18, 2025  
**Status**: ⏳ Awaiting Approval


