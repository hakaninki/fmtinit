"""
Pytest configuration module.
Provides shared mock fixtures and testing utilities.
"""

from pathlib import Path

import pytest


@pytest.fixture
def tmp_project(tmp_path: Path) -> Path:
    """Create a temp directory representing a project root."""
    return tmp_path


@pytest.fixture
def python_project(tmp_path: Path) -> Path:
    """Create a temp directory with sample Python files."""
    (tmp_path / "main.py").write_text("print('hello')")
    (tmp_path / "utils.py").write_text("def helper(): pass")
    return tmp_path


@pytest.fixture
def js_project(tmp_path: Path) -> Path:
    """Create a temp directory with sample JS/TS files."""
    (tmp_path / "index.js").write_text("console.log('hello')")
    (tmp_path / "app.ts").write_text("const x: number = 1")
    return tmp_path


@pytest.fixture
def multi_lang_project(tmp_path: Path) -> Path:
    """Create a temp directory with Python, JS, YAML, and Markdown files."""
    (tmp_path / "main.py").write_text("print('hello')")
    (tmp_path / "index.js").write_text("console.log('hello')")
    (tmp_path / "config.yaml").write_text("key: value")
    (tmp_path / "README.md").write_text("# Hello")
    return tmp_path
