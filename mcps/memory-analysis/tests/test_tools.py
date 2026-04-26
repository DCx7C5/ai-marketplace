"""
Tests for memory-analysis MCP tools.
"""

import pytest


class TestImports:
    def test_module_imports(self) -> None:
        try:
            import memory_analysis  # noqa: F401
        except ImportError as e:
            pytest.fail(f"Failed to import: {e}")


class TestTools:

    @pytest.mark.asyncio
    async def test_volatility_runner(self) -> None:
        """Test volatility_runner tool."""
        from memory_analysis.tools import volatility_runner
        result = await volatility_runner()
        assert isinstance(result, dict)
        assert "status" in result
        assert result["status"] == "ok"

    @pytest.mark.asyncio
    async def test_dump_processor(self) -> None:
        """Test dump_processor tool."""
        from memory_analysis.tools import dump_processor
        result = await dump_processor()
        assert isinstance(result, dict)
        assert "status" in result
        assert result["status"] == "ok"

    @pytest.mark.asyncio
    async def test_string_extractor(self) -> None:
        """Test string_extractor tool."""
        from memory_analysis.tools import string_extractor
        result = await string_extractor()
        assert isinstance(result, dict)
        assert "status" in result
        assert result["status"] == "ok"

    @pytest.mark.asyncio
    async def test_registry_analyzer(self) -> None:
        """Test registry_analyzer tool."""
        from memory_analysis.tools import registry_analyzer
        result = await registry_analyzer()
        assert isinstance(result, dict)
        assert "status" in result
        assert result["status"] == "ok"

    @pytest.mark.asyncio
    async def test_handle_enumerator(self) -> None:
        """Test handle_enumerator tool."""
        from memory_analysis.tools import handle_enumerator
        result = await handle_enumerator()
        assert isinstance(result, dict)
        assert "status" in result
        assert result["status"] == "ok"

    @pytest.mark.asyncio
    async def test_network_connections(self) -> None:
        """Test network_connections tool."""
        from memory_analysis.tools import network_connections
        result = await network_connections()
        assert isinstance(result, dict)
        assert "status" in result
        assert result["status"] == "ok"

    @pytest.mark.asyncio
    async def test_process_dumper(self) -> None:
        """Test process_dumper tool."""
        from memory_analysis.tools import process_dumper
        result = await process_dumper()
        assert isinstance(result, dict)
        assert "status" in result
        assert result["status"] == "ok"

    @pytest.mark.asyncio
    async def test_heap_analyzer(self) -> None:
        """Test heap_analyzer tool."""
        from memory_analysis.tools import heap_analyzer
        result = await heap_analyzer()
        assert isinstance(result, dict)
        assert "status" in result
        assert result["status"] == "ok"
