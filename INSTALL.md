# AI Marketplace MCP Installation Guide

This guide provides instructions for installing and configuring all 6 MCPs from the AI Marketplace.

## Prerequisites

- **Python 3.11+** installed on your system
- **uv** package manager (recommended) or pip
- Git (optional, for cloning the repository)

## Quick Start

### Option 1: Install all MCPs (Recommended)

```bash
# Using uv (recommended for fast installation)
uv pip install csscore-mcp canvas-mcp memory-mcp template-mcp playwright-mcp dystopian-crypto-mcp

# Or using pip
pip install csscore-mcp canvas-mcp memory-mcp template-mcp playwright-mcp dystopian-crypto-mcp
```

### Option 2: Install MCPs individually

Install each MCP based on your needs:

#### 1. CyberSecSuite Core MCP (csscore-mcp)
```bash
uv pip install csscore-mcp
python -m csscore_mcp
```

**Description:** Database, cases, findings, intelligence, and vault integration.

**Available Tools (64):**
- Cache operations (lookup, store, analytics, invalidate)
- Health checks and metrics
- Session management
- Database operations
- Intelligence bootstrapping
- Case and finding management
- And more...

See `mcps/csscore-mcp/tools.md` for complete tool list.

---

#### 2. Canvas Visualization (canvas-mcp)
```bash
uv pip install canvas-mcp
python -m canvas_mcp
```

**Description:** Create forensic Obsidian Canvas files for attack graphs, IOC maps, incident timelines, and more.

**Available Tools (6):**
- `canvas_create` - Create canvas with various archetypes
- `canvas_list` - List all canvas files
- `canvas_layout` - Re-layout existing canvas
- `canvas_add_node` - Add nodes to canvas
- `canvas_validate` - Validate canvas structure
- `canvas_archetypes` - List available archetypes

See `mcps/canvas-mcp/tools.md` for details.

---

#### 3. AI Memory (memory-mcp)
```bash
uv pip install memory-mcp
python -m memory_mcp
```

**Description:** Vector memory storage for AI agents.

**Available Tools (3):**
- Vector storage and retrieval
- Memory indexing
- And more...

See `mcps/memory-mcp/tools.md` for details.

---

#### 4. Template Engine (template-mcp)
```bash
uv pip install template-mcp
python -m template_mcp
```

**Description:** Template rendering and processing.

**Available Tools (1):**
- Template rendering operations

See `mcps/template-mcp/tools.md` for details.

---

#### 5. Playwright Browser Automation (playwright-mcp)
```bash
uv pip install playwright-mcp
python -m playwright_mcp
```

**Description:** Headless browser control and automation.

**Available Tools (10):**
- Browser launching and control
- Navigation and interaction
- Content extraction
- And more...

See `mcps/playwright-mcp/tools.md` for details.

---

#### 6. Dystopian Crypto (dystopian-crypto-mcp)
```bash
uv pip install dystopian-crypto-mcp
python -m dystopian_crypto_mcp
```

**Description:** Cryptographic operations.

**Available Tools (1):**
- Cryptographic operations

See `mcps/dystopian-crypto-mcp/tools.md` for details.

---

## Development Installation

### From Source

```bash
cd /path/to/ai-marketplace
cd mcps/<mcp-name>

# Install with dev dependencies
uv pip install -e ".[dev]"

# Run tests
uv run pytest tests/ -v

# Run linting
uv run ruff check src/

# Run type checking
uv run mypy --strict src/
```

### Example: Installing csscore-mcp from source

```bash
cd /home/daen/Projects/ai-marketplace/mcps/csscore-mcp

# Install in editable mode
uv pip install -e .

# Run tests
uv run pytest tests/ -v

# Verify installation
python -m csscore_mcp --help
```

## Configuration

### Environment Variables

Most MCPs support configuration via environment variables:

```bash
# For Canvas MCP
export CYBERSEC_VAULT_PATH="./data/vault"

# Run the MCP
python -m canvas_mcp
```

## Verification

After installation, verify each MCP:

```bash
# Test each MCP
python -m csscore_mcp --help
python -m canvas_mcp --help
python -m memory_mcp --help
python -m template_mcp --help
python -m playwright_mcp --help
python -m dystopian_crypto_mcp --help
```

## Testing

Run the full test suite:

```bash
# From marketplace root
cd /home/daen/Projects/ai-marketplace

# Test all MCPs
for mcp in csscore-mcp canvas-mcp memory-mcp template-mcp playwright-mcp dystopian-crypto-mcp; do
  echo "Testing $mcp..."
  cd mcps/$mcp
  uv run pytest tests/ -v
  cd /home/daen/Projects/ai-marketplace
done
```

## Troubleshooting

### Python Version Issues
```bash
# Check Python version
python --version  # Should be 3.11 or higher

# If using different Python versions
python3.11 -m pip install csscore-mcp
```

### Installation Failures
```bash
# Clear pip cache and retry
pip cache purge
uv pip install csscore-mcp

# Or upgrade pip first
pip install --upgrade pip setuptools wheel
uv pip install csscore-mcp
```

### Import Errors
```bash
# Verify installation
python -c "import csscore_mcp; print(csscore_mcp.__version__)"

# Reinstall if needed
uv pip install --force-reinstall csscore-mcp
```

## Marketplace Index

The marketplace maintains an `index.json` file listing all available MCPs:

```bash
# View marketplace metadata
cat index.json | jq .

# Query specific MCP
cat index.json | jq '.mcps[] | select(.id=="csscore-mcp")'
```

## Next Steps

1. **Read Individual MCP Documentation:**
   - Each MCP directory contains a `README.md` and `tools.md`
   - Check specific MCP directories for detailed usage examples

2. **Explore Tools:**
   - Run `python -m <mcp-name> --help` for each MCP
   - Check `mcps/<mcp-name>/tools.md` for tool documentation

3. **Integration:**
   - Use MCPs as plugins in your applications
   - Combine multiple MCPs for enhanced capabilities

## Support

For issues or questions:
1. Check the README in the specific MCP directory
2. Review the `tools.md` for tool-specific documentation
3. Check test files for usage examples

## Version Information

- **Marketplace Version:** 1.0
- **Python Requirement:** >=3.11
- **Build Backend:** hatchling
- **Package Manager:** uv (recommended) or pip

---

**Last Updated:** 2026-04-26
