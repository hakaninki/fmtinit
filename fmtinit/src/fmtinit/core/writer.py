"""Module for writing configuration files from templates."""

from pathlib import Path


def write_config(template_path: Path, dest_path: Path, context: dict) -> None:
    """
    Read template_path, perform simple string substitution using context dict,
    and write result to dest_path.

    Args:
        template_path: Path to the template file.
        dest_path: Path where the output file should be written.
        context: Dictionary of key-value pairs for substitution.

    Raises:
        FileNotFoundError: If the template file does not exist.
    """
    if not template_path.exists():
        raise FileNotFoundError(f"Template not found: {template_path}")

    if dest_path.exists():
        print(f"Warning: {dest_path} already exists. Skipping.")
        return

    content = template_path.read_text(encoding="utf-8")
    for key, value in context.items():
        content = content.replace(f"{{{{{key}}}}}", str(value))

    dest_path.write_text(content, encoding="utf-8")


def _resolve_template(templates_dir: Path, possible_names: list[str]) -> Path:
    """Find the first existing template file from a list of possible names."""
    for name in possible_names:
        template_path = templates_dir / name
        if template_path.exists():
            return template_path
    return templates_dir / possible_names[-1]  # Return last one to fail gracefully


def write_editorconfig(project_path: Path, templates_dir: Path) -> None:
    """
    Write .editorconfig to project_path using the editorconfig template.
    Template is assumed to be either `.editorconfig.template` or just `.editorconfig`.

    Args:
        project_path: Path to the project root directory.
        templates_dir: Path to the directory containing templates.
    """
    possible_names = ["editorconfig.tpl", ".editorconfig.template", ".editorconfig"]
    template_path = _resolve_template(templates_dir, possible_names)
    dest_path = project_path / ".editorconfig"
    write_config(template_path, dest_path, {"INDENT_SIZE": "2"})


def write_prettier_config(project_path: Path, templates_dir: Path) -> None:
    """
    Write .prettierrc.json to project_path using the prettier template.
    Template is assumed to be either `.prettierrc.json.template` or `.prettierrc.json`.

    Args:
        project_path: Path to the project root directory.
        templates_dir: Path to the directory containing templates.
    """
    possible_names = [
        "prettier.json.tpl",
        ".prettierrc.json.template",
        ".prettierrc.json",
    ]
    template_path = _resolve_template(templates_dir, possible_names)
    dest_path = project_path / ".prettierrc.json"
    write_config(template_path, dest_path, {})
