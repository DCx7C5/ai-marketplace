"""Tests for skill-manager-mcp."""
import pytest

class TestImports:
    def test_imports(self):
        try:
            import skill_manager_mcp
        except ImportError as e:
            pytest.fail(f"Import failed: {e}")
