"""Main CLI application using Typer."""

from pathlib import Path
from typing import Optional
import sys
import platform
import typer
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn
from rich import print as rprint

from agent_extract.core.config import Config
from agent_extract.core.types import OutputFormat
from agent_extract.readers.factory import ReaderFactory
from agent_extract.ocr.ocr_manager import OCRManager
from agent_extract.outputs.json_formatter import JSONFormatter
from agent_extract.outputs.markdown_formatter import MarkdownFormatter
from agent_extract.ai_extractor import AIDocumentExtractor

app = typer.Typer(
    name="agent-extract",
    help="Universal Document Intelligence Platform - Extract data from any document format",
    add_completion=False,
)

# Configure console for Windows compatibility
# Use legacy_windows=False and force UTF-8 encoding to avoid charmap issues
is_windows = platform.system() == "Windows"
console = Console(
    legacy_windows=False,
    force_terminal=True,
    force_interactive=True,
)


@app.command()
def extract(
    file_path: Path = typer.Argument(
        ...,
        help="Path to the document file to extract",
        exists=True,
        file_okay=True,
        dir_okay=False,
        resolve_path=True,
    ),
    output_format: str = typer.Option(
        "json",
        "--format",
        "-f",
        help="Output format: json or markdown",
    ),
    output_file: Optional[Path] = typer.Option(
        None,
        "--output",
        "-o",
        help="Output file path (default: prints to console)",
    ),
    no_ocr: bool = typer.Option(
        False,
        "--no-ocr",
        help="Disable OCR for image extraction",
    ),
    use_ai: bool = typer.Option(
        False,
        "--ai",
        help="Use AI-powered extraction (Phase 2)",
    ),
    no_vision: bool = typer.Option(
        False,
        "--no-vision",
        help="Disable vision model for AI extraction",
    ),
    llm_provider: str = typer.Option(
        "ollama",
        "--provider",
        "-p",
        help="LLM provider: 'ollama' (local, private) or 'gemini' (cloud, fast)",
    ),
    llm_model: str = typer.Option(
        None,
        "--model",
        "-m",
        help="Override model name (e.g., qwen3:0.6b, gemini-pro, gpt-4o-mini)",
    ),
):
    """
    Extract data from a document and output as JSON or Markdown.
    
    Examples:
        # Standard extraction (fast)
        agent-extract extract document.pdf
        
        # AI with local models (private)
        agent-extract extract document.pdf --ai --provider ollama
        
        # AI with Gemini (fast, requires API key)
        agent-extract extract document.pdf --ai --provider gemini
        
        # Custom model
        agent-extract extract document.pdf --ai --provider ollama --model qwen3:0.6b
    """
    try:
        # Configure LLM provider based on user selection
        if use_ai:
            _configure_llm_provider(llm_provider, llm_model, console)
        # Validate output format
        if output_format.lower() not in ["json", "markdown", "md"]:
            console.print(
                f"[red]Error: Invalid output format '{output_format}'. "
                f"Use 'json' or 'markdown'[/red]"
            )
            raise typer.Exit(1)

        # Normalize format
        output_fmt = "markdown" if output_format.lower() == "md" else output_format.lower()

        # Show processing message
        if use_ai:
            from agent_extract.core.config import config as cfg
            if llm_provider == "ollama":
                mode_text = f"[AI: Local {cfg.llm_model}]"
            else:
                mode_text = f"[AI: {llm_provider.upper()} {llm_model or 'default'}]"
        else:
            mode_text = "[Standard]"
        
        console.print(Panel.fit(
            f"[bold cyan]Processing:[/bold cyan] {file_path.name} {mode_text}",
            border_style="cyan"
        ))

        # Use simpler progress indicators on Windows to avoid encoding issues
        progress_columns = [
            TextColumn("[progress.description]{task.description}"),
        ]
        
        # Add spinner only if not on Windows or if encoding supports it
        if not is_windows:
            progress_columns.insert(0, SpinnerColumn())
        
        with Progress(
            *progress_columns,
            console=console,
            transient=True,  # Makes progress disappear after completion
        ) as progress:
            # Initialize OCR if needed
            ocr_engine = None
            if not no_ocr:
                task = progress.add_task("Initializing OCR engine...", total=None)
                try:
                    ocr_engine = OCRManager.from_config()
                    progress.update(task, description="[green]OK[/green] OCR engine ready", completed=True)
                except Exception as e:
                    progress.update(task, description=f"[yellow]WARN[/yellow] OCR initialization failed: {e}", completed=True)

            # Create reader factory
            task = progress.add_task("Loading document...", total=None)
            factory = ReaderFactory(ocr_engine=ocr_engine)
            reader = factory.get_reader(file_path)
            progress.update(task, description=f"[green]OK[/green] Using {reader.__class__.__name__}", completed=True)

            # Extract content
            task = progress.add_task("Extracting content...", total=None)
            
            if use_ai:
                # Use AI-powered extraction with logging
                progress.update(task, description="Initializing AI agents (qwen3 + gemma3)...")
                
                console.print("\n[bold cyan]AI Agent Workflow:[/bold cyan]")
                
                ai_extractor = AIDocumentExtractor(
                    use_vision=not no_vision,
                    use_basic_extraction=True,
                )
                
                # Extract with agent callback for logging
                result = _extract_with_logging(ai_extractor, file_path, console)
                
                progress.update(task, description="[green]OK[/green] AI extraction complete", completed=True)
            else:
                # Use standard extraction
                result = reader.read(file_path)
                progress.update(task, description="[green]OK[/green] Content extracted", completed=True)

            # Format output
            task = progress.add_task("Formatting output...", total=None)
            if output_fmt == "json":
                formatter = JSONFormatter()
                output_str = formatter.format(result)
            else:
                formatter = MarkdownFormatter()
                output_str = formatter.format(result)
            progress.update(task, description="[green]OK[/green] Output formatted", completed=True)

        # Save or print output
        if output_file:
            output_file.write_text(output_str, encoding="utf-8")
            console.print(f"\n[green]SUCCESS[/green] Output saved to: [bold]{output_file}[/bold]")
        else:
            console.print("\n[bold cyan]Extraction Result:[/bold cyan]\n")
            # Print with safe encoding
            try:
                console.print(output_str)
            except UnicodeEncodeError:
                # Fallback to plain print if console encoding fails
                print(output_str)

        # Show summary
        _show_summary(result)

    except Exception as e:
        console.print(f"\n[red]Error:[/red] {str(e)}")
        raise typer.Exit(1)


