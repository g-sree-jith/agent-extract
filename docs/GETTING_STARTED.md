# Getting Started with Agent-Extract

> Get up and running in 5 minutes

## 🚀 Quick Start

### 1. Clone & Install (2 minutes)

```bash
# Clone the repository
git clone https://github.com/g-sree-jith/agent-extract.git
cd agent-extract

# Install dependencies
uv sync
```

### 2. Verify Installation (30 seconds)

```bash
# Check version
uv run agent-extract version

# Show supported formats
uv run agent-extract info
```

### 3. Extract Your First Document (1 minute)

```bash
# Extract from a PDF
uv run agent-extract extract your-document.pdf

# Save as JSON
uv run agent-extract extract your-document.pdf --output result.json

# Save as Markdown
uv run agent-extract extract your-document.pdf --format markdown --output result.md
```

## 🎯 What You Get

Agent-Extract will extract:
- ✅ Full text content from all pages
- ✅ Tables with headers and data
- ✅ Document metadata (pages, size, author)
- ✅ Structured output in JSON or Markdown

## 📝 Example Output

**Input**: Invoice PDF  
**Output**: 
```json
{
  "metadata": {
    "filename": "invoice.pdf",
    "document_type": "pdf",
    "page_count": 2
  },
  "raw_text": "Invoice #12345...",
  "tables": [
    {
      "headers": ["Item", "Price"],
      "rows": [["Product A", "$100"]]
    }
  ]
}
```

## 🐛 Common Issues

### Issue: `ModuleNotFoundError`
```bash
pip install -e .
```

### Issue: OCR not working
```bash
# PaddleOCR will auto-install
# For Tesseract: choco install tesseract (Windows)
```

### Issue: Command not found
```bash
# Use with uv run
uv run agent-extract extract document.pdf
```

## 📚 What's Next?

1. **Quick commands**: See [QUICK_REFERENCE.md](../QUICK_REFERENCE.md)
2. **Full documentation**: Read [README.md](../README.md)
3. **Local AI models**: Check [LOCAL_MODELS.md](LOCAL_MODELS.md)
4. **Project roadmap**: View [PROJECT_PLAN.md](../PROJECT_PLAN.md)

## 💡 Quick Tips

```bash
# Batch process all PDFs in a folder
uv run agent-extract batch ./documents ./output --pattern "*.pdf"

# Extract from images (with OCR)
uv run agent-extract extract scanned.png --output text.json

# Get help anytime
uv run agent-extract --help
uv run agent-extract extract --help
```

---

**That's it! You're ready to extract documents! 🎉**

For detailed usage, see the [Quick Reference](../QUICK_REFERENCE.md) or [README](../README.md).
