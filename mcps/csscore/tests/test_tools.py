"""
Integration tests for CyberSecSuite Core MCP tools.

Tests the tool definitions and FastMCP integration for csscore.
"""

import pytest

from mcp_csscore import __version__


class TestCsscoreImports:
    """Test that csscore module imports correctly."""

    def test_csscore_module_imports(self) -> None:
        """Test that csscore package imports without errors."""
        try:
            import mcp_csscore  # noqa: F401
        except ImportError as e:
            pytest.fail(f"Failed to import mcp_csscore: {e}")

    def test_package_version(self) -> None:
        """Test that package version is accessible and correct."""
        assert __version__ is not None
        assert isinstance(__version__, str)
        assert __version__ == "1.0.0"

    def test_core_functions_exported(self) -> None:
        """Test that all core functions are exported."""
        from mcp_csscore import (
            create_audit_logger,
            discover_assets,
            get_configuration,
            get_marketplace_registry,
            get_scope_context,
        )

        assert callable(get_marketplace_registry)
        assert callable(discover_assets)
        assert callable(get_configuration)
        assert callable(create_audit_logger)
        assert callable(get_scope_context)


class TestCsscoreTools:
    """Test csscore tool definitions."""

    @pytest.mark.unit
    def test_scope_level_enum(self) -> None:
        """Test ScopeLevel enum is properly defined."""
        from mcp_csscore.core import ScopeLevel

        assert hasattr(ScopeLevel, "GLOBAL")
        assert hasattr(ScopeLevel, "APP")
        assert hasattr(ScopeLevel, "PROJECT")
        assert hasattr(ScopeLevel, "RUNTIME")
        assert hasattr(ScopeLevel, "SESSION")

    @pytest.mark.unit
    def test_scope_context_dataclass(self) -> None:
        """Test ScopeContext dataclass structure."""
        from mcp_csscore.core import ScopeContext, ScopeLevel

        scope = ScopeContext(
            scope_level=ScopeLevel.RUNTIME,
            runtime_id="test-runtime",
            worktree_path="/tmp/test",
        )

        assert scope.scope_level == ScopeLevel.RUNTIME
        assert scope.runtime_id == "test-runtime"
        assert scope.worktree_path == "/tmp/test"
        assert scope.project_id is None
        assert scope.session_id is None

    @pytest.mark.unit
    def test_marketplace_registry_dataclass(self) -> None:
        """Test MarketplaceRegistry dataclass structure."""
        from mcp_csscore.core import MarketplaceRegistry

        registry = MarketplaceRegistry(
            mcp_name="test-mcp",
            version="1.0.0",
            dependencies=["csscore"],
            tools=["tool1", "tool2"],
            metadata={"key": "value"},
        )

        assert registry.mcp_name == "test-mcp"
        assert registry.version == "1.0.0"
        assert "csscore" in registry.dependencies
        assert "tool1" in registry.tools
        assert registry.metadata["key"] == "value"
