# Cloud LLM Providers Guide

> Use OpenAI, Gemini, Groq, or Anthropic for faster and more accurate extraction

## 🎯 Overview

Agent-Extract supports **both local and cloud LLM providers**:

| Provider | Speed | Accuracy | Cost | Privacy |
|----------|-------|----------|------|---------|
| **Ollama** (Local) | Medium | Good | Free | ✅ 100% |
| **Groq** | ⚡ Fastest | Excellent | Free tier | ⚠️ Cloud |
| **Gemini** | Fast | Excellent | Free tier | ⚠️ Cloud |
| **OpenAI** | Fast | Best | Paid | ⚠️ Cloud |
| **Anthropic** | Fast | Best | Paid | ⚠️ Cloud |

---

## ⚡ **Quick Setup**

### **1. Install Cloud Provider Dependencies**

```bash
# Install all cloud providers
uv pip install langchain-openai langchain-google-genai langchain-groq langchain-anthropic

# Or install specific provider
uv pip install langchain-openai      # OpenAI only
uv pip install langchain-google-genai # Gemini only
uv pip install langchain-groq         # Groq only
uv pip install langchain-anthropic    # Anthropic only

# Or use optional dependency group
pip install -e ".[cloud-llms]"
```

### **2. Get API Keys**

| Provider | Get API Key |
|----------|------------|
| **OpenAI** | https://platform.openai.com/api-keys |
| **Gemini** | https://makersuite.google.com/app/apikey |
| **Groq** | https://console.groq.com/keys |
| **Anthropic** | https://console.anthropic.com/account/keys |

### **3. Configure Environment**

Create or update `.env` file:

```env
# Choose your provider
LLM_PROVIDER=gemini              # ollama, openai, gemini, groq, anthropic

# Set API key
GEMINI_API_KEY=your_api_key_here

# Or use generic key (works for all)
LLM_API_KEY=your_api_key_here

# Models (auto-selected if not specified)
LLM_MODEL=gemini-1.5-flash       # Fast model
LLM_VISION_MODEL=gemini-1.5-flash # Vision model
```

---

## 🚀 **Provider-Specific Setup**

### **Option 1: Groq (Recommended for Speed)** ⚡

**Why Groq:**
- ✅ FREE tier available
- ✅ Fastest inference (200+ tokens/sec)
- ✅ Great accuracy
- ✅ Simple API

**Setup:**
```env
# .env
LLM_PROVIDER=groq
GROQ_API_KEY=gsk_your_api_key_here
LLM_MODEL=llama-3.3-70b-versatile    # Fast and powerful
# Note: Groq doesn't have vision models yet - mix with Gemini
LLM_VISION_MODEL=gemini-1.5-flash
GEMINI_API_KEY=your_gemini_key
```

**Models Available:**
- `llama-3.3-70b-versatile` - Best all-around
- `llama-3.1-8b-instant` - Fastest
- `mixtral-8x7b-32768` - Large context

**Performance:**
- Speed: ⚡⚡⚡⚡⚡ (Fastest!)
- Extraction time: **~2-3 seconds** (vs 6-8s local)

---

### **Option 2: Google Gemini (Best Balance)** ⭐

**Why Gemini:**
- ✅ FREE tier (1500 requests/day)
- ✅ Excellent vision support
- ✅ Fast and accurate
- ✅ Handles both text AND images

**Setup:**
```env
# .env
LLM_PROVIDER=gemini
GEMINI_API_KEY=your_gemini_api_key

# Recommended models
LLM_MODEL=gemini-1.5-flash           # Fast, good for extraction
LLM_VISION_MODEL=gemini-1.5-flash    # Same model does vision!

# Or use Pro for higher accuracy
# LLM_MODEL=gemini-1.5-pro
# LLM_VISION_MODEL=gemini-1.5-pro
```

**Models Available:**
- `gemini-1.5-flash` - Fast, multimodal (recommended)
- `gemini-1.5-pro` - Most accurate
- `gemini-2.0-flash-exp` - Latest experimental

