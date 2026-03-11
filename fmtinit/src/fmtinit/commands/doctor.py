"""doctor command implementation."""

import pathlib

import typer
from rich.console import Console

from fmtinit.core.state import load_state

console = Console()


def doctor_check(
    path: pathlib.Path = typer.Option(
        pathlib.Path("."), "--path", help="Target project directory"
    ),
):
    """
    Check for missing configuration files.
    """
    state = load_state(path)
    if not state:
        console.print("fmtinit has not been run in this directory.")
        raise typer.Exit(1)

    missing = False

    # Check .editorconfig
    if not (path / ".editorconfig").exists():
        console.print("[bold red][MISSING][/bold red] .editorconfig")
        missing = True
    else:
        console.print("[bold green][OK][/bold green] .editorconfig found")

    # Check .prettierrc.json
    prettier_langs = {"javascript", "typescript", "json", "yaml", "markdown"}
    uses_prettier = any(lang in prettier_langs for lang in state.installed_languages)
    uses_prettier_fmt = any("prettier" in f.lower() for f in state.installed_formatters)
    if uses_prettier or uses_prettier_fmt:
        if not (path / ".prettierrc.json").exists():
            langs_str = ",".join(state.installed_languages)
            console.print(
                f"[bold red][MISSING][/bold red] .prettierrc.json — "
                f"run 'fmtinit init --langs {langs_str}' to fix"
            )
            missing = True
        else:
            console.print("[bold green][OK][/bold green] .prettierrc.json found")

    # Check .pre-commit-config.yaml
    if not (path / ".pre-commit-config.yaml").exists():
        langs_str = ",".join(state.installed_languages)
        console.print(
            f"[bold red][MISSING][/bold red] .pre-commit-config.yaml — "
            f"run 'fmtinit init --langs {langs_str}' to fix"
        )
        missing = True
    else:
        console.print("[bold green][OK][/bold green] .pre-commit-config.yaml found")

    if missing:
        raise typer.Exit(1)

    raise typer.Exit(0)
