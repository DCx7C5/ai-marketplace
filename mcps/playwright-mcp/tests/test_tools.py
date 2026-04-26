"""Tests for playwright-mcp."""
import pytest

class TestImports:
    def test_imports(self):
        try:
            import playwright_mcp
        except ImportError as e:
            pytest.fail(f"Import failed: {e}")
