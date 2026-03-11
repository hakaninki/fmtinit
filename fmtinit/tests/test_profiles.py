"""Tests for the profiles module."""

import pytest

from fmtinit.core.profiles import get_profile, get_profiles


def test_get_profile_python():
    profile = get_profile("python")
    assert profile.language == "python"
    assert "Black" in profile.formatters
    assert "Ruff" in profile.formatters


def test_get_profile_javascript():
    profile = get_profile("javascript")
    assert profile.language == "javascript"
    assert "Prettier" in profile.formatters


def test_get_profile_typescript():
    profile = get_profile("typescript")
    assert profile.language == "typescript"
    assert "Prettier" in profile.formatters
    assert "ESLint" in profile.formatters


def test_get_profile_dart():
    profile = get_profile("dart")
    assert profile.language == "dart"
    assert "dart format" in profile.formatters


def test_get_profile_json_yaml_markdown():
    for lang in ["json", "yaml", "markdown"]:
        profile = get_profile(lang)
        assert profile.language == lang
        assert "Prettier" in profile.formatters


def test_get_profile_unknown_raises():
    with pytest.raises(ValueError, match="not supported"):
        get_profile("unknown")


def test_get_profile_case_sensitive():
    with pytest.raises(ValueError, match="not supported"):
        get_profile("PYTHON")


def test_get_profiles_multiple():
    profiles = get_profiles(["python", "javascript"])
    assert len(profiles) == 2
    assert profiles[0].language == "python"
    assert profiles[1].language == "javascript"


def test_get_profiles_empty():
    assert get_profiles([]) == []


def test_get_profiles_invalid_raises():
    with pytest.raises(ValueError, match="not supported"):
        get_profiles(["python", "invalid"])


def test_all_supported_have_pre_commit_repos():
    # Only dart doesn't have pre-commit repos natively in this setup
    # wait let's check profile
    langs = ["python", "javascript", "typescript", "json", "yaml", "markdown"]
    for lang in langs:
        profile = get_profile(lang)
        assert len(profile.pre_commit_repos) > 0


def test_profile_has_all_fields():
    profile = get_profile("python")
    assert hasattr(profile, "language")
    assert hasattr(profile, "formatters")
    assert hasattr(profile, "install_commands")
    assert hasattr(profile, "config_files")
    assert hasattr(profile, "pre_commit_repos")

    assert isinstance(profile.language, str)
    assert isinstance(profile.formatters, list)
    assert isinstance(profile.install_commands, list)
    assert isinstance(profile.config_files, list)
    assert isinstance(profile.pre_commit_repos, list)