**Performance:**
- Speed: ⚡⚡⚡⚡
- Extraction time: **~3-4 seconds**
- Vision: Native support (same model!)

---

### **Option 3: OpenAI (Best Accuracy)**

**Why OpenAI:**
- ✅ Highest accuracy
- ✅ Excellent vision support (GPT-4o)
- ✅ Reliable and mature
- ⚠️ Paid (no free tier)

**Setup:**
```env
# .env
LLM_PROVIDER=openai
OPENAI_API_KEY=sk-your_openai_api_key

# Recommended models
LLM_MODEL=gpt-4o-mini                # Cost-effective
LLM_VISION_MODEL=gpt-4o              # Best vision

# For maximum accuracy (more expensive)
# LLM_MODEL=gpt-4o
# LLM_VISION_MODEL=gpt-4o
```

**Models Available:**
- `gpt-4o-mini` - Fast and cheap ($0.15/1M tokens)
- `gpt-4o` - Best accuracy ($2.50/1M tokens)
- `gpt-4-turbo` - High performance

**Performance:**
- Speed: ⚡⚡⚡⚡
- Extraction time: **~3-5 seconds**
- Accuracy: ⭐⭐⭐⭐⭐ (Best)

---

### **Option 4: Anthropic Claude**

**Why Claude:**
- ✅ Excellent at structured extraction
- ✅ Good vision support
- ✅ Long context (200K tokens)
- ⚠️ Paid

**Setup:**
```env
# .env
LLM_PROVIDER=anthropic
ANTHROPIC_API_KEY=sk-ant-your_api_key

# Recommended models
LLM_MODEL=claude-3-5-haiku-20241022      # Fast
LLM_VISION_MODEL=claude-3-5-sonnet-20241022  # Vision
```

**Models Available:**
- `claude-3-5-haiku` - Fastest
- `claude-3-5-sonnet` - Best (supports vision)
- `claude-3-opus` - Most powerful

---

## 🔧 **Mixed Provider Configuration** (Recommended!)

You can mix providers for optimal performance:

```env
# Use fast Groq for text extraction
LLM_PROVIDER=groq
GROQ_API_KEY=your_groq_key
LLM_MODEL=llama-3.3-70b-versatile

# Use Gemini for vision (free!)
LLM_VISION_MODEL=gemini-1.5-flash
GEMINI_API_KEY=your_gemini_key
```

Or in code:

```python
from agent_extract.core.llm_provider import LLMFactory

# Groq for text (fast)
text_llm = LLMFactory.create_llm(
    provider="groq",
    model_name="llama-3.3-70b-versatile",
    is_vision=False
)

# Gemini for vision (free + excellent)
vision_llm = LLMFactory.create_llm(
    provider="gemini",
    model_name="gemini-1.5-flash",
    is_vision=True
)
```

---

## 📊 **Performance Comparison**

### **Local vs Cloud - Speed**

| Provider | Model | Avg Time/Call | Total Extraction |
|----------|-------|---------------|------------------|
| **Ollama** | qwen3:0.6b | 1-2s | ~8-12s |
| **Ollama** | gemma3:4b | 2-3s | ~10-15s |
| **Groq** | llama-3.3-70b | 0.2-0.5s | ⚡ **~2-3s** |
| **Gemini** | gemini-1.5-flash | 0.3-0.6s | **~3-4s** |
| **OpenAI** | gpt-4o-mini | 0.5-1s | **~4-5s** |
| **Anthropic** | claude-3-5-haiku | 0.4-0.8s | **~3-5s** |

### **Accuracy Comparison**

| Provider | Typed Docs | Scanned Docs | Forms/Invoices |
|----------|------------|--------------|----------------|
| **Ollama (qwen3)** | 85-90% | 80-85% | 85-90% |
| **Groq (llama3.3)** | 92-95% | 88-92% | 90-95% |
| **Gemini (flash)** | 93-96% | 90-94% | 92-96% |
| **OpenAI (gpt-4o)** | 95-98% | 93-96% | 94-98% |
| **Anthropic (sonnet)** | 94-97% | 91-95% | 93-97% |

