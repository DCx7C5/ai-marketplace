"""Tests for agent-mcp."""
import pytest

class TestImports:
    def test_imports(self):
        try:
            import agent_mcp
        except ImportError as e:
            pytest.fail(f"Import failed: {e}")
