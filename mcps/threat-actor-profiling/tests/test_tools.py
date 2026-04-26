"""
Tests for dystopian-actors MCP tools.
"""

import pytest


class TestImports:
    def test_module_imports(self) -> None:
        try:
            import dystopian_actors  # noqa: F401
        except ImportError as e:
            pytest.fail(f"Failed to import: {e}")


class TestTools:

    @pytest.mark.asyncio
    async def test_threat_actor_profiler(self) -> None:
        """Test threat_actor_profiler tool."""
        from dystopian_actors.tools import threat_actor_profiler
        result = await threat_actor_profiler()
        assert isinstance(result, dict)
        assert "status" in result
        assert result["status"] == "ok"

    @pytest.mark.asyncio
    async def test_campaign_analyzer(self) -> None:
        """Test campaign_analyzer tool."""
        from dystopian_actors.tools import campaign_analyzer
        result = await campaign_analyzer()
        assert isinstance(result, dict)
        assert "status" in result
        assert result["status"] == "ok"

    @pytest.mark.asyncio
    async def test_ioc_correlator(self) -> None:
        """Test ioc_correlator tool."""
        from dystopian_actors.tools import ioc_correlator
        result = await ioc_correlator()
        assert isinstance(result, dict)
        assert "status" in result
        assert result["status"] == "ok"

    @pytest.mark.asyncio
    async def test_ttps_mapper(self) -> None:
        """Test ttps_mapper tool."""
        from dystopian_actors.tools import ttps_mapper
        result = await ttps_mapper()
        assert isinstance(result, dict)
        assert "status" in result
        assert result["status"] == "ok"

    @pytest.mark.asyncio
    async def test_malware_classifier(self) -> None:
        """Test malware_classifier tool."""
        from dystopian_actors.tools import malware_classifier
        result = await malware_classifier()
        assert isinstance(result, dict)
        assert "status" in result
        assert result["status"] == "ok"

    @pytest.mark.asyncio
    async def test_vuln_tracker(self) -> None:
        """Test vuln_tracker tool."""
        from dystopian_actors.tools import vuln_tracker
        result = await vuln_tracker()
        assert isinstance(result, dict)
        assert "status" in result
        assert result["status"] == "ok"

    @pytest.mark.asyncio
    async def test_attribution_engine(self) -> None:
        """Test attribution_engine tool."""
        from dystopian_actors.tools import attribution_engine
        result = await attribution_engine()
        assert isinstance(result, dict)
        assert "status" in result
        assert result["status"] == "ok"

    @pytest.mark.asyncio
    async def test_infrastructure_mapper(self) -> None:
        """Test infrastructure_mapper tool."""
        from dystopian_actors.tools import infrastructure_mapper
        result = await infrastructure_mapper()
        assert isinstance(result, dict)
        assert "status" in result
        assert result["status"] == "ok"

    @pytest.mark.asyncio
    async def test_timeline_correlator(self) -> None:
        """Test timeline_correlator tool."""
        from dystopian_actors.tools import timeline_correlator
        result = await timeline_correlator()
        assert isinstance(result, dict)
        assert "status" in result
        assert result["status"] == "ok"

    @pytest.mark.asyncio
    async def test_pattern_detector(self) -> None:
        """Test pattern_detector tool."""
        from dystopian_actors.tools import pattern_detector
        result = await pattern_detector()
        assert isinstance(result, dict)
        assert "status" in result
        assert result["status"] == "ok"

    @pytest.mark.asyncio
    async def test_threat_hunter(self) -> None:
        """Test threat_hunter tool."""
        from dystopian_actors.tools import threat_hunter
        result = await threat_hunter()
        assert isinstance(result, dict)
        assert "status" in result
        assert result["status"] == "ok"

    @pytest.mark.asyncio
    async def test_intel_aggregator(self) -> None:
        """Test intel_aggregator tool."""
        from dystopian_actors.tools import intel_aggregator
        result = await intel_aggregator()
        assert isinstance(result, dict)
        assert "status" in result
        assert result["status"] == "ok"
