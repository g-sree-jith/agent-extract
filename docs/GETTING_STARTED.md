# Getting Started with Agent-Extract

## Quick Installation (5 minutes)

### Step 1: Clone or Download

```bash
cd agent-extract
```

### Step 2: Install Dependencies

**Option A: Using uv (recommended)**
```bash
uv sync
```

**Option B: Using pip**
```bash
pip install -e .
```

**Option C: Using setup script**
```bash
python scripts/setup.py
```

### Step 3: Verify Installation

```bash
# Check version
agent-extract version

# Show supported formats
agent-extract info
```

## Your First Extraction

### 1. Prepare a Document

Place any of these documents in your `data/` folder:
- PDF file (e.g., `invoice.pdf`)
- Word document (e.g., `report.docx`)
- Image file (e.g., `receipt.png`)

### 2. Extract Data

```bash
# Extract from PDF
agent-extract data/invoice.pdf

# Save as JSON
agent-extract data/invoice.pdf --output result.json

# Save as Markdown
agent-extract data/invoice.pdf --format markdown --output result.md
```

### 3. View Results

The extraction will show:
- Document metadata (pages, size, type)
- Extracted text content
- Tables (if any)
- Processing time

## Python API Example

Create a file `test_extraction.py`:

```python
from pathlib import Path
from agent_extract.readers.factory import ReaderFactory
from agent_extract.ocr.ocr_manager import OCRManager

# Initialize
ocr_engine = OCRManager.from_config()
factory = ReaderFactory(ocr_engine=ocr_engine)

# Extract
result = factory.get_reader(Path("data/document.pdf")).read(Path("data/document.pdf"))

# Show results
print(f"📄 Document: {result.metadata.filename}")
print(f"📊 Pages: {result.metadata.page_count}")
print(f"📝 Text length: {len(result.raw_text)} characters")
print(f"📋 Tables: {len(result.tables)}")
print(f"⏱️  Time: {result.processing_time:.2f}s")
```

Run it:
```bash
python test_extraction.py
```

## Common Use Cases

### Invoice Processing

```bash
agent-extract invoice.pdf --format json --output invoice_data.json
```

### Batch Document Processing

```bash
agent-extract batch ./invoices ./output --pattern "*.pdf"
```

### Scanned Document OCR

```bash
agent-extract scanned_page.png --output extracted_text.json
```

## Troubleshooting

### Issue: OCR not working

**Solution 1:** Install PaddleOCR dependencies
```bash
pip install paddleocr paddlepaddle
```

**Solution 2:** Use Tesseract as fallback
```bash
# Install Tesseract
# Windows: choco install tesseract
# macOS: brew install tesseract
# Linux: sudo apt-get install tesseract-ocr

# Set in .env
echo "OCR_ENGINE=tesseract" > .env
```

### Issue: Import errors

```bash
# Reinstall in editable mode
pip install -e .
```

### Issue: File too large

Create `.env` file:
```env
MAX_FILE_SIZE_MB=100
```

## What's Next?

1. **Read the [Usage Guide](../USAGE_GUIDE.md)** for detailed API documentation
2. **Check the [Project Plan](../PROJECT_PLAN.md)** for upcoming features
3. **Run the tests** to ensure everything works:
   ```bash
   pytest
   ```
4. **Try advanced features** like table extraction and batch processing

## Need Help?

- 📖 Read the full [README](../README.md)
- 🔧 Check [Usage Guide](../USAGE_GUIDE.md)
- 🐛 Report issues on GitHub
- 💬 Join discussions

---

**Ready to extract some documents? Let's go! 🚀**


