"""Module for detecting programming languages in a project directory."""

from pathlib import Path

# Directories to ignore during the walk
IGNORE_DIRS = {
    "node_modules",
    ".git",
    "__pycache__",
    ".venv",
    "venv",
    "dist",
    "build",
    ".dart_tool",
}

# Extension to language mapping
EXT_MAP = {
    ".js": "javascript",
    ".ts": "typescript",
    ".tsx": "typescript",
    ".jsx": "javascript",
    ".py": "python",
    ".dart": "dart",
    ".json": "json",
    ".yaml": "yaml",
    ".yml": "yaml",
    ".md": "markdown",
    ".markdown": "markdown",
}


def detect_languages(project_path: Path) -> list[str]:
    """
    Walk the directory at project_path and return a list of language names
    detected based on file extensions.

    Args:
        project_path: The directory path to search in.

    Returns:
        A deduplicated, sorted list of detected language names. Matches exact
        values: "javascript", "typescript", "python", "dart", "json", "yaml", "markdown"

    Raises:
        ValueError: If project_path does not exist or is not a directory.
    """
    if not project_path.exists():
        raise ValueError(f"Directory {project_path} does not exist.")
    if not project_path.is_dir():
        raise ValueError(f"Path {project_path} is not a directory.")

    detected = set()

    # Iterative walk to avoid recursion limit and to easily skip ignore dirs
    dirs_to_visit = [project_path]

    while dirs_to_visit:
        current_dir = dirs_to_visit.pop()

        try:
            for item in current_dir.iterdir():
                if item.is_dir():
                    if item.name not in IGNORE_DIRS:
                        dirs_to_visit.append(item)
                elif item.is_file():
                    ext = item.suffix.lower()
                    if ext in EXT_MAP:
                        detected.add(EXT_MAP[ext])
        except PermissionError:
            pass  # Skip directories we cannot access

    return sorted(list(detected))
