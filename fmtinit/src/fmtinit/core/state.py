"""Module for state management in fmtinit."""

import json
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from pathlib import Path

STATE_FILE = ".fmtinit-state.json"


@dataclass
class FmtInitState:
    """Dataclass representing the state of fmtinit formatting in a project."""

    installed_languages: list[str]
    installed_formatters: list[str]
    initialized_at: str


def load_state(project_path: Path) -> FmtInitState | None:
    """
    Load state from .fmtinit-state.json in project_path.

    Args:
        project_path: Path to the project directory.

    Returns:
        FmtInitState object if it exists, otherwise None.

    Raises:
        ValueError: If the file exists but is invalid JSON.
    """
    state_path = project_path / STATE_FILE
    if not state_path.exists():
        return None

    try:
        data = json.loads(state_path.read_text(encoding="utf-8"))
        return FmtInitState(
            installed_languages=data.get("installed_languages", []),
            installed_formatters=data.get("installed_formatters", []),
            initialized_at=data.get("initialized_at", ""),
        )
    except json.JSONDecodeError as e:
        raise ValueError(f"Invalid JSON in state file: {e}") from e


def save_state(project_path: Path, state: FmtInitState) -> None:
    """
    Write state to .fmtinit-state.json in project_path.
    Creates the file if it does not exist. Overwrites if it does.

    Args:
        project_path: Path to the project directory.
        state: The FmtInitState object to save.
    """
    state_path = project_path / STATE_FILE
    with state_path.open("w", encoding="utf-8") as f:
        json.dump(asdict(state), f, indent=2)


def update_state(
    project_path: Path, new_languages: list[str], new_formatters: list[str]
) -> FmtInitState:
    """
    Load existing state (or create new), add new_languages and new_formatters
    (deduplicating), save, and return the updated state.

    Args:
        project_path: Path to the project directory.
        new_languages: List of languages to add.
        new_formatters: List of formatters to add.

    Returns:
        The updated FmtInitState object.
    """
    state = load_state(project_path)

    if state is None:
        state = FmtInitState(
            installed_languages=[],
            installed_formatters=[],
            initialized_at=datetime.now(timezone.utc).isoformat(),
        )

    # Deduplicate while preserving order across updates conceptually
    installed_langs = set(state.installed_languages)
    for lang in new_languages:
        if lang not in installed_langs:
            state.installed_languages.append(lang)
            installed_langs.add(lang)

    installed_fmts = set(state.installed_formatters)
    for fmt in new_formatters:
        if fmt not in installed_fmts:
            state.installed_formatters.append(fmt)
            installed_fmts.add(fmt)

    save_state(project_path, state)
    return state
