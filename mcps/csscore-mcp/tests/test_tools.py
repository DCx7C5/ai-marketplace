"""Tests for csscore-mcp."""
import pytest

class TestImports:
    def test_imports(self):
        try:
            import csscore_mcp
        except ImportError as e:
            pytest.fail(f"Import failed: {e}")
