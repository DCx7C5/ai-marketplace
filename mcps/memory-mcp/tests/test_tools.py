"""Tests for memory-mcp."""
import pytest

class TestImports:
    def test_imports(self):
        try:
            import memory_mcp
        except ImportError as e:
            pytest.fail(f"Import failed: {e}")
