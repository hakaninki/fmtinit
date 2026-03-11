"""Module for installing code formatters."""

import subprocess

from .profiles import FormatterProfile


def install_formatter(profile: FormatterProfile, dry_run: bool = False) -> list[str]:
    """
    Run all install_commands from the given profile.

    Args:
        profile: The formatter profile whose commands to run.
        dry_run: If True, print commands without executing them.

    Returns:
        A list of commands that were run (or would be run in dry_run mode).

    Raises:
        RuntimeError: If any install command exits with non-zero status.
    """
    executed_commands = []
    for cmd in profile.install_commands:
        if dry_run:
            print(f"Would run: {cmd}")
            executed_commands.append(cmd)
        else:
            print(f"Running: {cmd}")
            try:
                subprocess.run(cmd, shell=True, check=True)
                executed_commands.append(cmd)
            except subprocess.CalledProcessError as e:
                raise RuntimeError(f"Command failed: {cmd}") from e
    return executed_commands


def install_formatters(profiles: list[FormatterProfile], dry_run: bool = False) -> None:
    """
    Install all formatters for the given profiles.
    Deduplicates install commands so Prettier is only installed once
    even if multiple languages need it.

    Args:
        profiles: List of profiles to install formatters for.
        dry_run: If True, print commands without executing.
    """
    npm_packages = set()
    pip_packages = set()
    other_commands = []

    for profile in profiles:
        for cmd in profile.install_commands:
            if cmd.startswith("npm install --save-dev "):
                packages = cmd.replace("npm install --save-dev ", "").split()
                npm_packages.update(packages)
            elif cmd.startswith("pip install "):
                packages = cmd.replace("pip install ", "").split()
                pip_packages.update(packages)
            else:
                if cmd not in other_commands:
                    other_commands.append(cmd)

    final_commands = []
    if npm_packages:
        final_commands.append(
            "npm install --save-dev " + " ".join(sorted(npm_packages))
        )
    if pip_packages:
        final_commands.append("pip install " + " ".join(sorted(pip_packages)))
    final_commands.extend(other_commands)

    for cmd in final_commands:
        if dry_run:
            print(f"Would run: {cmd}")
        else:
            print(f"Running: {cmd}")
            try:
                subprocess.run(cmd, shell=True, check=True)
            except subprocess.CalledProcessError as e:
                raise RuntimeError(f"Command failed: {cmd}") from e
