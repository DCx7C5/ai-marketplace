# Bootstrap Installation Guide

**Last Updated:** 2026-04-27  
**Status:** ✅ Production Ready

## Overview

This guide explains how to bootstrap CyberSecSuite with the 6 core MCPs (Model Context Providers) from the AI Marketplace. The bootstrap process is fully automated and designed to complete in under 120 seconds.

## What Gets Installed

The bootstrap installer (`install-mcp-core.sh`) installs the following MCPs:

| MCP | Modules | Purpose |
|-----|---------|---------|
| **csscore-mcp** | 22 | Core infrastructure (database, cases, findings, vault, session) |
| **canvas-mcp** | 1 | Forensic visualization |
| **memory-mcp** | 1 | Vector memory storage |
| **template-mcp** | 1 | Template rendering engine |
| **playwright-mcp** | 1 | Browser automation (headless) |
| **dystopian-crypto-mcp** | 1 | Cryptographic operations |

**Total:** 6 MCPs, 27 modules, 85+ tools

## Prerequisites

Before running the bootstrap script, ensure you have:

- **Bash** 4.0 or later
- **Python** 3.11 or later
- **uv** package manager (0.1.0+)
- **jq** JSON processor
- **curl** (for health checks)
- **docker** & **docker-compose** (for running CyberSecSuite)

### Quick Check

```bash
# Verify prerequisites
bash --version | head -1
python3 --version
uv --version
jq --version
docker --version
docker-compose --version
```

## Installation Steps

### Step 1: Navigate to AI Marketplace

```bash
cd /home/daen/Projects/ai-marketplace
```

### Step 2: Run Bootstrap Installer

```bash
bash scripts/install-mcp-core.sh
```

**Expected Output:**
```
╔════════════════════════════════════════════════════════════════╗
║        CyberSecSuite Core MCP Bootstrap Installer            ║
║   Installing 6 Foundation MCPs (csscore + specialized)        ║
╚════════════════════════════════════════════════════════════════╝

[INFO] Checking prerequisites...
[✓] All prerequisites met
[INFO] Verifying marketplace structure...
[✓] Marketplace structure valid
[INFO] Installing 6 core MCPs...
[INFO] Installing csscore-mcp...
[✓] Installed csscore-mcp
...
[✓] All MCPs installed successfully
[✓] All MCPs verified successfully
[✓] MCP registry created at /path/to/cybersecsuite/config/mcps.json

╔════════════════════════════════════════════════════════════════╗
║           Bootstrap Complete! Ready for CyberSecSuite         ║
║                 Duration: Xs (target: <120s)                  ║
╚════════════════════════════════════════════════════════════════╝
```

**Duration:** Typically 3-5 seconds (well under 120s target)

### Step 3: Start CyberSecSuite

```bash
cd /home/daen/Projects/cybersecsuite
docker-compose up -d
```

### Step 4: Verify Health Check

```bash
# Wait for services to start
sleep 10

# Check dashboard health
curl http://localhost:8000/health

# Expected response:
# {"status":"ok","version":"1.0.0","mcps":"6","tools":"85"}
```

### Step 5: Test MCP Availability

```bash
# Test csscore-mcp
python3 -c "from csscore_mcp import tools; print('✓ csscore-mcp ready')"

# Test other MCPs
python3 -c "
from canvas_mcp import tools
from memory_mcp import tools
from template_mcp import tools
from playwright_mcp import tools
from dystopian_crypto_mcp import tools
print('✓ All MCPs ready')
"
```

## Advanced Usage

### Verify Only (Without Installation)

If MCPs are already installed, verify they're working:

```bash
bash scripts/install-mcp-core.sh --verify
```

### Cleanup Virtual Environments

To remove all installed virtual environments and start fresh:

```bash
bash scripts/install-mcp-core.sh --cleanup
```

Then run the full bootstrap again:

```bash
bash scripts/install-mcp-core.sh
```

### Debug Mode

Enable verbose output for troubleshooting:

```bash
DEBUG=true bash scripts/install-mcp-core.sh
```

## Troubleshooting

### Issue: "uv: command not found"