@app.command()
def batch(
    input_dir: Path = typer.Argument(
        ...,
        help="Directory containing documents to process",
        exists=True,
        file_okay=False,
        dir_okay=True,
        resolve_path=True,
    ),
    output_dir: Path = typer.Argument(
        ...,
        help="Directory to save extraction results",
    ),
    output_format: str = typer.Option(
        "json",
        "--format",
        "-f",
        help="Output format: json or markdown",
    ),
    pattern: str = typer.Option(
        "*.*",
        "--pattern",
        "-p",
        help="File pattern to match (e.g., '*.pdf')",
    ),
):
    """
    Batch process multiple documents in a directory.
    
    Example:
        agent-extract batch ./documents ./output --format json --pattern "*.pdf"
    """
    try:
        # Create output directory
        output_dir.mkdir(parents=True, exist_ok=True)

        # Find matching files
        files = list(input_dir.glob(pattern))
        
        if not files:
            console.print(f"[yellow]No files found matching pattern '{pattern}' in {input_dir}[/yellow]")
            return

        console.print(f"\n[bold cyan]Found {len(files)} file(s) to process[/bold cyan]\n")

        # Initialize OCR and factory once
        ocr_engine = OCRManager.from_config()
        factory = ReaderFactory(ocr_engine=ocr_engine)

        # Process each file
        success_count = 0
        error_count = 0

        with Progress(console=console) as progress:
            task = progress.add_task("[cyan]Processing files...", total=len(files))

            for file_path in files:
                try:
                    # Extract
                    reader = factory.get_reader(file_path)
                    result = reader.read(file_path)

                    # Format
                    output_fmt = "markdown" if output_format.lower() == "md" else output_format.lower()
                    if output_fmt == "json":
                        formatter = JSONFormatter()
                        output_str = formatter.format(result)
                        ext = ".json"
                    else:
                        formatter = MarkdownFormatter()
                        output_str = formatter.format(result)
                        ext = ".md"

                    # Save
                    output_file = output_dir / f"{file_path.stem}{ext}"
                    output_file.write_text(output_str, encoding="utf-8")

                    success_count += 1
                    console.print(f"[green]OK[/green] {file_path.name}")

                except Exception as e:
                    error_count += 1
                    console.print(f"[red]FAIL[/red] {file_path.name}: {str(e)}")

                progress.update(task, advance=1)

        # Summary
        console.print(f"\n[bold]Summary:[/bold]")
        console.print(f"  Success: [green]{success_count}[/green]")
        console.print(f"  Failed:  [red]{error_count}[/red]")
        console.print(f"  Output:  [cyan]{output_dir}[/cyan]")

    except Exception as e:
        console.print(f"\n[red]Error:[/red] {str(e)}")
        raise typer.Exit(1)


