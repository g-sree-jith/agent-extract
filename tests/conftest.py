"""Pytest configuration and fixtures."""

import pytest
from pathlib import Path
import tempfile
import shutil

from agent_extract.core.config import Config


@pytest.fixture
def temp_dir():
    """Create a temporary directory for tests."""
    temp_path = Path(tempfile.mkdtemp())
    yield temp_path
    shutil.rmtree(temp_path)


@pytest.fixture
def sample_pdf_path():
    """Path to a sample PDF file."""
    # This will be created when actual test files are added
    return Path("tests/fixtures/sample.pdf")


@pytest.fixture
def sample_docx_path():
    """Path to a sample DOCX file."""
    return Path("tests/fixtures/sample.docx")


@pytest.fixture
def sample_image_path():
    """Path to a sample image file."""
    return Path("tests/fixtures/sample.png")


@pytest.fixture
def test_config():
    """Test configuration."""
    return Config(
        debug=True,
        max_file_size_mb=10,
        enable_cache=False,
    )


