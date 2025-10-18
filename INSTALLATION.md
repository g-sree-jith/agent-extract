# Installation Instructions

## Prerequisites

- Python 3.12 or higher
- pip or uv package manager

## Quick Install (Recommended)

### Option 1: Using uv (Fastest)

```bash
# Install uv if you don't have it
pip install uv

# Sync all dependencies
uv sync
```

### Option 2: Using pip

```bash
# Install core dependencies
pip install -e .

# Or install with dev tools
pip install -e ".[dev]"
```

## Step-by-Step Installation

### 1. Verify Python Version

```bash
python --version
# Should show Python 3.12.x or higher
```

### 2. Create Virtual Environment (Optional but Recommended)

```bash
# Create venv
python -m venv venv

# Activate on Windows
.\venv\Scripts\activate

# Activate on macOS/Linux
source venv/bin/activate
```

### 3. Install Dependencies

```bash
# Navigate to project directory
cd agent-extract

# Install package
pip install -e .
```

This will install all required dependencies including:
- Document parsers (pymupdf, pdfplumber, python-docx)
- OCR engines (paddleocr, pytesseract)
- CLI tools (typer, rich)
- LLM frameworks (langchain, langgraph)
- And more...

### 4. Verify Installation

```bash
# Check if CLI works
python -m agent_extract.cli.main --help

# Or if installed as script
agent-extract --help
```

## OCR Dependencies

### PaddleOCR (Primary OCR Engine)

PaddleOCR will be installed automatically with the package. For GPU support:

```bash
# Install with GPU support (CUDA)
pip install paddlepaddle-gpu
```

### Tesseract (Fallback OCR Engine)

**Windows:**
```bash
# Using Chocolatey
choco install tesseract

# Or download from: https://github.com/UB-Mannheim/tesseract/wiki
```

**macOS:**
```bash
brew install tesseract
```

**Linux (Ubuntu/Debian):**
```bash
sudo apt-get update
sudo apt-get install tesseract-ocr
```

## Optional Dependencies

### Development Tools

```bash
pip install -e ".[dev]"
```

Includes:
- pytest (testing)
- black (formatting)
- ruff (linting)
- mypy (type checking)

### API Support (Phase 3)

```bash
pip install -e ".[api]"
```

Includes:
- fastapi
- uvicorn

### All Dependencies

```bash
pip install -e ".[all]"
```

## Troubleshooting

### Issue: `ModuleNotFoundError`

```bash
# Ensure you're in the project directory
cd agent-extract

# Reinstall in editable mode
pip install -e .
```

### Issue: PaddleOCR fails to install

```bash
# Install separately
pip install paddleocr paddlepaddle
```

### Issue: Camelot-py installation fails

```bash
# Install system dependencies first (Linux)
sudo apt-get install python3-tk ghostscript

# Then retry
pip install camelot-py[cv]
```

### Issue: Dependency conflicts

```bash
# Use fresh virtual environment
python -m venv fresh_venv
source fresh_venv/bin/activate  # or .\fresh_venv\Scripts\activate on Windows
pip install -e .
```

## Verify Installation

Run this to verify everything is working:

```python
# test_install.py
from pathlib import Path
from agent_extract.readers.factory import ReaderFactory
from agent_extract.core.config import Config

# Check configuration
config = Config()
print(f"✅ Configuration loaded: {config.app_name} v{config.version}")

# Check reader factory
factory = ReaderFactory()
formats = factory.get_supported_formats()
print(f"✅ Supported formats: {list(formats.keys())}")

print("\n🎉 Installation successful!")
```

```bash
python test_install.py
```

## Next Steps

After installation:

1. **Read the Quick Start**: See `QUICK_REFERENCE.md`
2. **Try the CLI**: `agent-extract --help`
3. **Run Tests**: `pytest` (if dev dependencies installed)
4. **Read Documentation**: `README.md` and `USAGE_GUIDE.md`

## Getting Help

If you encounter issues:
1. Check Python version (must be 3.12+)
2. Ensure you're in a virtual environment
3. Try reinstalling: `pip install -e . --force-reinstall`
4. Check the troubleshooting section above

---

**Ready to extract? Let's go! 🚀**


