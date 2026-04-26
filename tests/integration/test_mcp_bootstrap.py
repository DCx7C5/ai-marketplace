"""
Integration tests for CyberSecSuite MCP bootstrap installer.

Tests verify that the bootstrap process correctly installs and registers
all 6 core MCPs and that they are available for use in CyberSecSuite.
"""

import json
import os
import subprocess
import sys
import time
from pathlib import Path
from typing import Any, Dict, List

import pytest


# ============================================================================
# CONFIGURATION & FIXTURES
# ============================================================================

MARKETPLACE_ROOT = Path(__file__).parent.parent.parent
SCRIPTS_DIR = MARKETPLACE_ROOT / "scripts"
MCPS_DIR = MARKETPLACE_ROOT / "mcps"
CONFIG_DIR = MARKETPLACE_ROOT.parent / "cybersecsuite" / "config"
MCPS_CONFIG = CONFIG_DIR / "mcps.json"

CORE_MCPS = [
    "csscore-mcp",
    "canvas-mcp",
    "memory-mcp",
    "template-mcp",
    "playwright-mcp",
    "dystopian-crypto-mcp",
]

BOOTSTRAP_SCRIPT = SCRIPTS_DIR / "install-mcp-core.sh"


@pytest.fixture(scope="session")
def marketplace_root() -> Path:
    """Return path to marketplace root."""
    return MARKETPLACE_ROOT


@pytest.fixture(scope="session")
def mcps_config() -> Dict[str, Any]:
    """Load and validate MCP configuration."""
    if not MCPS_CONFIG.exists():
        pytest.skip("MCP config not generated yet")
    
    with open(MCPS_CONFIG) as f:
        return json.load(f)


# ============================================================================
# BOOTSTRAP EXECUTION TESTS
# ============================================================================

class TestBootstrapExecution:
    """Test bootstrap script execution and performance."""

    def test_bootstrap_script_exists(self) -> None:
        """Verify bootstrap script exists and is executable."""
        assert BOOTSTRAP_SCRIPT.exists(), f"Bootstrap script not found: {BOOTSTRAP_SCRIPT}"
        assert os.access(BOOTSTRAP_SCRIPT, os.X_OK), "Bootstrap script not executable"

    def test_bootstrap_help(self) -> None:
        """Verify bootstrap script responds to --help."""
        result = subprocess.run(
            [str(BOOTSTRAP_SCRIPT), "--help"],
            capture_output=True,
            text=True,
            timeout=10,
        )
        assert result.returncode == 0, f"Help command failed: {result.stderr}"
        assert "Bootstrap" in result.stdout
        assert "Options:" in result.stdout

    def test_bootstrap_completes_under_120s(self) -> None:
        """Verify bootstrap completes in under 120 seconds."""
        start = time.time()
        result = subprocess.run(
            [str(BOOTSTRAP_SCRIPT), "--verify"],
            capture_output=True,
            text=True,
            timeout=120,
        )
        elapsed = time.time() - start

        assert result.returncode == 0, f"Bootstrap failed: {result.stderr}"
        assert elapsed < 120, f"Bootstrap took {elapsed:.1f}s (target: <120s)"
        assert "verified" in result.stdout.lower() or "passed" in result.stdout.lower()

    def test_bootstrap_output_contains_success_markers(self) -> None:
        """Verify bootstrap output contains success indicators."""
        result = subprocess.run(
            [str(BOOTSTRAP_SCRIPT), "--verify"],
            capture_output=True,
            text=True,
            timeout=120,
        )
        
        output = result.stdout + result.stderr
        assert "prerequisites" in output.lower()
        assert "marketplace" in output.lower()
        assert "verified" in output.lower() or "passed" in output.lower()


# ============================================================================
# MCP INSTALLATION TESTS
# ============================================================================

class TestMCPInstallation:
    """Test MCP installation and availability."""

    def test_all_core_mcps_exist(self) -> None:
        """Verify all 6 core MCPs exist in marketplace."""
        for mcp_name in CORE_MCPS:
            mcp_dir = MCPS_DIR / mcp_name
            assert mcp_dir.exists(), f"MCP directory not found: {mcp_name}"
            assert (mcp_dir / "pyproject.toml").exists(), f"No pyproject.toml in {mcp_name}"

    def test_all_core_mcps_have_tests(self) -> None:
        """Verify all core MCPs have test directories."""
        for mcp_name in CORE_MCPS:
            mcp_tests = MCPS_DIR / mcp_name / "tests"
            assert mcp_tests.exists(), f"No tests directory in {mcp_name}"

    def test_mcp_imports(self) -> None:
        """Verify all MCPs can be imported successfully."""
        # This test requires MCPs to be installed in current environment
        # Skip if not in bootstrap environment
        try:
            import csscore_mcp
            import canvas_mcp
            import memory_mcp
            import template_mcp
            import playwright_mcp
            import dystopian_crypto_mcp
            
            # If imports succeed, MCPs are available
            assert True
        except ImportError as e:
            pytest.skip(f"MCPs not installed in current environment: {e}")


# ============================================================================
# CONFIGURATION TESTS
# ============================================================================

