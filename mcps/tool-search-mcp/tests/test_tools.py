"""Tests for tool-search-mcp."""
import pytest

class TestImports:
    def test_imports(self):
        try:
            import tool_search_mcp
        except ImportError as e:
            pytest.fail(f"Import failed: {e}")
