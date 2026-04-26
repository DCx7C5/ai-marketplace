"""Tests for proxy-mcp."""
import pytest

class TestImports:
    def test_imports(self):
        try:
            import proxy_mcp
        except ImportError as e:
            pytest.fail(f"Import failed: {e}")
