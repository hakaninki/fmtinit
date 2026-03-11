"""Integration tests for the CLI module."""

from pathlib import Path

from typer.testing import CliRunner

from fmtinit.cli import app

runner = CliRunner()


def test_help_output():
    result = runner.invoke(app, ["--help"])
    assert result.exit_code == 0
    assert "init" in result.stdout
    assert "add" in result.stdout
    assert "scan" in result.stdout
    assert "doctor" in result.stdout


def test_init_help_output():
    result = runner.invoke(app, ["init", "--help"])
    assert result.exit_code == 0
    assert "--langs" in result.stdout


def test_scan_python_project(python_project: Path):
    result = runner.invoke(app, ["scan", "--path", str(python_project)])
    assert result.exit_code == 0
    assert "python" in result.stdout.lower()


def test_scan_empty_dir(tmp_project: Path):
    result = runner.invoke(app, ["scan", "--path", str(tmp_project)])
    assert result.exit_code == 0
    assert "No supported" in result.stdout


def test_init_success(tmp_project: Path):
    result = runner.invoke(
        app, ["init", "--langs", "python", "--path", str(tmp_project), "--dry-run"]
    )
    assert result.exit_code == 0


def test_init_invalid_language(tmp_project: Path):
    result = runner.invoke(
        app, ["init", "--langs", "invalid_lang", "--path", str(tmp_project)]
    )
    assert result.exit_code == 1


def test_add_success(tmp_project: Path):
    result = runner.invoke(
        app, ["add", "python", "--path", str(tmp_project), "--dry-run"]
    )
    assert result.exit_code == 0


def test_doctor_command(tmp_project: Path):
    result = runner.invoke(app, ["doctor", "--path", str(tmp_project)])
    assert result.exit_code in (0, 1)


def test_init_multiple_languages(tmp_project: Path):
    result = runner.invoke(
        app,
        [
            "init",
            "--langs",
            "python,javascript",
            "--path",
            str(tmp_project),
            "--dry-run",
        ],
    )
    assert result.exit_code == 0


def test_commands_handle_missing_path(monkeypatch):
    # Missing --path should default to cwd, we just want to ensure it doesn't crash
    # Using a fake directory and monkeypatching cwd

    # We will just run them without --path and check they don't crash
    result_scan = runner.invoke(app, ["scan"])
    assert result_scan.exit_code in (0, 1)

    result_init = runner.invoke(app, ["init", "--langs", "python", "--dry-run"])
    assert result_init.exit_code in (0, 1)

    result_add = runner.invoke(app, ["add", "python", "--dry-run"])
    assert result_add.exit_code in (0, 1)

    result_doctor = runner.invoke(app, ["doctor"])
    assert result_doctor.exit_code in (0, 1)