---

## 💰 **Cost Comparison**

### **Free Options:**
1. **Ollama** - Completely free (local)
2. **Groq** - 30 requests/minute free
3. **Gemini** - 1500 requests/day free

### **Paid Options:**
| Provider | Model | Cost per 1M Tokens |
|----------|-------|-------------------|
| **OpenAI** | gpt-4o-mini | $0.15 input, $0.60 output |
| **OpenAI** | gpt-4o | $2.50 input, $10.00 output |
| **Gemini** | gemini-1.5-flash | $0.075 input, $0.30 output |
| **Gemini** | gemini-1.5-pro | $1.25 input, $5.00 output |
| **Anthropic** | claude-3-5-haiku | $0.80 input, $4.00 output |
| **Groq** | Above free tier | TBD |

**Typical document extraction**: ~10K tokens = **$0.001 - $0.05** per document

---

## 🎯 **Recommended Configurations**

### **For Maximum Speed** ⚡
```env
LLM_PROVIDER=groq
GROQ_API_KEY=your_key
LLM_MODEL=llama-3.3-70b-versatile
```
**Result**: 2-3 second extractions!

### **For Best Accuracy** 🎯
```env
LLM_PROVIDER=openai
OPENAI_API_KEY=your_key
LLM_MODEL=gpt-4o
LLM_VISION_MODEL=gpt-4o
```
**Result**: 95-98% accuracy

### **For Free + Fast** 🆓
```env
LLM_PROVIDER=gemini
GEMINI_API_KEY=your_key
LLM_MODEL=gemini-1.5-flash
LLM_VISION_MODEL=gemini-1.5-flash
```
**Result**: Free, fast, accurate!

### **For Privacy** 🔒
```env
LLM_PROVIDER=ollama
LLM_MODEL=qwen3:0.6b
LLM_VISION_MODEL=gemma3:4b
```
**Result**: 100% local, no data leaves your machine

### **Best of Both Worlds** 🌟
```env
# Fast Groq for text
LLM_PROVIDER=groq
GROQ_API_KEY=your_groq_key
LLM_MODEL=llama-3.3-70b-versatile

# Free Gemini for vision
LLM_VISION_MODEL=gemini-1.5-flash
GEMINI_API_KEY=your_gemini_key
```
**Result**: Fast + Free vision!

---

## 🔧 **Configuration Examples**

### **Complete .env Example**

```env
# === LLM Provider Configuration ===

# Choose provider: ollama, openai, gemini, groq, anthropic
LLM_PROVIDER=gemini

# API Keys (set the one you're using)
GEMINI_API_KEY=your_gemini_api_key_here
OPENAI_API_KEY=your_openai_api_key_here
GROQ_API_KEY=your_groq_api_key_here
ANTHROPIC_API_KEY=your_anthropic_api_key_here

# Models (auto-selected based on provider if not specified)
LLM_MODEL=gemini-1.5-flash
LLM_VISION_MODEL=gemini-1.5-flash

# LLM Settings
LLM_TEMPERATURE=0.1
LLM_MAX_TOKENS=4096

# === Local Ollama Settings (if using ollama provider) ===
LLM_BASE_URL=http://localhost:11434

# === OCR Settings ===
OCR_ENGINE=tesseract
OCR_LANGUAGE=eng

# === Processing ===
MAX_FILE_SIZE_MB=50
DEFAULT_OUTPUT_FORMAT=json
ENABLE_VISION_MODEL=true
ENABLE_ENTITY_EXTRACTION=true
```

---

## 💻 **Python API Usage**

### **Using Specific Provider**

