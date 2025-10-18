# Using Local Models with Agent-Extract

## 🎯 Recommended Local Models

Agent-Extract is optimized to work with lightweight local models via Ollama.

### Your Current Models

Based on your setup, you have:

| Model | Size | Capability | Use Case |
|-------|------|------------|----------|
| **qwen3:0.6b** | 522 MB | Tool calling, Fast inference | Primary LLM for document understanding |
| **gemma3:4b** | 3.3 GB | Vision, Multimodal | Vision-based extraction from images |

## 🚀 Quick Setup

### 1. Verify Ollama is Running

```bash
# Check if Ollama is running
curl http://localhost:11434/api/tags

# Start Ollama if needed
ollama serve
```

### 2. Configure Agent-Extract

The default configuration already uses your models:

```python
# In src/agent_extract/core/config.py
llm_model = "qwen3:0.6b"          # Fast, tool calling
llm_vision_model = "gemma3:4b"     # Vision understanding
```

Or set via environment variables:

```bash
# .env file
LLM_MODEL=qwen3:0.6b
LLM_VISION_MODEL=gemma3:4b
```

## 💡 Model Capabilities

### Qwen3:0.6b - Primary LLM
- ✅ **Tool Calling**: Can use functions and tools
- ✅ **Fast**: Only 522 MB, quick inference
- ✅ **Efficient**: Low memory usage
- ✅ **Use For**:
  - Document type detection
  - Schema extraction
  - Entity recognition
  - Text analysis

### Gemma3:4b - Vision Model
- ✅ **Vision**: Can process images
- ✅ **Multimodal**: Text + images
- ✅ **Moderate Size**: 3.3 GB
- ✅ **Use For**:
  - Scanned document understanding
  - Form field detection
  - Image-based extraction
  - Layout analysis

## 🔧 Testing Your Models

```bash
# Test qwen3
ollama run qwen3:0.6b "Extract key information from this text: Invoice #12345 dated 2025-01-15"

# Test gemma3
ollama run gemma3:4b "Describe this image"
```

## 📊 Phase 2: How Models Will Be Used

### Document Understanding Pipeline

```
1. Load Document
   ↓
2. OCR (PaddleOCR/Tesseract)  ← Current Phase 1
   ↓
3. qwen3:0.6b                  ← Phase 2
   - Detect document type
   - Extract schema
   - Identify entities
   ↓
4. gemma3:4b (if image/scan)   ← Phase 2
   - Visual understanding
   - Layout analysis
   - Form field detection
   ↓
5. Structured Output (JSON/Markdown)
```

## 🎯 Advantages of Local Models

### Privacy
- ✅ All processing happens locally
- ✅ No data sent to cloud services
- ✅ GDPR/compliance friendly

### Cost
- ✅ No API fees
- ✅ Unlimited usage
- ✅ One-time download

### Speed
- ✅ No network latency
- ✅ Fast inference (especially qwen3:0.6b)
- ✅ Batch processing efficient

### Control
- ✅ Model version control
- ✅ Customize parameters
- ✅ Fine-tune if needed

## 🔄 Alternative Models

If you want to try other models:

### Faster/Smaller
```bash
# Even smaller models
ollama pull qwen:0.5b          # 395 MB
ollama pull phi3:mini          # 2.3 GB
```

### More Capable
```bash
# Larger models (if you have VRAM)
ollama pull qwen2.5:7b         # 4.7 GB
ollama pull llama3.2-vision:11b # 7.9 GB
```

### Specialized
```bash
# Document-specific models
ollama pull mistral:7b         # Good for structured extraction
ollama pull codellama:7b       # Good for code/structured data
```

## ⚙️ Configuration Tips

### Memory Management

```python
# .env configuration
LLM_MAX_TOKENS=2048        # Reduce for faster inference
LLM_TEMPERATURE=0.1        # Lower for consistent extraction
ENABLE_CACHE=true          # Cache LLM responses
```

### Batch Processing

```python
# For batch processing, consider:
PARALLEL_PROCESSING=false   # Sequential for low memory
# OR
PARALLEL_PROCESSING=true    # Parallel if you have 16GB+ RAM
```

## 🧪 Benchmarks (Estimated)

| Operation | qwen3:0.6b | gemma3:4b |
|-----------|------------|-----------|
| Document Classification | ~100ms | ~300ms |
| Entity Extraction | ~200ms | ~500ms |
| Schema Detection | ~150ms | ~400ms |
| Vision Understanding | N/A | ~800ms |

*Times on typical CPU, will be faster with GPU*

## 🚀 Phase 2 Preview

When we implement Phase 2, you'll be able to:

```python
from agent_extract import DocumentIntelligence

# Initialize with your local models (automatically detected)
intel = DocumentIntelligence()

# Smart extraction with AI understanding
result = intel.extract("invoice.pdf", 
    schema="invoice",  # Detected automatically
    use_vision=True    # For scanned docs
)

# Structured output
print(result.invoice_number)  # "INV-12345"
print(result.total_amount)    # 1234.56
print(result.line_items)      # [...]
```

## 💬 Need Different Models?

The architecture is flexible! Just update config:

```python
# config.py or .env
LLM_MODEL=your-preferred-model
LLM_VISION_MODEL=your-vision-model
```

---

**Your current setup with qwen3:0.6b and gemma3:4b is excellent for:**
- ✅ Fast local processing
- ✅ Low memory usage
- ✅ Tool calling support
- ✅ Vision capabilities
- ✅ Privacy-first approach

Perfect for document intelligence! 🎉