@app.command()
def info():
    """
    Show information about supported formats and configuration.
    """
    console.print("\n[bold cyan]Agent-Extract - Document Intelligence Platform[/bold cyan]\n")

    # Supported formats
    factory = ReaderFactory()
    formats = factory.get_supported_formats()

    table = Table(title="Supported Document Formats", show_header=True, header_style="bold magenta")
    table.add_column("Format Type", style="cyan")
    table.add_column("Extensions", style="green")

    for format_type, extensions in formats.items():
        table.add_row(format_type, ", ".join(extensions))

    console.print(table)

    # Configuration
    console.print("\n[bold]Current Configuration:[/bold]")
    config = Config()
    console.print(f"  OCR Engine: [cyan]{config.ocr_engine}[/cyan]")
    console.print(f"  OCR Language: [cyan]{config.ocr_language}[/cyan]")
    console.print(f"  LLM Model: [cyan]{config.llm_model}[/cyan]")
    console.print(f"  Max File Size: [cyan]{config.max_file_size_mb} MB[/cyan]")
    console.print(f"  Default Output: [cyan]{config.default_output_format}[/cyan]")
    console.print()


@app.command()
def version():
    """Show version information."""
    from agent_extract import __version__
    console.print(f"[bold cyan]agent-extract[/bold cyan] version [green]{__version__}[/green]")


def _extract_with_logging(ai_extractor, file_path, console):
    """Extract with real-time agent logging."""
    import asyncio
    import time
    
    async def extract_with_progress():
        """Run extraction with progress updates."""
        start_time = time.time()
        
        # Step 1: Basic extraction
        console.print("  [dim]>[/dim] Running Phase 1 extraction (OCR/PDF parsing)...")
        basic_result = await ai_extractor._basic_extraction(file_path)
        console.print(f"    [green]+[/green] Text extracted: {len(basic_result.raw_text)} chars")
        
        # Step 2: Prepare state
        initial_state = ai_extractor._prepare_agent_state(file_path, basic_result)
        console.print("  [dim]>[/dim] Starting AI agent workflow...\n")
        
        # Step 3: Run agents with logging
        final_state = await _run_agents_with_logging(
            ai_extractor.agent_graph,
            initial_state,
            console
        )
        
        # Step 4: Build result
        processing_time = time.time() - start_time
        result = ai_extractor._build_extraction_result(
            file_path,
            basic_result,
            final_state,
            processing_time,
        )
        
        return result
    
    return asyncio.run(extract_with_progress())


