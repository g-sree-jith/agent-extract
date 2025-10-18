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
        help="Use AI-powered extraction with qwen3 and gemma3 (Phase 2)",
    ),
    no_vision: bool = typer.Option(
        False,
        "--no-vision",
        help="Disable vision model (gemma3) for AI extraction",
    ),
):
    """
    Extract data from a document and output as JSON or Markdown.
    
    Examples:
        agent-extract extract document.pdf
        agent-extract extract document.pdf --format markdown
        agent-extract extract image.png --output result.json
        agent-extract extract document.pdf --ai  # AI-powered extraction
    """
    try:
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
        mode_text = "[AI Mode with qwen3 + gemma3]" if use_ai else "[Standard Mode]"
        console.print(Panel.fit(
            f"[bold cyan]Processing document:[/bold cyan] {file_path.name} {mode_text}",
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
                # Use AI-powered extraction
                progress.update(task, description="Initializing AI agents (qwen3 + gemma3)...")
                ai_extractor = AIDocumentExtractor(
                    use_vision=not no_vision,
                    use_basic_extraction=True,
                )
                result = ai_extractor.extract_sync(file_path)
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


def _show_summary(result):
    """Show extraction summary."""
    console.print("\n[bold]Extraction Summary:[/bold]")
    console.print(f"  Document Type: [cyan]{result.metadata.document_type.value.upper()}[/cyan]")
    console.print(f"  Pages: [cyan]{result.metadata.page_count or 'N/A'}[/cyan]")
    console.print(f"  Text Length: [cyan]{len(result.raw_text)} characters[/cyan]")
    console.print(f"  Tables Found: [cyan]{len(result.tables)}[/cyan]")
    console.print(f"  Entities Found: [cyan]{len(result.entities)}[/cyan]")
    if result.processing_time:
        console.print(f"  Processing Time: [cyan]{result.processing_time:.2f}s[/cyan]")
    console.print()


if __name__ == "__main__":
    app()

