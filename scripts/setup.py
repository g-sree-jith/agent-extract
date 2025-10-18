#!/usr/bin/env python
"""Setup script to help users get started with agent-extract."""

import subprocess
import sys
from pathlib import Path


def run_command(cmd, description):
    """Run a command and handle errors."""
    print(f"\n{'='*60}")
    print(f"📦 {description}")
    print(f"{'='*60}")
    
    try:
        result = subprocess.run(
            cmd,
            shell=True,
            check=True,
            capture_output=True,
            text=True
        )
        print(result.stdout)
        print(f"✅ {description} - Success!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} - Failed!")
        print(f"Error: {e.stderr}")
        return False


def main():
    """Run setup steps."""
    print("""
    ╔═══════════════════════════════════════════════════════════╗
    ║                                                           ║
    ║           Agent-Extract Setup Assistant                   ║
    ║     Universal Document Intelligence Platform              ║
    ║                                                           ║
    ╚═══════════════════════════════════════════════════════════╝
    """)

    # Check Python version
    if sys.version_info < (3, 12):
        print("❌ Python 3.12 or higher is required!")
        print(f"   Current version: {sys.version}")
        sys.exit(1)
    
    print(f"✅ Python version: {sys.version.split()[0]}")

    steps = [
        ("pip install -e .", "Installing agent-extract package"),
        ("pip install -e .[dev]", "Installing development dependencies"),
    ]

    success_count = 0
    for cmd, description in steps:
        if run_command(cmd, description):
            success_count += 1

    print(f"\n{'='*60}")
    print(f"Setup Summary: {success_count}/{len(steps)} steps completed")
    print(f"{'='*60}\n")

    if success_count == len(steps):
        print("🎉 Setup completed successfully!\n")
        print("Next steps:")
        print("  1. Run tests: pytest")
        print("  2. Try the CLI: agent-extract --help")
        print("  3. Extract a document: agent-extract your_document.pdf")
        print("\nFor more information, see README.md and USAGE_GUIDE.md")
    else:
        print("⚠️  Some steps failed. Please check the errors above.")
        sys.exit(1)


if __name__ == "__main__":
    main()


