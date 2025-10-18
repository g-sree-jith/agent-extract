# Contributing to Agent-Extract

First off, thank you for considering contributing to Agent-Extract! 🎉

## How Can I Contribute?

### Reporting Bugs

Before creating bug reports, please check the issue list as you might find out that you don't need to create one. When you are creating a bug report, please include as many details as possible:

* **Use a clear and descriptive title**
* **Describe the exact steps to reproduce the problem**
* **Provide specific examples** (sample documents, commands used)
* **Describe the behavior you observed and what you expected**
* **Include screenshots if relevant**
* **Note your environment** (OS, Python version, package versions)

### Suggesting Enhancements

Enhancement suggestions are tracked as GitHub issues. When creating an enhancement suggestion, please include:

* **Use a clear and descriptive title**
* **Provide a detailed description of the suggested enhancement**
* **Explain why this enhancement would be useful**
* **List any alternatives you've considered**

### Pull Requests

1. Fork the repo and create your branch from `master`
2. If you've added code that should be tested, add tests
3. Ensure the test suite passes
4. Make sure your code lints
5. Issue that pull request!

## Development Setup

```bash
# Clone your fork
git clone https://github.com/YOUR_USERNAME/agent-extract.git
cd agent-extract

# Install with development dependencies
uv sync --all-extras
# or
pip install -e ".[dev]"

# Run tests
pytest

# Run linting
ruff check src/ tests/
black src/ tests/ --check

# Format code
black src/ tests/
```

## Coding Style

* Follow PEP 8 guidelines
* Use type hints wherever possible
* Write descriptive docstrings for all public functions/classes
* Maximum line length: 100 characters
* Use `black` for code formatting
* Use `ruff` for linting

## Testing

* Write unit tests for all new features
* Ensure all tests pass before submitting PR
* Aim for >80% code coverage
* Test on multiple document types when relevant

## Commit Messages

* Use clear and meaningful commit messages
* Start with a verb in present tense (Add, Fix, Update, Remove)
* Keep the first line under 72 characters
* Add detailed description if needed

Examples:
```
Add support for Excel file extraction
Fix OCR encoding issue on Windows
Update documentation for CLI usage
```

## Project Structure

```
agent-extract/
├── src/agent_extract/    # Main package
│   ├── core/             # Core configuration and types
│   ├── readers/          # Document readers
│   ├── ocr/              # OCR engines
│   ├── outputs/          # Output formatters
│   ├── cli/              # CLI interface
│   ├── agents/           # AI agents (Phase 2+)
│   └── api/              # REST API (Phase 3+)
├── tests/                # Test suite
├── docs/                 # Documentation
└── scripts/              # Utility scripts
```

## Adding New Features

### Adding a New Document Reader

1. Create a new file in `src/agent_extract/readers/`
2. Inherit from `BaseReader`
3. Implement the `read()` method
4. Add file extensions to `supported_extensions`
5. Register in `ReaderFactory`
6. Write tests

Example:
```python
from agent_extract.readers.base import BaseReader
from agent_extract.core.types import ExtractionResult

class NewFormatReader(BaseReader):
    def __init__(self):
        super().__init__()
        self.supported_extensions = {".ext"}
    
    def read(self, file_path: Path) -> ExtractionResult:
        # Implementation
        pass
```

### Adding a New Output Format

1. Create a new file in `src/agent_extract/outputs/`
2. Implement `format()` and `format_to_file()` methods
3. Add tests
4. Update CLI to support new format

## Documentation

* Update README.md for user-facing changes
* Update USAGE_GUIDE.md for new features
* Add docstrings to all new code
* Update PROJECT_PLAN.md if adding new phases/features

## Questions?

Feel free to open an issue with the "question" label or reach out to the maintainers.

## Code of Conduct

### Our Pledge

We are committed to providing a welcoming and inspiring community for all.

### Our Standards

* Be respectful and inclusive
* Accept constructive criticism gracefully
* Focus on what is best for the community
* Show empathy towards others

Thank you for contributing! 🚀

