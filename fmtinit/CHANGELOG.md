# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.1.0] - 2025-01-01

### Added
- `fmtinit init --langs` command to initialize formatters for selected languages
- `fmtinit add <language>` command to incrementally add a new language
- `fmtinit scan` command to detect languages used in a project
- `fmtinit doctor` command to check for missing formatter configurations
- Support for JavaScript, TypeScript, Python, Dart, JSON, YAML, and Markdown
- Formatter profiles: Prettier, ESLint, Black, Ruff, dart format
- Pre-commit hook generation via `.pre-commit-config.yaml`
- Idempotent config file writing — existing files are never overwritten
- Project state tracking via `.fmtinit-state.json`
- `--dry-run` flag for `init` and `add` commands
- `--path` option to target any directory
