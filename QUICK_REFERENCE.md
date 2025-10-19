# Agent-Extract Quick Reference

> One-page cheat sheet for common tasks

## ⚡ Installation
```bash
git clone https://github.com/g-sree-jith/agent-extract.git
cd agent-extract
uv sync              # Install with uv (recommended)
# OR
pip install -e .     # Install with pip
```

## CLI Commands

### Extract Single Document
```bash
# Standard extraction (Phase 1 - Fast ~1s)
agent-extract extract document.pdf                              # Print to console
agent-extract extract document.pdf -o result.json               # Save as JSON
agent-extract extract document.pdf -f markdown -o result.md     # Save as Markdown

# AI-Powered extraction (Phase 2 - Smart) 🤖

# Gemini AI (Default - Fast, Accurate) ⚡
agent-extract extract document.pdf --ai -o result.json          # Uses Gemini
agent-extract extract document.pdf --ai --provider gemini       # Explicit

# Other Cloud Providers
agent-extract extract document.pdf --ai --provider openai       # OpenAI GPT
agent-extract extract document.pdf --ai --provider groq         # Groq (fastest!)

# Local (if you have Ollama)
agent-extract extract document.pdf --ai --provider ollama       # Local qwen3

# Custom model
agent-extract extract doc.pdf --ai -p ollama -m qwen3:0.6b      # Specific model
```

### Batch Processing
```bash
agent-extract batch ./input ./output                    # Process all files
agent-extract batch ./input ./output --pattern "*.pdf"  # Only PDFs
agent-extract batch ./input ./output -f markdown        # Output as Markdown
```

### Information
```bash
agent-extract info       # Show supported formats
agent-extract version    # Show version
```

## Python API

### Basic Extraction
```python
from pathlib import Path
from agent_extract.readers.factory import ReaderFactory
from agent_extract.ocr.ocr_manager import OCRManager

ocr = OCRManager.from_config()
factory = ReaderFactory(ocr_engine=ocr)

result = factory.get_reader(Path("doc.pdf")).read(Path("doc.pdf"))
print(result.raw_text)
```

### Format Output
```python
from agent_extract.outputs.json_formatter import JSONFormatter
from agent_extract.outputs.markdown_formatter import MarkdownFormatter

# JSON
json_fmt = JSONFormatter()
json_str = json_fmt.format(result)
json_fmt.format_to_file(result, Path("output.json"))

# Markdown
md_fmt = MarkdownFormatter()
md_str = md_fmt.format(result)
md_fmt.format_to_file(result, Path("output.md"))
```

### Access Extracted Data
```python
# Metadata
print(f"Type: {result.metadata.document_type}")
print(f"Pages: {result.metadata.page_count}")
print(f"Size: {result.metadata.file_size}")

# Content
print(result.raw_text)

# Tables
for table in result.tables:
    print(f"Headers: {table.headers}")
    for row in table.rows:
        print(row)

# Structured data
print(result.structured_data)
```

## Supported Formats

| Format | Extensions | Reader |
|--------|-----------|---------|
| PDF | `.pdf` | PDFReader |
| Word | `.docx` | DOCXReader |
| Images | `.png`, `.jpg`, `.jpeg`, `.tiff` | ImageReader |

## Configuration (.env)

Create `.env` file in project root:

```env
# Gemini API (Required for AI extraction)
GEMINI_API_KEY=your_gemini_api_key_here

# LLM Settings
LLM_PROVIDER=gemini
LLM_MODEL=gemini-pro
LLM_VISION_MODEL=gemini-pro

# OCR
OCR_ENGINE=tesseract
OCR_LANGUAGE=eng

# Processing
MAX_FILE_SIZE_MB=50
DEFAULT_OUTPUT_FORMAT=json
```

## Common Patterns

### Invoice Processing
```bash
agent-extract extract invoice.pdf -o invoice_data.json
```

### Batch OCR
```bash
agent-extract batch ./scanned ./text --pattern "*.png"
```

### Extract Tables
```python
result = reader.read(Path("report.pdf"))
for i, table in enumerate(result.tables):
    print(f"Table {i+1}: {len(table.rows)} rows")
```

## Troubleshooting

### OCR Issues
```bash
# Install PaddleOCR
pip install paddleocr paddlepaddle

# Or use Tesseract
echo "OCR_ENGINE=tesseract" > .env
```

### Import Errors
```bash
pip install -e .
```

### File Too Large
```env
# In .env file
MAX_FILE_SIZE_MB=100
```

## Getting Help
```bash
agent-extract --help              # CLI help
agent-extract extract --help      # Command help
```

## Testing
```bash
pytest                            # Run all tests
pytest -v                         # Verbose
pytest --cov=src/agent_extract    # With coverage
```

## Resources
- 📖 **Main docs**: [README.md](README.md)
- 🚀 **Quick start**: [docs/GETTING_STARTED.md](docs/GETTING_STARTED.md)
- 🤖 **Local models**: [docs/LOCAL_MODELS.md](docs/LOCAL_MODELS.md)
- 📋 **Roadmap**: [PROJECT_PLAN.md](PROJECT_PLAN.md)
- 📝 **Changelog**: [CHANGELOG.md](CHANGELOG.md)
- 🤝 **Contributing**: [CONTRIBUTING.md](CONTRIBUTING.md)


