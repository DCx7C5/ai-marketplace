"""
Tests for binary-analysis MCP tools.
"""

import pytest


class TestImports:
    def test_module_imports(self) -> None:
        try:
            import binary_analysis  # noqa: F401
        except ImportError as e:
            pytest.fail(f"Failed to import: {e}")


class TestTools:

    @pytest.mark.asyncio
    async def test_disassembler(self) -> None:
        """Test disassembler tool."""
        from binary_analysis.tools import disassembler
        result = await disassembler()
        assert isinstance(result, dict)
        assert "status" in result
        assert result["status"] == "ok"

    @pytest.mark.asyncio
    async def test_decompiler(self) -> None:
        """Test decompiler tool."""
        from binary_analysis.tools import decompiler
        result = await decompiler()
        assert isinstance(result, dict)
        assert "status" in result
        assert result["status"] == "ok"

    @pytest.mark.asyncio
    async def test_function_analyzer(self) -> None:
        """Test function_analyzer tool."""
        from binary_analysis.tools import function_analyzer
        result = await function_analyzer()
        assert isinstance(result, dict)
        assert "status" in result
        assert result["status"] == "ok"

    @pytest.mark.asyncio
    async def test_string_finder(self) -> None:
        """Test string_finder tool."""
        from binary_analysis.tools import string_finder
        result = await string_finder()
        assert isinstance(result, dict)
        assert "status" in result
        assert result["status"] == "ok"

    @pytest.mark.asyncio
    async def test_import_resolver(self) -> None:
        """Test import_resolver tool."""
        from binary_analysis.tools import import_resolver
        result = await import_resolver()
        assert isinstance(result, dict)
        assert "status" in result
        assert result["status"] == "ok"

    @pytest.mark.asyncio
    async def test_xref_generator(self) -> None:
        """Test xref_generator tool."""
        from binary_analysis.tools import xref_generator
        result = await xref_generator()
        assert isinstance(result, dict)
        assert "status" in result
        assert result["status"] == "ok"

    @pytest.mark.asyncio
    async def test_control_flow_grapher(self) -> None:
        """Test control_flow_grapher tool."""
        from binary_analysis.tools import control_flow_grapher
        result = await control_flow_grapher()
        assert isinstance(result, dict)
        assert "status" in result
        assert result["status"] == "ok"

    @pytest.mark.asyncio
    async def test_entropy_calculator(self) -> None:
        """Test entropy_calculator tool."""
        from binary_analysis.tools import entropy_calculator
        result = await entropy_calculator()
        assert isinstance(result, dict)
        assert "status" in result
        assert result["status"] == "ok"
