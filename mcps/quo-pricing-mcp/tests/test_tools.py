"""Tests for quo-pricing-mcp."""
import pytest

class TestImports:
    def test_imports(self):
        try:
            import quo_pricing_mcp
        except ImportError as e:
            pytest.fail(f"Import failed: {e}")
