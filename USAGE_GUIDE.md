# Agent-Extract Usage Guide

## Installation

### Prerequisites

- Python 3.12 or higher
- (Optional) Tesseract OCR for fallback OCR engine
- (Optional) Ollama for AI features (Phase 2+)

### Install Agent-Extract

```bash
# Using uv (recommended)
uv sync

# Using pip
pip install -e .

# With development dependencies
pip install -e ".[dev]"

# With API support (Phase 3)
pip install -e ".[api]"

# Install everything
pip install -e ".[all]"
```

### Install OCR Dependencies

PaddleOCR will be installed automatically, but you may need to install Tesseract separately:

**Windows:**
```bash
# Download installer from: https://github.com/UB-Mannheim/tesseract/wiki
# Or use chocolatey:
choco install tesseract
```

**macOS:**
```bash
brew install tesseract
```

**Linux:**
```bash
sudo apt-get install tesseract-ocr
```

## CLI Usage

### Basic Commands

#### 1. Extract from a Single Document

```bash
# Extract and print to console (JSON format by default)
agent-extract document.pdf

# Save to file
agent-extract document.pdf --output result.json

# Use Markdown format
agent-extract document.pdf --format markdown --output result.md

# Short form
agent-extract document.pdf -f md -o result.md
```

#### 2. Batch Processing

Process multiple documents at once:

```bash
# Process all files in a directory
agent-extract batch ./input ./output

# Process only PDFs
agent-extract batch ./input ./output --pattern "*.pdf"

# Output as Markdown
agent-extract batch ./input ./output --format markdown
```

#### 3. Get Information

```bash
# Show supported formats and configuration
agent-extract info

# Show version
agent-extract version
```

### Advanced Options

#### Disable OCR

For PDFs with embedded text, you can disable OCR to speed up processing:

```bash
agent-extract document.pdf --no-ocr
```

## Python API Usage

### Basic Extraction

```python
from pathlib import Path
from agent_extract.readers.factory import ReaderFactory
from agent_extract.ocr.ocr_manager import OCRManager

# Initialize
ocr_engine = OCRManager.from_config()
factory = ReaderFactory(ocr_engine=ocr_engine)

# Extract
document_path = Path("document.pdf")
reader = factory.get_reader(document_path)
result = reader.read(document_path)

# Access extracted data
print(f"Document: {result.metadata.filename}")
print(f"Pages: {result.metadata.page_count}")
print(f"Text length: {len(result.raw_text)}")
print(f"Tables found: {len(result.tables)}")
```

### Working with Different Formats

#### PDF Documents

```python
from agent_extract.readers.pdf_reader import PDFReader

reader = PDFReader()
result = reader.read(Path("document.pdf"))

# Access text
print(result.raw_text)

# Access tables
for i, table in enumerate(result.tables):
    print(f"Table {i + 1}:")
    print(f"  Headers: {table.headers}")
    print(f"  Rows: {len(table.rows)}")
```

#### DOCX Documents

```python
from agent_extract.readers.docx_reader import DOCXReader

reader = DOCXReader()
result = reader.read(Path("document.docx"))

# Access content
print(result.raw_text)
print(f"Tables: {len(result.tables)}")
```

#### Images with OCR

```python
from agent_extract.readers.image_reader import ImageReader
from agent_extract.ocr.ocr_manager import OCRManager

# Initialize OCR
ocr_engine = OCRManager(primary_engine="paddle", lang="en")

# Read image
reader = ImageReader(ocr_engine=ocr_engine)
result = reader.read(Path("scanned_document.png"))

print(result.raw_text)
```

### Output Formatting

#### JSON Output

```python
from agent_extract.outputs.json_formatter import JSONFormatter

formatter = JSONFormatter()

# Get JSON string
json_str = formatter.format(result)
print(json_str)

# Save to file
formatter.format_to_file(result, Path("output.json"))

# Compact format (no indentation)
compact_json = formatter.format_compact(result)

# Pretty format (sorted keys)
pretty_json = formatter.format_pretty(result)
```

#### Markdown Output

```python
from agent_extract.outputs.markdown_formatter import MarkdownFormatter

formatter = MarkdownFormatter()

# Get Markdown string
markdown_str = formatter.format(result)
print(markdown_str)

# Save to file
formatter.format_to_file(result, Path("output.md"))

# Without metadata section
formatter = MarkdownFormatter(include_metadata=False)
markdown_str = formatter.format(result)
```

### Custom Configuration

```python
from agent_extract.core.config import Config

# Create custom configuration
config = Config(
    debug=True,
    max_file_size_mb=100,
    ocr_engine="tesseract",
    ocr_language="en",
    enable_cache=True,
)

# Use configuration
print(f"Max file size: {config.max_file_size_bytes} bytes")
```

### OCR Engine Selection

```python
from agent_extract.ocr.ocr_manager import OCRManager

# Use PaddleOCR (default)
ocr = OCRManager(primary_engine="paddle", lang="en")
text = ocr.extract_text(Path("image.png"))

# Use Tesseract
ocr = OCRManager(primary_engine="tesseract", lang="eng")
text = ocr.extract_text(Path("image.png"))

# With bounding boxes
boxes = ocr.extract_with_boxes(Path("image.png"))
for text, confidence, (x, y, w, h) in boxes:
    print(f"{text} (confidence: {confidence:.2%})")
```

## Working with Extraction Results