async def _run_agents_with_logging(graph, initial_state, console):
    """Run agent graph with step-by-step logging."""
    from langchain_core.runnables import RunnableConfig
    
    # Track which agents have run
    agents_run = set()
    step_count = 0
    max_steps = 10  # Safety limit
    
    # Manual workflow execution with logging
    state = initial_state
    
    # Step 1: Planner
    console.print("  [yellow]1. Planner Agent[/yellow] - Creating extraction strategy...")
    state = await graph.planner_agent.process(state)
    plan = state.get("structured_data", {}).get("extraction_plan", {})
    console.print(f"     [green]+[/green] Strategy: {plan.get('extraction_approach', 'unknown')} approach")
    console.print(f"     [green]+[/green] Category: {plan.get('document_category', 'unknown')}")
    
    # Step 2-N: Supervisor loop
    while state.get("next_action") != "complete" and step_count < max_steps:
        step_count += 1
        
        # Supervisor decides
        console.print(f"\n  [yellow]{step_count+1}. Supervisor Agent[/yellow] - Deciding next step...")
        state = await graph.supervisor_agent.process(state)
        next_action = state.get("next_action", "complete")
        
        if next_action == "complete":
            console.print(f"     [green]+[/green] Decision: Workflow complete!")
            break
        
        console.print(f"     [green]+[/green] Routing to: {next_action}")
        
        # Execute the chosen agent
        step_count += 1
        if next_action == "schema":
            console.print(f"  [yellow]{step_count+1}. Schema Agent[/yellow] - Detecting document type...")
            state = await graph.schema_agent.process(state)
            schema = state.get("detected_schema", {})
            console.print(f"     [green]+[/green] Type: {schema.get('document_type', 'unknown')}")
            console.print(f"     [green]+[/green] Confidence: {schema.get('confidence', 0):.1%}")
            
        elif next_action == "extraction":
            console.print(f"  [yellow]{step_count+1}. Extraction Agent[/yellow] - Extracting structured data...")
            state = await graph.extraction_agent.process(state)
            data = state.get("structured_data", {})
            entities = state.get("entities", [])
            console.print(f"     [green]+[/green] Fields extracted: {len([k for k in data.keys() if k not in ['extraction_plan', 'ai_processing', 'quality_critique']])}")
            console.print(f"     [green]+[/green] Entities found: {len(entities)}")
            
        elif next_action == "table_parser":
            console.print(f"  [yellow]{step_count+1}. Table Parser Agent[/yellow] - Analyzing tables...")
            state = await graph.table_agent.process(state)
            tables = state.get("tables", [])
            console.print(f"     [green]+[/green] Tables processed: {len(tables)}")
            
        elif next_action == "vision" and graph.vision_agent:
            console.print(f"  [yellow]{step_count+1}. Vision Agent (gemma3)[/yellow] - Analyzing image...")
            state = await graph.vision_agent.process(state)
            console.print(f"     [green]+[/green] Vision analysis complete")
            
        elif next_action == "critic":
            console.print(f"  [yellow]{step_count+1}. Critic Agent[/yellow] - Validating quality...")
            state = await graph.critic_agent.process(state)
            critique = state.get("structured_data", {}).get("quality_critique", {})
            console.print(f"     [green]+[/green] Quality: {critique.get('overall_quality', 'unknown')}")
            console.print(f"     [green]+[/green] Confidence: {state.get('confidence_score', 0):.1%}")
            console.print(f"     [green]+[/green] Verdict: {critique.get('final_verdict', 'unknown')}")
            
        else:
            # Unknown action, complete
            state["next_action"] = "complete"
            break
    
    if step_count >= max_steps:
        console.print(f"\n  [yellow]![/yellow] Max steps reached ({max_steps}), completing extraction")
    
    console.print(f"\n  [bold green]DONE Workflow complete![/bold green] ({step_count} agent calls)\n")
    
    return state


