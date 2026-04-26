"""Tests for canvas-mcp."""
import pytest

class TestImports:
    def test_imports(self):
        try:
            import canvas_mcp
        except ImportError as e:
            pytest.fail(f"Import failed: {e}")