**Solution:** Install uv package manager:
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
export PATH="$HOME/.cargo/bin:$PATH"
```

### Issue: "jq: command not found"

**Solution:** Install jq:
```bash
# Ubuntu/Debian
sudo apt-get install jq

# macOS
brew install jq
```

### Issue: "Python 3.11+ required"

**Solution:** Upgrade Python:
```bash
# Ubuntu/Debian
sudo apt-get install python3.11

# macOS
brew install python@3.11
```

### Issue: Bootstrap Takes > 120 seconds

**Possible causes:**
- Slow internet connection (downloading dependencies)
- Low system resources
- Disk I/O bottleneck

**Solution:** Ensure you have:
- Stable internet connection (>5 Mbps)
- At least 2 GB free disk space
- 2+ GB RAM available

### Issue: MCP Import Fails

**Solution:** Verify installation:
```bash
bash scripts/install-mcp-core.sh --verify
```

If verification fails, cleanup and reinstall:
```bash
bash scripts/install-mcp-core.sh --cleanup
bash scripts/install-mcp-core.sh
```

### Issue: CyberSecSuite Won't Start

**Solution:** Check Docker status and logs:
```bash
# Check service health
docker-compose ps

# View logs
docker-compose logs cybersec-dashboard

# Restart services
docker-compose restart cybersec-dashboard
docker-compose restart cybersec-postgres
```

## Configuration

### MCP Registry

After bootstrap, CyberSecSuite reads MCP configuration from:

```
/home/daen/Projects/cybersecsuite/config/mcps.json
```

**Example Configuration:**
```json
{
  "version": "1.0",
  "timestamp": "2026-04-27T00:04:49+02:00",
  "mode": "sdk",
  "mcps": [
    {
      "name": "csscore-mcp",
      "path": "/home/daen/Projects/ai-marketplace/mcps/csscore-mcp",
      "installed": true,
      "version": "1.0.0"
    },
    ...
  ]
}
```

**Configuration Fields:**
- `version`: Schema version (currently 1.0)
- `timestamp`: When MCPs were registered
- `mode`: Operating mode ("sdk" = externalized MCPs)
- `mcps`: Array of installed MCPs with paths and versions

### SDK Mode vs. Legacy Mode

**SDK Mode (Recommended - Current):**
- MCPs run as separate processes
- Isolated environments
- Better resource management
- Easier to update individual MCPs

**Legacy Mode (Deprecated):**
- MCPs run in-process
- Tighter coupling
- Not recommended for new installations

## Verification Checklist

After bootstrap, verify:

- [ ] All 6 MCPs installed (`scripts/install-mcp-core.sh --verify`)
- [ ] CyberSecSuite dashboard accessible (http://localhost:8000)
- [ ] Health check endpoint returns OK
- [ ] All MCP imports successful
- [ ] Bootstrap duration < 120 seconds
- [ ] No error messages in logs

## Performance Metrics

**Typical Bootstrap Performance:**

| Stage | Duration | Target |
|-------|----------|--------|
| Prerequisites check | <1s | <5s |
| Marketplace validation | <1s | <5s |
| MCP installation | 1-3s | <60s |
| MCP verification | <1s | <30s |
| MCP registration | <1s | <5s |
| **Total** | **3-5s** | **<120s** |

## Next Steps

After successful bootstrap:

1. **Configure Workspace:** `.css/` directory in current project
2. **Install Skills:** Via marketplace installer or CLI
3. **Load Agents:** Per agent configuration files
4. **Run Tasks:** Use CyberSecSuite CLI or dashboard

## Support & Documentation

- **Main Docs:** `docs/index.md`
- **MCP Documentation:** `mcps/*/README.md`
- **Tool Reference:** `mcps/*/tools.md`
- **Marketplace:** `index.json`
- **Installation Guide:** `INSTALL.md`

## Summary

✅ **Bootstrap Complete!**

Your CyberSecSuite instance is now equipped with:
- **6 production-ready MCPs**
- **85+ enterprise tools**
- **Comprehensive documentation**
- **Sub-5-second installation**

Ready to use. Happy securing! 🚀
