"""Tests for web-search-mcp."""
import pytest

class TestImports:
    def test_imports(self):
        try:
            import web_search_mcp
        except ImportError as e:
            pytest.fail(f"Import failed: {e}")
