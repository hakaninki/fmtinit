"""add command implementation."""

import pathlib

import typer
from rich.console import Console

from fmtinit.core.hooks import write_hooks
from fmtinit.core.installer import install_formatters
from fmtinit.core.profiles import get_profiles, get_supported_languages
from fmtinit.core.state import load_state, update_state

console = Console()

TEMPLATES_DIR = pathlib.Path(__file__).parent.parent / "templates"


def add_language(
    language: str = typer.Argument(..., help="Language to add"),
    path: pathlib.Path = typer.Option(
        pathlib.Path("."), "--path", help="Target project directory"
    ),
    dry_run: bool = typer.Option(False, "--dry-run", help="Dry run mode"),
):
    """
    Add a single language formatter to an already initialized project.
    """
    lang = language.strip().lower()

    # 1. Validate
    if lang not in set(get_supported_languages()):
        console.print(
            f"[bold red]Error:[/bold red] Unknown language '{lang}'. "
            f"Supported are: {', '.join(get_supported_languages())}"
        )
        raise typer.Exit(1)

    # 2. Load existing state
    state = load_state(path)

    # 3. Check if already installed
    if state and lang in state.installed_languages:
        console.print(f"[bold green]Already configured:[/bold green] {lang}")
        raise typer.Exit(0)

    # 4. Get profile and install
    profiles = get_profiles([lang])
    profile = profiles[0]

    all_formatters = profile.formatters

    if not dry_run:
        try:
            install_formatters([profile], dry_run=dry_run)
        except RuntimeError as e:
            console.print(f"[bold red]Installation failed:[/bold red] {e}")
            raise typer.Exit(1)

        # 5. Append hooks
        write_hooks(path, [profile], overwrite=False)

        # 6. Update state
        update_state(path, [lang], list(all_formatters))

    # 7. Print success
    if dry_run:
        console.print(f"[bold yellow]Dry-run complete.[/bold yellow] Would add: {lang}")
    else:
        console.print(f"[bold green]Success![/bold green] Added {lang} formatters.")