def _configure_llm_provider(provider: str, model: str, console):
    """Configure LLM provider based on user selection."""
    from agent_extract.core.config import config
    
    # Validate provider
    valid_providers = ["ollama", "gemini", "openai", "groq", "anthropic"]
    if provider.lower() not in valid_providers:
        console.print(f"[yellow]Warning:[/yellow] Unknown provider '{provider}'. Using 'ollama'")
        provider = "ollama"
    
    # Set provider
    config.llm_provider = provider.lower()
    
    # Set model if specified
    if model:
        config.llm_model = model
        config.llm_vision_model = model
    elif provider.lower() == "gemini":
        # Auto-configure for Gemini
        config.llm_model = "gemini-pro"
        config.llm_vision_model = "gemini-pro"
        
        # Check API key
        if not config.gemini_api_key:
            console.print("[yellow]⚠ Warning:[/yellow] GEMINI_API_KEY not set. Set it in .env or environment")
            console.print("   Example: $env:GEMINI_API_KEY=\"your_key_here\"")
            console.print("   Falling back to Ollama...")
            config.llm_provider = "ollama"
            config.llm_model = "qwen3:0.6b"
            config.llm_vision_model = "gemma3:4b"
    elif provider.lower() == "openai":
        config.llm_model = "gpt-4o-mini"
        config.llm_vision_model = "gpt-4o"
        
        if not config.openai_api_key:
            console.print("[yellow]⚠ Warning:[/yellow] OPENAI_API_KEY not set. Falling back to Ollama...")
            config.llm_provider = "ollama"
            config.llm_model = "qwen3:0.6b"
    elif provider.lower() == "groq":
        config.llm_model = "llama-3.3-70b-versatile"
        
        if not config.groq_api_key:
            console.print("[yellow]⚠ Warning:[/yellow] GROQ_API_KEY not set. Falling back to Ollama...")
            config.llm_provider = "ollama"
            config.llm_model = "qwen3:0.6b"
    
    # Show what's being used
    console.print(f"\n[dim]Using LLM Provider:[/dim] [cyan]{config.llm_provider}[/cyan]")
    console.print(f"[dim]Text Model:[/dim] [cyan]{config.llm_model}[/cyan]")
    console.print(f"[dim]Vision Model:[/dim] [cyan]{config.llm_vision_model}[/cyan]\n")


def _show_summary(result):
    """Show extraction summary."""
    console.print("\n[bold]Extraction Summary:[/bold]")
    console.print(f"  Document Type: [cyan]{result.metadata.document_type.value.upper()}[/cyan]")
    console.print(f"  Pages: [cyan]{result.metadata.page_count or 'N/A'}[/cyan]")
    console.print(f"  Text Length: [cyan]{len(result.raw_text)} characters[/cyan]")
    console.print(f"  Tables Found: [cyan]{len(result.tables)}[/cyan]")
    console.print(f"  Entities Found: [cyan]{len(result.entities)}[/cyan]")
    
    # Show AI processing info if available
    ai_info = result.structured_data.get("ai_processing", {})
    if ai_info:
        console.print(f"  AI Agents Used: [cyan]{len(set(s.split(']')[0].replace('[', '') for s in ai_info.get('agents_used', []) if ']' in s))}[/cyan]")
        detected_type = ai_info.get("detected_document_type")
        if detected_type:
            console.print(f"  Detected Type: [cyan]{detected_type}[/cyan]")
    
    if result.processing_time:
        console.print(f"  Processing Time: [cyan]{result.processing_time:.2f}s[/cyan]")
    
    if result.confidence_score:
        console.print(f"  Confidence Score: [cyan]{result.confidence_score:.1%}[/cyan]")
    
    console.print()


if __name__ == "__main__":
    app()

