# CyberSecSuite Core MCP (csscore)

**Version:** 1.0.0  
**Status:** Foundation MCP for all externalized MCPs  
**License:** MIT

## Overview

CyberSecSuite Core MCP (`csscore`) is the essential foundation for all 12 externalized MCPs in the CyberSecSuite ecosystem. It provides 5 core utility functions that every MCP depends on:

1. **Marketplace Registry Access** — Query available MCPs, versions, and dependencies
2. **Asset Discovery & Enumeration** — List discovered systems, assets, and targets
3. **Configuration Management** — Read/write/validate CyberSecSuite configuration
4. **Core Logging & Audit** — Structured logging for all MCP operations
5. **Scope & Context Management** — Runtime scope tracking (5-level hierarchy)

## Installation

```bash
uv pip install mcp-csscore
```

Or from source:

```bash
cd /home/daen/Projects/ai-marketplace/mcps/csscore
uv sync
```

## Quick Start

```python
from mcp_csscore import (
    ScopeLevel,
    get_marketplace_registry,
    get_scope_context,
    discover_assets,
)

# Create a scope context
scope = await get_scope_context(
    scope_level=ScopeLevel.SESSION,
    runtime_id="runtime-001",
    worktree_path="/tmp/workspace"
)

# Get marketplace registry
registry = await get_marketplace_registry()

# Discover assets
assets = await discover_assets(scope, asset_type="host")
```

## Core Functions

### `get_marketplace_registry()`
Query available MCPs and their metadata from the marketplace registry.

**Returns:** `Dict[str, Any]` — MCP registry mapping names to metadata

### `discover_assets(scope, asset_type=None)`
Enumerate discovered systems, assets, and targets.

**Args:**
- `scope` (ScopeContext): Execution scope context
- `asset_type` (Optional[str]): Filter by asset type (e.g., 'host', 'network')

**Returns:** `List[Dict[str, Any]]` — Discovered assets with metadata

### `get_configuration(config_key, scope)`
Read and validate CyberSecSuite configuration.

**Args:**
- `config_key` (str): Configuration key path (e.g., 'logging.level')
- `scope` (ScopeContext): Execution scope context

**Returns:** `Optional[Dict[str, Any]]` — Configuration value or None

### `create_audit_logger(service_name, scope)`
Create structured audit logger for MCP operations.

**Args:**
- `service_name` (str): Name of the service creating the logger
- `scope` (ScopeContext): Execution scope context

**Returns:** `logging.Logger` — Configured logger with audit context

### `get_scope_context(scope_level, runtime_id, worktree_path)`
Retrieve or create scope and context tracking.

**Args:**
- `scope_level` (ScopeLevel): Level in scope hierarchy
- `runtime_id` (str): Unique runtime identifier
- `worktree_path` (str): Working tree path for execution

**Returns:** `ScopeContext` — Scope context object with tracking metadata

## Scope Levels

CyberSecSuite uses a 5-level scope hierarchy:

- **GLOBAL** — System-wide configuration
- **APP** — Application-level context
- **PROJECT** — Project-specific scope
- **RUNTIME** — Runtime execution context
- **SESSION** — User/session scope

## Dependencies

All Phase 2-5 MCPs depend on csscore:

- **Phase 2:** forensic-vault, network-layers, threat-intelligence, database-tools
- **Phase 3:** session-management, incident-management, ai-memory
- **Phase 4:** browser-automation, utility-tools, business-tools, network-monitoring
- **Phase 5:** dystopian-actors

**Version Pinning:** All MCPs pin to exactly `csscore==1.0.0`

## Testing

Run unit tests with 100% coverage requirement:

```bash
cd /home/daen/Projects/ai-marketplace/mcps/csscore
uv run pytest tests/ -v --cov=mcp_csscore --cov-fail-under=100
```

## Development

### Running the Server

```bash
python -m mcp_csscore
```

### Running Linting

```bash
ruff check src/
mypy src/ --strict
```

### Running Tests

```bash
pytest tests/ -v --cov=mcp_csscore --cov-report=term-missing
```

## Quality Assurance

Phase 0.75 Exit Gate Checklist:

- ✓ Ruff: zero errors
- ✓ MyPy strict: zero errors
- ✓ Pytest: 100% coverage (not 80%)
- ✓ Module size: ≤2 MB
- ✓ MCP server starts cleanly
- ✓ All 12 Phase 2-5 MCPs can import csscore
- ✓ No circular imports detected

## API Contract

The csscore API is documented in `docs/csscore.md` in the main CyberSecSuite repository.

**Breaking Changes:** Any changes to csscore's public API require updating all dependent MCPs.

## Architecture

```
csscore (Foundation)
  ├── get_marketplace_registry() — Registry access
  ├── discover_assets() — Asset enumeration
  ├── get_configuration() — Config management
  ├── create_audit_logger() — Structured logging
  └── get_scope_context() — Scope tracking
```

**No Domain Logic:** csscore contains ONLY generic utilities, no CyberSecSuite-specific functions.

## Known Issues

None. Phase 0.75 is production-ready.

## License

MIT License — See LICENSE file for details.

---

**Next Phase:** Phase 2 — High-Priority MCP Extraction (forensic-vault, network-layers, threat-intelligence, database-tools)
