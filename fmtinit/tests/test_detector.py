"""Tests for the detector module."""

from pathlib import Path

import pytest

from fmtinit.core.detector import detect_languages


def test_empty_dir_returns_empty_list(tmp_project: Path):
    assert detect_languages(tmp_project) == []


def test_py_files_returns_python(python_project: Path):
    assert detect_languages(python_project) == ["python"]


def test_js_ts_files_returns_sorted_list(js_project: Path):
    assert detect_languages(js_project) == ["javascript", "typescript"]


def test_all_supported_extensions_returns_all(multi_lang_project: Path):
    (multi_lang_project / "file.dart").write_text("void main() {}")
    (multi_lang_project / "file.json").write_text("{}")

    assert detect_languages(multi_lang_project) == [
        "dart",
        "javascript",
        "json",
        "markdown",
        "python",
        "yaml",
    ]

    (multi_lang_project / "app.ts").write_text("const x = 1;")
    assert detect_languages(multi_lang_project) == [
        "dart",
        "javascript",
        "json",
        "markdown",
        "python",
        "typescript",
        "yaml",
    ]


def test_ignore_node_modules(tmp_project: Path):
    node_modules = tmp_project / "node_modules"
    node_modules.mkdir()
    (node_modules / "index.js").write_text("console.log('hello')")
    assert detect_languages(tmp_project) == []


def test_ignore_pycache(tmp_project: Path):
    pycache = tmp_project / "__pycache__"
    pycache.mkdir()
    (pycache / "main.py").write_text("print('hello')")
    assert detect_languages(tmp_project) == []


def test_ignore_git(tmp_project: Path):
    git_dir = tmp_project / ".git"
    git_dir.mkdir()
    (git_dir / "config.py").write_text("print('hello')")
    assert detect_languages(tmp_project) == []


def test_ignore_venv(tmp_project: Path):
    venv = tmp_project / ".venv"
    venv.mkdir()
    (venv / "main.py").write_text("print('hello')")
    assert detect_languages(tmp_project) == []


def test_non_existent_path_raises_value_error(tmp_project: Path):
    bad_path = tmp_project / "does_not_exist"
    with pytest.raises(ValueError, match="does not exist"):
        detect_languages(bad_path)


def test_file_path_raises_value_error(tmp_project: Path):
    file_path = tmp_project / "file.txt"
    file_path.write_text("hello")
    with pytest.raises(ValueError, match="not a directory"):
        detect_languages(file_path)


def test_mixed_extensions_correct_deduplication(tmp_project: Path):
    (tmp_project / "1.js").write_text("")
    (tmp_project / "2.jsx").write_text("")
    (tmp_project / "3.yaml").write_text("")
    (tmp_project / "4.yml").write_text("")
    assert detect_languages(tmp_project) == ["javascript", "yaml"]


def test_unsupported_extensions_ignored(tmp_project: Path):
    (tmp_project / "image.png").write_text("")
    (tmp_project / "notes.txt").write_text("")
    assert detect_languages(tmp_project) == []
