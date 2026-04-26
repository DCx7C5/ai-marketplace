"""Tests for tool-toggle-mcp."""
import pytest

class TestImports:
    def test_imports(self):
        try:
            import tool_toggle_mcp
        except ImportError as e:
            pytest.fail(f"Import failed: {e}")
