"""Tests for structured-extract-mcp."""
import pytest

class TestImports:
    def test_imports(self):
        try:
            import structured_extract_mcp
        except ImportError as e:
            pytest.fail(f"Import failed: {e}")
