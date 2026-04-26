"""
Tests for artifact-extraction MCP tools.
"""

import pytest


class TestImports:
    def test_module_imports(self) -> None:
        try:
            import artifact_extraction  # noqa: F401
        except ImportError as e:
            pytest.fail(f"Failed to import: {e}")


class TestTools:

    @pytest.mark.asyncio
    async def test_registry_extractor(self) -> None:
        """Test registry_extractor tool."""
        from artifact_extraction.tools import registry_extractor
        result = await registry_extractor()
        assert isinstance(result, dict)
        assert "status" in result
        assert result["status"] == "ok"

    @pytest.mark.asyncio
    async def test_event_log_parser(self) -> None:
        """Test event_log_parser tool."""
        from artifact_extraction.tools import event_log_parser
        result = await event_log_parser()
        assert isinstance(result, dict)
        assert "status" in result
        assert result["status"] == "ok"

    @pytest.mark.asyncio
    async def test_prefetch_analyzer(self) -> None:
        """Test prefetch_analyzer tool."""
        from artifact_extraction.tools import prefetch_analyzer
        result = await prefetch_analyzer()
        assert isinstance(result, dict)
        assert "status" in result
        assert result["status"] == "ok"

    @pytest.mark.asyncio
    async def test_shortcuts_parser(self) -> None:
        """Test shortcuts_parser tool."""
        from artifact_extraction.tools import shortcuts_parser
        result = await shortcuts_parser()
        assert isinstance(result, dict)
        assert "status" in result
        assert result["status"] == "ok"

    @pytest.mark.asyncio
    async def test_mru_extractor(self) -> None:
        """Test mru_extractor tool."""
        from artifact_extraction.tools import mru_extractor
        result = await mru_extractor()
        assert isinstance(result, dict)
        assert "status" in result
        assert result["status"] == "ok"

    @pytest.mark.asyncio
    async def test_thumbnail_analyzer(self) -> None:
        """Test thumbnail_analyzer tool."""
        from artifact_extraction.tools import thumbnail_analyzer
        result = await thumbnail_analyzer()
        assert isinstance(result, dict)
        assert "status" in result
        assert result["status"] == "ok"

    @pytest.mark.asyncio
    async def test_recycle_bin_parser(self) -> None:
        """Test recycle_bin_parser tool."""
        from artifact_extraction.tools import recycle_bin_parser
        result = await recycle_bin_parser()
        assert isinstance(result, dict)
        assert "status" in result
        assert result["status"] == "ok"

    @pytest.mark.asyncio
    async def test_temp_collector(self) -> None:
        """Test temp_collector tool."""
        from artifact_extraction.tools import temp_collector
        result = await temp_collector()
        assert isinstance(result, dict)
        assert "status" in result
        assert result["status"] == "ok"
