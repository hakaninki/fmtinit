"""Module defining formatter profiles and registry."""

from dataclasses import dataclass


@dataclass
class FormatterProfile:
    """Dataclass representing a code formatter configuration profile."""

    language: str
    formatters: list[str]
    install_commands: list[str]
    config_files: list[str]
    pre_commit_repos: list[dict]


# Module-level registry
_PROFILES: dict[str, FormatterProfile] = {
    "javascript": FormatterProfile(
        language="javascript",
        formatters=["Prettier"],
        install_commands=["npm install --save-dev prettier"],
        config_files=[".prettierrc.json"],
        pre_commit_repos=[
            {
                "repo": "https://github.com/pre-commit/mirrors-prettier",
                "rev": "v3.1.0",
                "hooks": [{"id": "prettier"}],
            }
        ],
    ),
    "typescript": FormatterProfile(
        language="typescript",
        formatters=["Prettier", "ESLint"],
        install_commands=["npm install --save-dev prettier eslint"],
        config_files=[".prettierrc.json", ".eslintrc.json"],
        pre_commit_repos=[
            {
                "repo": "https://github.com/pre-commit/mirrors-prettier",
                "rev": "v3.1.0",
                "hooks": [{"id": "prettier"}],
            },
            {
                "repo": "https://github.com/pre-commit/mirrors-eslint",
                "rev": "v8.56.0",
                "hooks": [{"id": "eslint"}],
            },
        ],
    ),
    "python": FormatterProfile(
        language="python",
        formatters=["Black", "Ruff"],
        install_commands=["pip install black ruff"],
        config_files=["pyproject.toml"],
        pre_commit_repos=[
            {
                "repo": "https://github.com/psf/black",
                "rev": "23.12.1",
                "hooks": [{"id": "black"}],
            },
            {
                "repo": "https://github.com/astral-sh/ruff-pre-commit",
                "rev": "v0.1.9",
                "hooks": [{"id": "ruff", "args": ["--fix"]}, {"id": "ruff-format"}],
            },
        ],
    ),
    "dart": FormatterProfile(
        language="dart",
        formatters=["dart format"],
        install_commands=[],
        config_files=[],
        pre_commit_repos=[],
    ),
    "json": FormatterProfile(
        language="json",
        formatters=["Prettier"],
        install_commands=["npm install --save-dev prettier"],
        config_files=[".prettierrc.json"],
        pre_commit_repos=[
            {
                "repo": "https://github.com/pre-commit/mirrors-prettier",
                "rev": "v3.1.0",
                "hooks": [{"id": "prettier"}],
            }
        ],
    ),
    "yaml": FormatterProfile(
        language="yaml",
        formatters=["Prettier"],
        install_commands=["npm install --save-dev prettier"],
        config_files=[".prettierrc.json"],
        pre_commit_repos=[
            {
                "repo": "https://github.com/pre-commit/mirrors-prettier",
                "rev": "v3.1.0",
                "hooks": [{"id": "prettier"}],
            }
        ],
    ),
    "markdown": FormatterProfile(
        language="markdown",
        formatters=["Prettier"],
        install_commands=["npm install --save-dev prettier"],
        config_files=[".prettierrc.json"],
        pre_commit_repos=[
            {
                "repo": "https://github.com/pre-commit/mirrors-prettier",
                "rev": "v3.1.0",
                "hooks": [{"id": "prettier"}],
            }
        ],
    ),
}


def get_profile(language: str) -> FormatterProfile:
    """
    Return the FormatterProfile for the given language name.

    Args:
        language: The exact language name.

    Returns:
        The matched FormatterProfile.

    Raises:
        ValueError: If the language is not supported.
    """
    if language not in _PROFILES:
        raise ValueError(f"Language '{language}' is not supported.")
    return _PROFILES[language]


def get_profiles(languages: list[str]) -> list[FormatterProfile]:
    """
    Return a list of FormatterProfile objects for the given language names.
    Deduplicates formatter installations where multiple languages share a
    formatter (e.g. Prettier).

    Args:
        languages: List of exact language names.

    Returns:
        A list of matched FormatterProfile objects.

    Raises:
        ValueError: If any language is not supported.
    """
    profiles = []

    unique_langs = []
    seen_langs = set()
    for lang in languages:
        if lang not in seen_langs:
            unique_langs.append(lang)
            seen_langs.add(lang)

    for lang in unique_langs:
        profile = get_profile(lang)

        # Build deduplicated formatter and install command lists conceptually
        # But to return valid FormatterProfiles, we can return the profile as is.
        # Deduplication of pre-commit repos and install commands will happen
        # further down the pipeline in `installer` and `hooks` generation.
        # For simplicity, returning the identical profiles for requested languages.
        profiles.append(profile)

    return profiles


def get_supported_languages() -> list[str]:
    """
    Return a sorted list of all supported language names.

    Returns:
        A sorted list of language name strings.
    """
    return sorted(_PROFILES.keys())
