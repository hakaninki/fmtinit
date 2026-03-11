"""scan command implementation."""

import pathlib

import typer
from rich.console import Console

from fmtinit.core.detector import detect_languages

console = Console()


def scan_project(
    path: pathlib.Path = typer.Option(
        pathlib.Path("."), "--path", help="Target project directory"
    ),
):
    """
    Detect supported languages in the project.
    """
    languages = detect_languages(path)

    if not languages:
        console.print("No supported languages detected.")
        return

    console.print(f"Detected languages: {', '.join(languages)}")
    console.print(
        f"Run [cyan]fmtinit init --langs {','.join(languages)}[/cyan] "
        "to configure formatters."
    )
