# Agent-Extract Quick Reference Card

## Installation
```bash
uv sync              # Install with uv
pip install -e .     # Or with pip
```

## CLI Commands

### Extract Single Document
```bash
agent-extract document.pdf                              # Print to console
agent-extract document.pdf -o result.json               # Save as JSON
agent-extract document.pdf -f markdown -o result.md     # Save as Markdown
agent-extract image.png --no-ocr                        # Skip OCR
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

```env
# OCR
OCR_ENGINE=paddle
OCR_LANGUAGE=en

# Processing
MAX_FILE_SIZE_MB=50
DEFAULT_OUTPUT_FORMAT=json

# LLM (Phase 2)
LLM_MODEL=llama3.1
LLM_BASE_URL=http://localhost:11434
```

## Common Patterns

### Invoice Processing
```bash
agent-extract invoice.pdf -o invoice_data.json
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
- 📖 Full docs: `README.md`
- 🎓 Usage guide: `USAGE_GUIDE.md`
- 🚀 Quick start: `docs/GETTING_STARTED.md`
- 📋 Project plan: `PROJECT_PLAN.md`


