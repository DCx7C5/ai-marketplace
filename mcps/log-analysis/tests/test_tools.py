"""
Tests for log-analysis MCP tools.
"""

import pytest


class TestImports:
    def test_module_imports(self) -> None:
        try:
            import log_analysis  # noqa: F401
        except ImportError as e:
            pytest.fail(f"Failed to import: {e}")


class TestTools:

    @pytest.mark.asyncio
    async def test_log_parser(self) -> None:
        """Test log_parser tool."""
        from log_analysis.tools import log_parser
        result = await log_parser()
        assert isinstance(result, dict)
        assert "status" in result
        assert result["status"] == "ok"

    @pytest.mark.asyncio
    async def test_anomaly_detector(self) -> None:
        """Test anomaly_detector tool."""
        from log_analysis.tools import anomaly_detector
        result = await anomaly_detector()
        assert isinstance(result, dict)
        assert "status" in result
        assert result["status"] == "ok"

    @pytest.mark.asyncio
    async def test_pattern_matcher(self) -> None:
        """Test pattern_matcher tool."""
        from log_analysis.tools import pattern_matcher
        result = await pattern_matcher()
        assert isinstance(result, dict)
        assert "status" in result
        assert result["status"] == "ok"

    @pytest.mark.asyncio
    async def test_timeline_builder(self) -> None:
        """Test timeline_builder tool."""
        from log_analysis.tools import timeline_builder
        result = await timeline_builder()
        assert isinstance(result, dict)
        assert "status" in result
        assert result["status"] == "ok"

    @pytest.mark.asyncio
    async def test_correlation_engine(self) -> None:
        """Test correlation_engine tool."""
        from log_analysis.tools import correlation_engine
        result = await correlation_engine()
        assert isinstance(result, dict)
        assert "status" in result
        assert result["status"] == "ok"

    @pytest.mark.asyncio
    async def test_alert_generator(self) -> None:
        """Test alert_generator tool."""
        from log_analysis.tools import alert_generator
        result = await alert_generator()
        assert isinstance(result, dict)
        assert "status" in result
        assert result["status"] == "ok"

    @pytest.mark.asyncio
    async def test_index_builder(self) -> None:
        """Test index_builder tool."""
        from log_analysis.tools import index_builder
        result = await index_builder()
        assert isinstance(result, dict)
        assert "status" in result
        assert result["status"] == "ok"

    @pytest.mark.asyncio
    async def test_archive_handler(self) -> None:
        """Test archive_handler tool."""
        from log_analysis.tools import archive_handler
        result = await archive_handler()
        assert isinstance(result, dict)
        assert "status" in result
        assert result["status"] == "ok"