```python
from pathlib import Path
from agent_extract.ai_extractor import AIDocumentExtractor
from agent_extract.core.config import Config

# Configure for Gemini
config = Config(
    llm_provider="gemini",
    llm_model="gemini-1.5-flash",
    llm_vision_model="gemini-1.5-flash",
    gemini_api_key="your_api_key"
)

# Extract with Gemini
extractor = AIDocumentExtractor(use_vision=True)
result = extractor.extract_sync(Path("document.pdf"))

print(f"Provider used: {config.llm_provider}")
print(f"Confidence: {result.confidence_score:.1%}")
```

### **Mix Providers for Optimal Performance**

```python
from agent_extract.core.llm_provider import LLMFactory

# Fast Groq for text extraction
text_llm = LLMFactory.create_llm(
    provider="groq",
    model_name="llama-3.3-70b-versatile",
    api_key="your_groq_key",
    is_vision=False
)

# Free Gemini for vision
vision_llm = LLMFactory.create_llm(
    provider="gemini",
    model_name="gemini-1.5-flash",
    api_key="your_gemini_key",
    is_vision=True
)
```

---

## 📈 **When to Use Each Provider**

### **Use Ollama (Local)** when:
- ✅ Privacy is critical
- ✅ No internet connection
- ✅ Free unlimited processing
- ✅ GDPR compliance required
- ✅ Experimenting/development

### **Use Groq** when:
- ✅ Speed is priority
- ✅ Have free tier quota
- ✅ Text-only extraction
- ✅ High-volume processing

### **Use Gemini** when:
- ✅ Need vision + text
- ✅ Want free tier
- ✅ Balance of speed and accuracy
- ✅ Multimodal documents

### **Use OpenAI** when:
- ✅ Maximum accuracy needed
- ✅ Complex documents
- ✅ Budget available
- ✅ Production system

### **Use Anthropic** when:
- ✅ Long documents (200K context)
- ✅ Structured extraction
- ✅ High accuracy needed
- ✅ Budget available

---

## 🎯 **Real-World Examples**

### **Example 1: Fast Batch Processing with Groq**

```bash
# Setup
export LLM_PROVIDER=groq
export GROQ_API_KEY=your_key

# Process 100 invoices in ~5 minutes (vs 15 minutes local)
uv run agent-extract batch ./invoices ./output --ai
```

### **Example 2: High-Accuracy Forms with Gemini**

```bash
# Setup
export LLM_PROVIDER=gemini
export GEMINI_API_KEY=your_key

# Extract from complex government form
uv run agent-extract extract complex_form.pdf --ai -o result.json
```

### **Example 3: Scanned Documents with OpenAI Vision**

```bash
# Setup
export LLM_PROVIDER=openai
export OPENAI_API_KEY=your_key

# Extract from scanned invoice image
uv run agent-extract extract scanned_invoice.png --ai -o data.json
```

### **Example 4: Mix Local + Cloud**

```python
# Use local Ollama for development
os.environ["LLM_PROVIDER"] = "ollama"
result_dev = extractor.extract_sync("dev_doc.pdf")

# Switch to Groq for production
os.environ["LLM_PROVIDER"] = "groq"
result_prod = extractor.extract_sync("prod_doc.pdf")
```

---

## 🔐 **Security Best Practices**

### **API Key Management**

```bash
# NEVER commit API keys to git!
# Use .env file (already in .gitignore)

# Good
echo "GEMINI_API_KEY=your_key" >> .env

# Bad
export GEMINI_API_KEY=your_key  # Lost after terminal closes
```

### **Environment Variables**

```python
# Load from .env automatically
from dotenv import load_dotenv
load_dotenv()

# Or set in code (for testing only)
import os
os.environ["GEMINI_API_KEY"] = "your_key"
```

---

## 📊 **Cost Optimization**

### **Strategy 1: Use Free Tiers**

```env
# Groq for text (free, fast)
LLM_PROVIDER=groq
GROQ_API_KEY=your_key
LLM_MODEL=llama-3.1-8b-instant

# Gemini for vision (free, 1500/day)
LLM_VISION_MODEL=gemini-1.5-flash
GEMINI_API_KEY=your_key
```

