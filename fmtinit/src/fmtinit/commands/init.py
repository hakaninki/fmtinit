"""init command implementation."""

import pathlib

import typer
from rich.console import Console

from fmtinit.core.hooks import write_hooks
from fmtinit.core.installer import install_formatters
from fmtinit.core.profiles import get_profiles, get_supported_languages
from fmtinit.core.state import update_state
from fmtinit.core.writer import write_editorconfig, write_prettier_config

console = Console()

TEMPLATES_DIR = pathlib.Path(__file__).parent.parent / "templates"


def init_project(
    langs: str = typer.Option(
        ..., "--langs", help="Comma-separated list of language names"
    ),
    path: pathlib.Path = typer.Option(
        pathlib.Path("."), "--path", help="Target project directory"
    ),
    dry_run: bool = typer.Option(False, "--dry-run", help="Dry run mode"),
):
    """
    Initialize formatting for the given languages in the project.
    """
    # 1. Parse --langs
    parsed_langs = [lang.strip().lower() for lang in langs.split(",") if lang.strip()]
    if not parsed_langs:
        console.print("[bold red]Error:[/bold red] No languages provided.")
        raise typer.Exit(1)

    # 2. Validate
    supported = set(get_supported_languages())
    unknown_langs = [lang for lang in parsed_langs if lang not in supported]
    if unknown_langs:
        uk_str = ", ".join(unknown_langs)
        supported_str = ", ".join(get_supported_languages())
        console.print(
            f"[bold red]Error:[/bold red] Unknown languages: {uk_str}\n"
            f"Supported are: {supported_str}"
        )
        raise typer.Exit(1)

    # 3. Get profiles
    profiles = get_profiles(parsed_langs)

    # 4. Install formatters
    if not dry_run:
        try:
            install_formatters(profiles, dry_run=dry_run)
        except RuntimeError as e:
            console.print(f"[bold red]Installation failed:[/bold red] {e}")
            raise typer.Exit(1)

    # 5. Write configs
    all_formatters = set()
    needs_prettier = False
    for p in profiles:
        for f in p.formatters:
            all_formatters.add(f)
            if "Prettier" in f or "prettier" in f.lower():
                needs_prettier = True

    if not dry_run:
        write_editorconfig(path, TEMPLATES_DIR)
        if needs_prettier:
            write_prettier_config(path, TEMPLATES_DIR)

    # 6. Write hooks
    if not dry_run:
        write_hooks(path, profiles, overwrite=False)

    # 7. Update state
    if not dry_run:
        update_state(path, parsed_langs, list(all_formatters))

    # 8. Print success summary
    langs_str = ", ".join(parsed_langs)
    if dry_run:
        console.print(
            f"[bold yellow]Dry-run complete.[/bold yellow] Would configure: {langs_str}"
        )
    else:
        console.print(
            f"[bold green]Success![/bold green] Configured formatters for: {langs_str}"
        )
