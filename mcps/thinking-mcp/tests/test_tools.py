"""Tests for thinking-mcp."""
import pytest

class TestImports:
    def test_imports(self):
        try:
            import thinking_mcp
        except ImportError as e:
            pytest.fail(f"Import failed: {e}")
