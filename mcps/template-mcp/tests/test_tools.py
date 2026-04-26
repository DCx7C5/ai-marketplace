"""Tests for template-mcp."""
import pytest

class TestImports:
    def test_imports(self):
        try:
            import template_mcp
        except ImportError as e:
            pytest.fail(f"Import failed: {e}")
