"""Tests for the hooks module."""

from pathlib import Path

import pytest
import yaml

from fmtinit.core.hooks import generate_hooks_config, read_hooks, write_hooks
from fmtinit.core.profiles import get_profile


def test_generate_hooks_config_empty():
    assert generate_hooks_config([]) == {"repos": []}


def test_generate_hooks_config_python():
    profile = get_profile("python")
    config = generate_hooks_config([profile])

    assert "repos" in config
    assert len(config["repos"]) == 2
    repos = [repo["repo"] for repo in config["repos"]]
    assert "https://github.com/psf/black" in repos
    assert "https://github.com/astral-sh/ruff-pre-commit" in repos


def test_generate_hooks_config_deduplicates_prettier():
    p1 = get_profile("javascript")
    p2 = get_profile("typescript")

    config = generate_hooks_config([p1, p2])
    assert "repos" in config
    repos = config["repos"]

    # Needs Black, Ruff, ESLint, Prettier -> 4 unique repos max
    # Oh wait, p1 + p2 is just Prettier and ESLint + Prettier
    # Total unique repos: Prettier, ESLint -> 2 total
    assert len(repos) == 2
    repo_urls = [repo["repo"] for repo in repos]
    assert "https://github.com/pre-commit/mirrors-prettier" in repo_urls
    assert "https://github.com/pre-commit/mirrors-eslint" in repo_urls


def test_generate_hooks_config_valid_yaml():
    profile = get_profile("python")
    config = generate_hooks_config([profile])

    # Should not raise exception
    yaml_str = yaml.dump(config, default_flow_style=False, sort_keys=False)
    assert "https://github.com/psf/black" in yaml_str


def test_write_hooks_creates_file(tmp_project: Path):
    write_hooks(tmp_project, [])
    config_path = tmp_project / ".pre-commit-config.yaml"
    assert config_path.exists()
    content = config_path.read_text("utf-8")
    assert "repos" in content


def test_write_hooks_no_overwrite_merges(tmp_project: Path):
    # Setup initial
    write_hooks(tmp_project, [get_profile("python")])

    # Second write with no overwrite
    write_hooks(tmp_project, [get_profile("javascript")], overwrite=False)

    config_path = tmp_project / ".pre-commit-config.yaml"
    content = yaml.safe_load(config_path.read_text("utf-8"))

    repos = [repo["repo"] for repo in content["repos"]]
    assert len(repos) == 3
    assert "https://github.com/psf/black" in repos
    assert "https://github.com/pre-commit/mirrors-prettier" in repos


def test_write_hooks_overwrite_replaces(tmp_project: Path):
    # Setup initial
    write_hooks(tmp_project, [get_profile("python")])

    # Second write with overwrite
    write_hooks(tmp_project, [get_profile("javascript")], overwrite=True)

    config_path = tmp_project / ".pre-commit-config.yaml"
    content = yaml.safe_load(config_path.read_text("utf-8"))

    repos = [repo["repo"] for repo in content["repos"]]
    assert len(repos) == 1
    assert "https://github.com/pre-commit/mirrors-prettier" in repos
    assert "https://github.com/psf/black" not in repos


def test_read_hooks_none_for_missing(tmp_project: Path):
    assert read_hooks(tmp_project) is None


def test_read_hooks_valid_dict(tmp_project: Path):
    write_hooks(tmp_project, [get_profile("python")])
    config = read_hooks(tmp_project)

    assert isinstance(config, dict)
    assert "repos" in config
    assert len(config["repos"]) == 2


def test_read_hooks_invalid_yaml(tmp_project: Path):
    config_path = tmp_project / ".pre-commit-config.yaml"
    config_path.write_text("invalid: yaml: :")

    with pytest.raises(ValueError, match="Invalid YAML"):
        read_hooks(tmp_project)
