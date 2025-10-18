"""
Main entry point for agent-extract.

This file is kept for backwards compatibility.
Use the CLI via: agent-extract or python -m agent_extract.cli.main
"""

from agent_extract.cli.main import app


def main():
    """Run the CLI application."""
    app()


if __name__ == "__main__":
    main()