**Cost**: $0/month for most use cases!

### **Strategy 2: Local Development, Cloud Production**

```python
# Development (local)
if os.getenv("ENV") == "development":
    config.llm_provider = "ollama"
    
# Production (cloud for speed/accuracy)
else:
    config.llm_provider = "gemini"
```

### **Strategy 3: Fallback Chain**

```python
# Try Groq (fast, free)
# If quota exceeded → Gemini (free tier)
# If that fails → Ollama (local, always works)
```

---

## 🎯 **Recommended Setup by Use Case**

### **Startup / Personal Project**
```env
LLM_PROVIDER=gemini          # Free tier
GEMINI_API_KEY=your_key
```
**Cost**: $0/month

### **Small Business**
```env
LLM_PROVIDER=groq            # Fast processing
GROQ_API_KEY=your_key
LLM_VISION_MODEL=gemini-1.5-flash  # Free vision
GEMINI_API_KEY=your_key
```
**Cost**: ~$5-20/month

### **Enterprise**
```env
LLM_PROVIDER=openai          # Best accuracy
OPENAI_API_KEY=your_key
LLM_MODEL=gpt-4o
```
**Cost**: Based on volume

### **Privacy-Focused**
```env
LLM_PROVIDER=ollama          # 100% local
LLM_MODEL=qwen3:0.6b
```
**Cost**: $0, hardware only

---

## 🚀 **Quick Start**

### **1. Pick Your Provider**

Choose based on your needs (speed/accuracy/cost)

### **2. Get API Key**

Visit provider website and create key

### **3. Set Environment**

```bash
echo "LLM_PROVIDER=gemini" >> .env
echo "GEMINI_API_KEY=your_key" >> .env
```

### **4. Install Provider**

```bash
pip install langchain-google-genai
```

### **5. Test It**

```bash
uv run agent-extract extract document.pdf --ai -o result.json
```

**You're done!** ✅

---

## 🐛 **Troubleshooting**

### **Issue: API key not found**
```bash
# Check if key is set
echo $GEMINI_API_KEY  # Linux/Mac
echo %GEMINI_API_KEY%  # Windows CMD
$env:GEMINI_API_KEY    # Windows PowerShell
```

### **Issue: Provider package not installed**
```bash
pip install langchain-openai       # For OpenAI
pip install langchain-google-genai # For Gemini
pip install langchain-groq         # For Groq
pip install langchain-anthropic    # For Anthropic
```

### **Issue: Rate limit exceeded**
```
# Switch provider in .env
LLM_PROVIDER=gemini  # If Groq quota exceeded
```

---

## 📝 **Summary**

### **Quick Recommendations:**

| Your Priority | Provider | Why |
|--------------|----------|-----|
| **Speed** ⚡ | Groq | 200+ tokens/sec, free tier |
| **Accuracy** 🎯 | OpenAI gpt-4o | Best results |
| **Free** 🆓 | Gemini | 1500 req/day, multimodal |
| **Privacy** 🔒 | Ollama | 100% local |
| **Balance** ⭐ | Gemini | Fast, free, accurate |

### **My Recommendation for You:**

```env
# Start with Gemini (free + excellent)
LLM_PROVIDER=gemini
GEMINI_API_KEY=your_key
LLM_MODEL=gemini-1.5-flash
LLM_VISION_MODEL=gemini-1.5-flash
```

**Benefits:**
- ✅ **Free** (1500 requests/day)
- ✅ **Fast** (3-4 seconds vs 8-12s local)
- ✅ **Accurate** (93-96% vs 85-90% local)
- ✅ **Vision** (native multimodal support)
- ✅ **Easy** (single API key, one model for both)

**Result**: 3-4x faster, more accurate, still free!

---

**Ready to speed up your extractions? Pick a provider and add your API key!** 🚀

