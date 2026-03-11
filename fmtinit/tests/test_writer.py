"""Tests for the writer module."""

import json
from pathlib import Path

import pytest

from fmtinit.core.writer import write_config, write_editorconfig, write_prettier_config


@pytest.fixture
def mock_templates_dir(tmp_project: Path) -> Path:
    templates_dir = tmp_project / "templates"
    templates_dir.mkdir()
    (templates_dir / ".editorconfig.template").write_text(
        "root = true\nindent_style = space", encoding="utf-8"
    )
    (templates_dir / ".prettierrc.json.template").write_text(
        '{\n  "semi": false\n}', encoding="utf-8"
    )
    return templates_dir


def test_write_config_correct_content(tmp_project: Path):
    template = tmp_project / "template.txt"
    template.write_text("Hello {{NAME}}!", encoding="utf-8")

    dest = tmp_project / "output.txt"
    write_config(template, dest, {"NAME": "World"})

    assert dest.exists()
    assert dest.read_text(encoding="utf-8") == "Hello World!"


def test_write_config_replaces_keys(tmp_project: Path):
    template = tmp_project / "template.txt"
    template.write_text("A: {{A}}, B: {{B}}", encoding="utf-8")

    dest = tmp_project / "output.txt"
    write_config(template, dest, {"A": "1", "B": "2"})

    assert dest.read_text(encoding="utf-8") == "A: 1, B: 2"


def test_write_config_no_overwrite(tmp_project: Path, capsys):
    template = tmp_project / "template.txt"
    template.write_text("Hello {{NAME}}!", encoding="utf-8")

    dest = tmp_project / "output.txt"
    dest.write_text("Existing content", encoding="utf-8")

    write_config(template, dest, {"NAME": "World"})

    # Should not overwrite
    assert dest.read_text(encoding="utf-8") == "Existing content"

    # Should print warning
    captured = capsys.readouterr()
    assert "Warning" in captured.out
    assert "already exists. Skipping." in captured.out


def test_write_config_missing_template(tmp_project: Path):
    template = tmp_project / "missing.txt"
    dest = tmp_project / "output.txt"

    with pytest.raises(FileNotFoundError, match="Template not found"):
        write_config(template, dest, {})


def test_write_editorconfig(tmp_project: Path, mock_templates_dir: Path):
    write_editorconfig(tmp_project, mock_templates_dir)

    dest = tmp_project / ".editorconfig"
    assert dest.exists()
    content = dest.read_text(encoding="utf-8")
    assert "root = true" in content
    assert "indent_style" in content


def test_write_editorconfig_finds_tpl(tmp_project: Path, mock_templates_dir: Path):
    # Remove the .template files
    (mock_templates_dir / ".editorconfig.template").unlink()
    # Write the matching .tpl file
    (mock_templates_dir / "editorconfig.tpl").write_text(
        "root = found", encoding="utf-8"
    )

    write_editorconfig(tmp_project, mock_templates_dir)
    dest = tmp_project / ".editorconfig"
    assert dest.read_text(encoding="utf-8") == "root = found"


def test_write_prettier_config(tmp_project: Path, mock_templates_dir: Path):
    write_prettier_config(tmp_project, mock_templates_dir)

    dest = tmp_project / ".prettierrc.json"
    assert dest.exists()
    content = dest.read_text(encoding="utf-8")
    assert "{" in content
    assert "}" in content


def test_written_prettier_is_valid_json(tmp_project: Path, mock_templates_dir: Path):
    write_prettier_config(tmp_project, mock_templates_dir)

    dest = tmp_project / ".prettierrc.json"
    content = dest.read_text(encoding="utf-8")

    # Needs to be valid json
    parsed = json.loads(content)
    assert isinstance(parsed, dict)
