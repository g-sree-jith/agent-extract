"""Generate visualization of the LangGraph agent workflow."""

from pathlib import Path
from agent_extract.agents.graph import DocumentExtractionGraph


def generate_graph_image():
    """Generate and save the agent workflow graph."""
    print("Creating agent workflow graph...")
    
    # Create the extraction graph
    graph = DocumentExtractionGraph(use_vision=True)
    
    # Get the graph visualization
    try:
        # LangGraph can generate a Mermaid diagram or graphviz
        graph_repr = graph.graph.get_graph()
        
        # Try to draw the graph
        try:
            # This requires graphviz to be installed
            png_data = graph_repr.draw_mermaid_png()
            
            # Save to file
            output_path = Path("agent-orch.png")
            output_path.write_bytes(png_data)
            
            print(f"✅ Graph saved to: {output_path}")
            print(f"   Size: {len(png_data)} bytes")
            
        except Exception as e:
            print(f"⚠️  PNG generation failed: {e}")
            print("   Trying ASCII representation instead...")
            
            # Fallback: save as text diagram
            ascii_diagram = graph_repr.draw_ascii()
            output_path = Path("agent-orch.txt")
            output_path.write_text(ascii_diagram, encoding="utf-8")
            
            print(f"✅ ASCII diagram saved to: {output_path}")
            
    except Exception as e:
        print(f"❌ Error generating graph: {e}")
        print("\nGenerating manual diagram instead...")
        
        # Create manual diagram as fallback
        create_manual_diagram()


def create_manual_diagram():
    """Create a manual diagram using Mermaid markdown."""
    mermaid_diagram = """# Agent Orchestration Workflow

```mermaid
graph TD
    Start([Document Input]) --> Vision{Use Vision?}
    
    Vision -->|Yes| VisionAgent[Vision Analysis Agent<br/>gemma3:4b<br/>Layout & Structure]
    Vision -->|No| Schema[Schema Detection Agent<br/>qwen3:0.6b<br/>Document Type]
    
    VisionAgent --> Schema
    
    Schema --> Extract[Content Extraction Agent<br/>qwen3:0.6b<br/>Key-Value Pairs]
    
    Extract --> CheckTables{Has Tables?}
    
    CheckTables -->|Yes| TableAgent[Table Parser Agent<br/>qwen3:0.6b<br/>Enhanced Tables]
    CheckTables -->|No| Validate[Validation Agent<br/>qwen3:0.6b<br/>Quality Check]
    
    TableAgent --> Validate
    
    Validate --> End([Structured Output<br/>JSON/Markdown])
    
    style VisionAgent fill:#e1f5ff
    style Schema fill:#fff4e1
    style Extract fill:#ffe1f5
    style TableAgent fill:#e1ffe1
    style Validate fill:#f5e1ff
    style Start fill:#e8e8e8
    style End fill:#e8e8e8
```

## Agent Details

### 1. Vision Analysis Agent (gemma3:4b)
- **Input**: Image file path
- **Output**: Layout analysis, quality assessment
- **Purpose**: Understand document structure visually
- **Model**: gemma3:4b (3.3 GB, multimodal)

### 2. Schema Detection Agent (qwen3:0.6b)
- **Input**: Raw text
- **Output**: Document type, key fields to extract
- **Purpose**: Classify document and identify schema
- **Model**: qwen3:0.6b (522 MB, tool calling)

### 3. Content Extraction Agent (qwen3:0.6b)
- **Input**: Raw text + detected schema
- **Output**: Structured data (key-value pairs), entities
- **Purpose**: Extract relevant information
- **Model**: qwen3:0.6b (522 MB, tool calling)

### 4. Table Parser Agent (qwen3:0.6b)
- **Input**: Detected tables + raw text
- **Output**: Enhanced table data
- **Purpose**: Improve table extraction accuracy
- **Model**: qwen3:0.6b (522 MB, tool calling)

### 5. Validation Agent (qwen3:0.6b)
- **Input**: All extracted data
- **Output**: Validated data, confidence score
- **Purpose**: Quality assurance and corrections
- **Model**: qwen3:0.6b (522 MB, tool calling)

## Workflow States

```
Initial State:
  - file_path: str
  - raw_text: str (from OCR/reader)
  - document_type: None

After Schema Detection:
  - document_type: detected
  - detected_schema: {...}
  - confidence_score: float

After Content Extraction:
  - structured_data: {...}
  - entities: [...]

After Table Parsing:
  - tables: [enhanced...]

After Validation:
  - confidence_score: final
  - all data validated

Final Output:
  - ExtractionResult with all data
```

## Features

- ✅ Multi-agent collaboration
- ✅ Conditional routing based on document type
- ✅ Vision model integration for images
- ✅ Tool calling support (qwen3)
- ✅ Quality validation
- ✅ Error tracking
- ✅ Processing step history

## Performance

- **qwen3:0.6b**: ~100-200ms per agent call
- **gemma3:4b**: ~300-500ms for vision analysis
- **Total**: Varies by document complexity (typically 2-5 seconds)
"""
    
    output_path = Path("AGENT_WORKFLOW.md")
    output_path.write_text(mermaid_diagram, encoding="utf-8")
    print(f"✅ Workflow diagram saved to: {output_path}")
    print("   This file contains Mermaid diagram that can be viewed on GitHub!")


if __name__ == "__main__":
    generate_graph_image()

