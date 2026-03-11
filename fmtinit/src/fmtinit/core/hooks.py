"""
Pre-commit hook generation and file writing module.

Note: pyyaml may need to be added to pyproject.toml dependencies.
"""

from pathlib import Path

import yaml


def generate_hooks_config(profiles: list) -> dict:
    """
    Generate a complete pre-commit config dict from a list of FormatterProfile objects.

    Collect all pre_commit_repos entries from all profiles.
    Deduplicate by repo URL (same repo should not appear twice).

    Args:
        profiles: List of FormatterProfile objects.

    Returns:
        A dictionary containing a "repos" list.
    """
    repos = []
    seen_repos = set()

    for profile in profiles:
        for repo_config in profile.pre_commit_repos:
            repo_url = repo_config.get("repo")
            if repo_url and repo_url not in seen_repos:
                seen_repos.add(repo_url)
                repos.append(repo_config)

    return {"repos": repos}


def write_hooks(project_path: Path, profiles: list, overwrite: bool = False) -> None:
    """
    Generate .pre-commit-config.yaml in project_path from the given profiles.

    If .pre-commit-config.yaml does not exist: create it.
    If .pre-commit-config.yaml already exists and overwrite=False: merge new repos into
    the existing file, deduplicating by repo URL. Do not remove existing repos.
    If overwrite=True: replace the file entirely.

    The written YAML must be valid and parseable by pre-commit.
    Use yaml.dump with default_flow_style=False for clean output.

    Args:
        project_path: Path to the project root directory.
        profiles: List of FormatterProfile objects.
        overwrite: If True, replace the file entirely.
    """
    config_path = project_path / ".pre-commit-config.yaml"
    new_config = generate_hooks_config(profiles)

    if not overwrite and config_path.exists():
        existing_config = read_hooks(project_path)
        if existing_config:
            existing_repos = existing_config.get("repos", [])
            seen_urls = {
                repo.get("repo")
                for repo in existing_repos
                if isinstance(repo, dict) and "repo" in repo
            }

            merged_repos = list(existing_repos)
            for repo in new_config.get("repos", []):
                if repo.get("repo") not in seen_urls:
                    merged_repos.append(repo)
                    seen_urls.add(repo.get("repo"))

            final_config = {"repos": merged_repos}
        else:
            final_config = new_config
    else:
        final_config = new_config

    with open(config_path, "w", encoding="utf-8") as file:
        yaml.dump(final_config, file, default_flow_style=False, sort_keys=False)


def read_hooks(project_path: Path) -> dict | None:
    """
    Read and parse .pre-commit-config.yaml from project_path.

    Returns None if the file does not exist.
    Raises ValueError if the file exists but is not valid YAML.

    Args:
        project_path: Path to the project root directory.

    Returns:
        The parsed YAML configuration as a dictionary, or None if missing.

    Raises:
        ValueError: If the file is not valid YAML.
    """
    config_path = project_path / ".pre-commit-config.yaml"
    if not config_path.exists():
        return None

    try:
        with open(config_path, "r", encoding="utf-8") as file:
            content = yaml.safe_load(file)
            return content if isinstance(content, dict) else {}
    except yaml.YAMLError as e:
        raise ValueError(f"Invalid YAML in .pre-commit-config.yaml: {e}")
