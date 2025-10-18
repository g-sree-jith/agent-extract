"""Create PNG visualization of agent workflow."""

from pathlib import Path
from agent_extract.agents.graph import DocumentExtractionGraph


def main():
    """Generate graph PNG."""
    print("Creating agent workflow visualization...")
    
    # Create graph with vision enabled
    graph = DocumentExtractionGraph(use_vision=True)
    
    try:
        # Get the compiled graph
        graph_repr = graph.graph.get_graph()
        
        # Try ASCII first
        print("\nASCII Representation:")
        print("=" * 60)
        ascii_diagram = graph_repr.draw_ascii()
        print(ascii_diagram)
        print("=" * 60)
        
        # Save ASCII to file
        Path("agent-orch-ascii.txt").write_text(ascii_diagram, encoding="utf-8")
        print("\n✅ ASCII diagram saved to: agent-orch-ascii.txt")
        
        # Try PNG (requires internet or pyppeteer)
        try:
            print("\nAttempting to create PNG...")
            png_data = graph_repr.draw_mermaid_png()
            Path("agent-orch.png").write_bytes(png_data)
            print("✅ PNG saved to: agent-orch.png")
        except Exception as e:
            print(f"⚠️  PNG generation requires internet connection: {e}")
            print("\n💡 Alternative: AGENT_WORKFLOW.md contains Mermaid diagram")
            print("   that will render beautifully on GitHub!")
            
    except Exception as e:
        print(f"❌ Error: {e}")


if __name__ == "__main__":
    main()