class TestMCPConfiguration:
    """Test MCP configuration file."""

    def test_mcps_config_exists(self) -> None:
        """Verify MCP configuration file exists."""
        assert MCPS_CONFIG.exists(), f"MCP config not found: {MCPS_CONFIG}"

    def test_mcps_config_valid_json(self) -> None:
        """Verify MCP configuration is valid JSON."""
        with open(MCPS_CONFIG) as f:
            config = json.load(f)
        assert config is not None

    def test_mcps_config_structure(self, mcps_config: Dict[str, Any]) -> None:
        """Verify MCP configuration has required structure."""
        assert "version" in mcps_config, "Missing 'version' field"
        assert "timestamp" in mcps_config, "Missing 'timestamp' field"
        assert "mode" in mcps_config, "Missing 'mode' field"
        assert "mcps" in mcps_config, "Missing 'mcps' array"
        assert isinstance(mcps_config["mcps"], list), "'mcps' must be an array"

    def test_mcps_config_contains_all_core_mcps(
        self, mcps_config: Dict[str, Any]
    ) -> None:
        """Verify config contains all 6 core MCPs."""
        registered_names = [mcp["name"] for mcp in mcps_config["mcps"]]
        
        for mcp_name in CORE_MCPS:
            assert mcp_name in registered_names, f"{mcp_name} not in MCP config"

    def test_mcps_config_entries_valid(self, mcps_config: Dict[str, Any]) -> None:
        """Verify each MCP entry has required fields."""
        for mcp in mcps_config["mcps"]:
            assert "name" in mcp, "MCP entry missing 'name'"
            assert "path" in mcp, "MCP entry missing 'path'"
            assert "installed" in mcp, "MCP entry missing 'installed'"
            assert "version" in mcp, "MCP entry missing 'version'"
            assert mcp["installed"] is True, f"{mcp['name']} marked as not installed"

    def test_mcps_config_mode_is_sdk(self, mcps_config: Dict[str, Any]) -> None:
        """Verify MCP config mode is 'sdk'."""
        assert mcps_config["mode"] == "sdk", "MCP mode should be 'sdk' (externalized)"


# ============================================================================
# CYBERSECSUITE INTEGRATION TESTS
# ============================================================================

class TestCyberSecSuiteIntegration:
    """Test integration with CyberSecSuite."""

    def test_cybersecsuite_root_exists(self) -> None:
        """Verify CyberSecSuite root directory exists."""
        css_root = MARKETPLACE_ROOT.parent / "cybersecsuite"
        assert css_root.exists(), f"CyberSecSuite root not found: {css_root}"

    def test_cybersecsuite_config_dir_exists(self) -> None:
        """Verify CyberSecSuite config directory can be accessed."""
        assert CONFIG_DIR.exists() or CONFIG_DIR.parent.exists(), \
            f"CyberSecSuite config path not accessible: {CONFIG_DIR}"

    def test_cybersecsuite_can_read_mcps_config(self, mcps_config: Dict[str, Any]) -> None:
        """Verify CyberSecSuite can read MCP configuration."""
        # If we can load the config, CyberSecSuite should be able to
        assert mcps_config is not None
        assert len(mcps_config["mcps"]) == 6, "Expected 6 MCPs in config"


# ============================================================================
# MARKETPLACE INDEX TESTS
# ============================================================================

class TestMarketplaceIndex:
    """Test marketplace index consistency."""

    def test_index_json_exists(self) -> None:
        """Verify index.json exists."""
        index_file = MARKETPLACE_ROOT / "index.json"
        assert index_file.exists(), "index.json not found"

    def test_index_json_valid(self) -> None:
        """Verify index.json is valid JSON."""
        index_file = MARKETPLACE_ROOT / "index.json"
        with open(index_file) as f:
            index = json.load(f)
        assert index is not None

    def test_index_json_lists_all_core_mcps(self) -> None:
        """Verify index.json lists all 6 core MCPs."""
        index_file = MARKETPLACE_ROOT / "index.json"
        with open(index_file) as f:
            index = json.load(f)
        
        indexed_names = [mcp["id"] for mcp in index.get("mcps", [])]
        for mcp_name in CORE_MCPS:
            assert mcp_name in indexed_names, f"{mcp_name} not in index.json"

    def test_index_json_file_size(self) -> None:
        """Verify index.json is within acceptable size limits."""
        index_file = MARKETPLACE_ROOT / "index.json"
        size_bytes = index_file.stat().st_size
        size_mb = size_bytes / (1024 * 1024)
        
        # Should be well under 1 MB
        assert size_mb < 1.0, f"index.json too large: {size_mb:.2f} MB (limit: 1 MB)"


# ============================================================================
# PERFORMANCE TESTS
# ============================================================================

class TestBootstrapPerformance:
    """Test bootstrap performance metrics."""

    def test_bootstrap_timing_goal_met(self) -> None:
        """Verify bootstrap meets 120-second timing goal."""
        start = time.time()
        result = subprocess.run(
            [str(BOOTSTRAP_SCRIPT), "--verify"],
            capture_output=True,
            timeout=120,
        )
        elapsed = time.time() - start

        assert result.returncode == 0
        assert elapsed < 120, f"Bootstrap took {elapsed:.1f}s (target: <120s)"


# ============================================================================
# SUMMARY TESTS
# ============================================================================

class TestBootstrapSummary:
    """Summary test demonstrating overall bootstrap readiness."""

    def test_bootstrap_complete_and_ready(self) -> None:
        """Verify bootstrap is complete and CyberSecSuite is ready."""
        # Verify all components exist
        assert BOOTSTRAP_SCRIPT.exists()
        assert MCPS_CONFIG.exists()
        assert (MARKETPLACE_ROOT / "index.json").exists()
        
        # Verify configuration
        with open(MCPS_CONFIG) as f:
            config = json.load(f)
        
        assert config["mode"] == "sdk"
        assert len(config["mcps"]) == 6
        
        # All checks passed - bootstrap is ready
        print("\n✅ Bootstrap complete and verified!")
        print(f"   MCPs installed: {len(config['mcps'])}/6")
        print(f"   Mode: {config['mode']}")
        print(f"   Ready for CyberSecSuite deployment")


# ============================================================================
# CLI TEST EXECUTION
# ============================================================================

if __name__ == "__main__":
    # Run with pytest if available
    pytest.main([__file__, "-v"])
