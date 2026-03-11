# fmtinit-formatter

![Python](https://img.shields.io/badge/python-3.11+-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)

## Overview

`fmtinit` is a smart command-line interface (CLI) tool designed to bootstrap code formatting for multi-language projects. It automatically detects programming languages, installs appropriate formatters, and configures tools like Prettier, Black, Ruff, and pre-commit hooks. The goal is to standardize code style across diverse projects with minimal manual setup.

## Features

*   **Language Detection:** Automatically identifies programming languages present in a project.
*   **Formatter Installation:** Installs recommended formatters (e.g., Prettier, Black, Ruff) based on detected languages.
*   **Configuration Generation:** Creates configuration files (`.editorconfig`, `.prettierrc`, `pyproject.toml`, `.pre-commit-config.yaml`) tailored to project needs.
*   **Pre-commit Hook Setup:** Integrates formatters into pre-commit hooks to enforce consistent styling.
*   **Extensible Profiles:** Supports custom formatter profiles for different language ecosystems.
*   **Doctor Command:** Provides diagnostics to check the formatting setup.
*   **Add Language Support:** Allows adding formatting for new languages to an existing setup.

## Tech Stack

| Layer          | Technology                               |
| :------------- | :--------------------------------------- |
| CLI Framework  | Python (Typer, Rich)                     |
| Core Logic     | Python                                   |
| Package Mgmt   | Python (pip, setuptools), JavaScript (npm) |
| Formatting     | Black, Ruff, Prettier                    |
| Configuration  | YAML, TOML, JSON, INI                    |
| CI/CD          | GitHub Actions                           |

## Project Structure

```
fmtinit-formatter/
├── fmtinit/
│   ├── src/
│   │   ├── fmtinit/
│   │   │   ├── commands/
│   │   │   │   ├── __init__.py
│   │   │   │   ├── add.py
│   │   │   │   ├── doctor.py
│   │   │   │   ├── init.py
│   │   │   │   └── scan.py
│   │   │   ├── core/
│   │   │   │   ├── __init__.py
│   │   │   │   ├── detector.py
│   │   │   │   ├── hooks.py
│   │   │   │   ├── installer.py
│   │   │   │   ├── profiles.py
│   │   │   │   ├── state.py
│   │   │   │   └── writer.py
│   │   │   ├── templates/
│   │   │   │   ├── editorconfig.tpl
│   │   │   │   ├── precommit.yaml.tpl
│   │   │   │   └── prettier.json.tpl
│   │   │   ├── __init__.py
│   │   │   ├── cli.py
│   │   │   └── main.py
│   │   └── fmtinit.egg-info/
│   │       ├── dependency_links.txt
│   │       ├── entry_points.txt
│   │       ├── PKG-INFO
│   │       ├── requires.txt
│   │       ├── SOURCES.txt
│   │       └── top_level.txt
│   ├── tests/
│   │   ├── __init__.py
│   │   ├── conftest.py
│   │   ├── test_cli.py
│   │   ├── test_detector.py
│   │   ├── test_hooks.py
│   │   ├── test_profiles.py
│   │   └── test_writer.py
│   ├── .gitignore
│   ├── CHANGELOG.md
│   ├── LICENSE
│   ├── pyproject.toml
│   └── README.md
├── package-lock.json
└── package.json
```

## Getting Started

### Prerequisites

*   Python 3.11 or higher
*   pip (Python package installer)
*   npm (Node.js package manager, for JavaScript/TypeScript projects)
*   git (for pre-commit hooks)

### Installation

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/your-username/fmtinit-formatter.git
    cd fmtinit-formatter/fmtinit
    ```

2.  **Install the package:**
    ```bash
    pip install .
    ```
    For development, install with dev dependencies:
    ```bash
    pip install ".[dev]"
    ```

3.  **Verify installation:**
    ```bash
    fmtinit --version
    ```

### Environment Setup

No specific environment variables are required for basic operation. `fmtinit` primarily interacts with local project files and system-wide package managers.

## Usage

### Initializing a Project

To set up formatting for a new or existing project, navigate to the project root and run:

```bash
fmtinit init
```

This command will:
1.  Detect languages in your project.
2.  Suggest and install relevant formatters (e.g., `prettier` via `npm`, `black` via `pip`).
3.  Generate configuration files (`.editorconfig`, `.prettierrc.json`, `pyproject.toml` sections).
4.  Set up `pre-commit` hooks.

### Adding Language Support

If you add new languages to your project later, you can update the formatting setup:

```bash
fmtinit add <language>
# Example: fmtinit add javascript
```

### Scanning for Issues

To scan your project for formatting issues without fixing them:

```bash
fmtinit scan
```

### Diagnosing Setup

To check the health of your formatting setup and identify potential problems:

```bash
fmtinit doctor
```

## API Reference

This project is a CLI tool and does not expose a public API in the traditional sense. Its interface is through the command-line arguments and options.

## Architecture

```mermaid
graph TD
    A[User CLI] --> B[fmtinit CLI]
    B --> C[Command Router]
    C --> D[Init Command]
    C --> E[Add Command]
    C --> F[Scan Command]
    C --> G[Doctor Command]
    D --> H[Language Detector]
    D --> I[Formatter Installer]
    D --> J[Config Writer]
    D --> K[Hook Generator]
    I --> L[npm]
    I --> M[pip]
    J --> N[Template Engine]
    H --> O[Project Files]
    K --> P[Pre commit]
```

## Contributing

We welcome contributions! Please follow these steps:

1.  Fork the repository.
2.  Create a new branch for your feature or bug fix.
3.  Make your changes and ensure tests pass.
4.  Write clear, concise commit messages.
5.  Submit a pull request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
