"""Tests for dystopian-crypto-mcp."""
import pytest

class TestImports:
    def test_imports(self):
        try:
            import dystopian_crypto_mcp
        except ImportError as e:
            pytest.fail(f"Import failed: {e}")