### Accessing Metadata

```python
result = reader.read(document_path)

# Document metadata
metadata = result.metadata
print(f"Filename: {metadata.filename}")
print(f"Type: {metadata.document_type}")
print(f"Size: {metadata.file_size} bytes")
print(f"Pages: {metadata.page_count}")
print(f"Author: {metadata.author}")
print(f"Title: {metadata.title}")
```

### Processing Tables

```python
# Iterate through tables
for i, table in enumerate(result.tables):
    print(f"\nTable {i + 1} (Page {table.page or 'N/A'}):")
    print(f"Headers: {table.headers}")
    
    # Process rows
    for row in table.rows:
        print(row)
    
    # Convert to pandas DataFrame (requires pandas)
    import pandas as pd
    df = pd.DataFrame(table.rows, columns=table.headers)
    print(df)
```

### Structured Data

```python
# Access structured data
structured = result.structured_data

# For images, includes image properties
if "image_width" in structured:
    print(f"Image size: {structured['image_width']}x{structured['image_height']}")
```

## Configuration File

Create a `.env` file in your project root:

```env
# Application Settings
DEBUG=false
APP_NAME=agent-extract

# Document Processing
MAX_FILE_SIZE_MB=50
DEFAULT_OUTPUT_FORMAT=json

# OCR Settings
OCR_ENGINE=paddle
OCR_LANGUAGE=en
OCR_CONFIDENCE_THRESHOLD=0.5

# LLM Settings (Phase 2+)
LLM_MODEL=llama3.1
LLM_VISION_MODEL=llama3.2-vision
LLM_BASE_URL=http://localhost:11434
LLM_TEMPERATURE=0.1
LLM_MAX_TOKENS=4096

# Processing Features
ENABLE_TABLE_EXTRACTION=true
ENABLE_ENTITY_EXTRACTION=true
ENABLE_VISION_MODEL=true
PARALLEL_PROCESSING=false

# Cache Settings
ENABLE_CACHE=true
CACHE_TTL_SECONDS=3600

# Paths
DATA_DIR=data
CACHE_DIR=.cache
MODELS_DIR=models
```

## Examples

### Example 1: PDF Invoice Processing

```python
from pathlib import Path
from agent_extract.readers.pdf_reader import PDFReader
from agent_extract.outputs.json_formatter import JSONFormatter

# Read invoice
reader = PDFReader()
result = reader.read(Path("invoice.pdf"))

# Extract tables (invoice items)
for table in result.tables:
    print("Invoice Items:")
    for row in table.rows:
        print(f"  {row}")

# Save as JSON
formatter = JSONFormatter()
formatter.format_to_file(result, Path("invoice_data.json"))
```

### Example 2: Batch Image OCR

```python
from pathlib import Path
from agent_extract.readers.factory import ReaderFactory
from agent_extract.ocr.ocr_manager import OCRManager

# Initialize
ocr_engine = OCRManager.from_config()
factory = ReaderFactory(ocr_engine=ocr_engine)

# Process all images in a directory
image_dir = Path("scanned_documents")
output_dir = Path("extracted_text")
output_dir.mkdir(exist_ok=True)

for image_path in image_dir.glob("*.png"):
    print(f"Processing {image_path.name}...")
    
    reader = factory.get_reader(image_path)
    result = reader.read(image_path)
    
    # Save extracted text
    output_file = output_dir / f"{image_path.stem}.txt"
    output_file.write_text(result.raw_text)
```

### Example 3: Document Comparison

```python
from pathlib import Path
from agent_extract.readers.factory import ReaderFactory

factory = ReaderFactory()

# Extract from two versions
doc1 = factory.get_reader(Path("document_v1.pdf")).read(Path("document_v1.pdf"))
doc2 = factory.get_reader(Path("document_v2.pdf")).read(Path("document_v2.pdf"))

# Compare text
if doc1.raw_text == doc2.raw_text:
    print("Documents have identical text")
else:
    print("Documents differ")
    
# Compare metadata
print(f"Doc1 pages: {doc1.metadata.page_count}")
print(f"Doc2 pages: {doc2.metadata.page_count}")
```

## Troubleshooting

### OCR Issues

**Problem:** PaddleOCR not working
```bash
# Try installing specific version
pip install paddleocr==2.7.0 paddlepaddle==2.6.0

# Or use Tesseract as fallback
export OCR_ENGINE=tesseract
```

**Problem:** Low OCR accuracy
```python
# Increase image quality before processing
from PIL import Image

img = Image.open("document.png")
# Resize to higher resolution
img = img.resize((img.width * 2, img.height * 2), Image.LANCZOS)
img.save("document_hires.png")
```

### File Size Issues

**Problem:** File too large
```python
# Increase max file size
from agent_extract.core.config import Config

config = Config(max_file_size_mb=100)
```

### Import Errors

**Problem:** Module not found
```bash
# Ensure package is installed in editable mode
pip install -e .

# Or add to PYTHONPATH
export PYTHONPATH="${PYTHONPATH}:${PWD}/src"
```

## Next Steps

- Check out the [Project Plan](PROJECT_PLAN.md) for upcoming features
- Explore [Phase 2 features](PROJECT_PLAN.md#phase-2-ai-intelligence-layer-week-3-4) for AI-powered extraction
- Join our community for support and discussions

---

For more information, visit the [documentation](docs/) or open an issue on GitHub.


