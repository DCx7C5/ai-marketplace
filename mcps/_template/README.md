# MCP Template

A reusable template for Model Context Protocol (MCP) implementations in CyberSecSuite.

## Overview

This is a template repository for creating new MCP servers within the CyberSecSuite ecosystem. It includes:

- Complete Python package structure
- Type-safe async implementations
- Pytest fixtures and test infrastructure
- GitHub Actions CI/CD workflow stub
- MIT License

## Quick Start

### Prerequisites

- Python 3.10+
- `uv` package manager

### Setup

```bash
git clone <repository>
cd _template
uv venv
uv sync --group dev
```

### Running Tests

```bash
uv run pytest tests/ -v --cov=src
```

### Running the MCP Server

```bash
uv run -m mcp_template
```

## Project Structure

```
_template/
├── src/mcp_template/           # Main package
│   ├── __init__.py
│   ├── __main__.py             # MCP server entry point
│   └── tools/                  # Tool implementations
│       └── __init__.py
├── tests/                      # Test suite
│   ├── conftest.py             # Pytest fixtures
│   └── test_tools.py           # Tool tests
├── .github/workflows/          # CI/CD
│   └── ci.yaml                 # GitHub Actions workflow
├── README.md                   # This file
├── LICENSE                     # MIT License
├── MANIFEST.in                 # Package metadata
└── pyproject.toml              # Project configuration
```

## Development

### Code Standards

- **Type Safety:** PEP 484/526 compliance, mypy strict mode
- **Async-First:** All I/O operations must be async
- **Testing:** Minimum 60% coverage, pytest-based
- **Linting:** ruff with zero errors
- **Cryptography:** Ed25519, BLAKE2b, Argon2id, AES-256-GCM only

### Contributing

1. Create feature branch
2. Implement changes with full type hints
3. Add tests (minimum 60% coverage)
4. Run linting and type checking
5. Submit pull request

### Running Quality Checks

```bash
# Format code
uv run ruff format src/ tests/

# Lint
uv run ruff check src/ tests/

# Type checking
uv run mypy src/

# Tests with coverage
uv run pytest tests/ -v --cov=src --cov-report=term-missing
```

## License

This project is licensed under the MIT License - see [LICENSE](LICENSE) file for details.

## Security

For security concerns or vulnerability reports, please contact the CyberSecSuite security team.
