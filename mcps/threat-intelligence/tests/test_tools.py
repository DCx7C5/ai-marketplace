"""
Tests for threat-intelligence MCP tools.
"""

import pytest


class TestImports:
    def test_module_imports(self) -> None:
        try:
            import threat_intelligence  # noqa: F401
        except ImportError as e:
            pytest.fail(f"Failed to import: {e}")


class TestTools:

    @pytest.mark.asyncio
    async def test_actor_profiler(self) -> None:
        """Test actor_profiler tool."""
        from threat_intelligence.tools import actor_profiler
        result = await actor_profiler()
        assert isinstance(result, dict)
        assert "status" in result
        assert result["status"] == "ok"
        assert "tool" in result
        assert result["tool"] == "actor_profiler"

    @pytest.mark.asyncio
    async def test_ioc_enrichment(self) -> None:
        """Test ioc_enrichment tool."""
        from threat_intelligence.tools import ioc_enrichment
        result = await ioc_enrichment()
        assert isinstance(result, dict)
        assert "status" in result
        assert result["status"] == "ok"
        assert "tool" in result
        assert result["tool"] == "ioc_enrichment"

    @pytest.mark.asyncio
    async def test_threat_feed(self) -> None:
        """Test threat_feed tool."""
        from threat_intelligence.tools import threat_feed
        result = await threat_feed()
        assert isinstance(result, dict)
        assert "status" in result
        assert result["status"] == "ok"
        assert "tool" in result
        assert result["tool"] == "threat_feed"

    @pytest.mark.asyncio
    async def test_vulnerability_mapper(self) -> None:
        """Test vulnerability_mapper tool."""
        from threat_intelligence.tools import vulnerability_mapper
        result = await vulnerability_mapper()
        assert isinstance(result, dict)
        assert "status" in result
        assert result["status"] == "ok"
        assert "tool" in result
        assert result["tool"] == "vulnerability_mapper"

    @pytest.mark.asyncio
    async def test_exploit_analyzer(self) -> None:
        """Test exploit_analyzer tool."""
        from threat_intelligence.tools import exploit_analyzer
        result = await exploit_analyzer()
        assert isinstance(result, dict)
        assert "status" in result
        assert result["status"] == "ok"
        assert "tool" in result
        assert result["tool"] == "exploit_analyzer"

    @pytest.mark.asyncio
    async def test_campaign_correlator(self) -> None:
        """Test campaign_correlator tool."""
        from threat_intelligence.tools import campaign_correlator
        result = await campaign_correlator()
        assert isinstance(result, dict)
        assert "status" in result
        assert result["status"] == "ok"
        assert "tool" in result
        assert result["tool"] == "campaign_correlator"

    @pytest.mark.asyncio
    async def test_infrastructure_mapper(self) -> None:
        """Test infrastructure_mapper tool."""
        from threat_intelligence.tools import infrastructure_mapper
        result = await infrastructure_mapper()
        assert isinstance(result, dict)
        assert "status" in result
        assert result["status"] == "ok"
        assert "tool" in result
        assert result["tool"] == "infrastructure_mapper"

    @pytest.mark.asyncio
    async def test_tlp_classification(self) -> None:
        """Test tlp_classification tool."""
        from threat_intelligence.tools import tlp_classification
        result = await tlp_classification()
        assert isinstance(result, dict)
        assert "status" in result
        assert result["status"] == "ok"
        assert "tool" in result
        assert result["tool"] == "tlp_classification"

    @pytest.mark.asyncio
    async def test_attribution_engine(self) -> None:
        """Test attribution_engine tool."""
        from threat_intelligence.tools import attribution_engine
        result = await attribution_engine()
        assert isinstance(result, dict)
        assert "status" in result
        assert result["status"] == "ok"
        assert "tool" in result
        assert result["tool"] == "attribution_engine"

    @pytest.mark.asyncio
    async def test_timeline_correlator(self) -> None:
        """Test timeline_correlator tool."""
        from threat_intelligence.tools import timeline_correlator
        result = await timeline_correlator()
        assert isinstance(result, dict)
        assert "status" in result
        assert result["status"] == "ok"
        assert "tool" in result
        assert result["tool"] == "timeline_correlator"

    @pytest.mark.asyncio
    async def test_pattern_detector(self) -> None:
        """Test pattern_detector tool."""
        from threat_intelligence.tools import pattern_detector
        result = await pattern_detector()
        assert isinstance(result, dict)
        assert "status" in result
        assert result["status"] == "ok"
        assert "tool" in result
        assert result["tool"] == "pattern_detector"

    @pytest.mark.asyncio
    async def test_threat_hunting(self) -> None:
        """Test threat_hunting tool."""
        from threat_intelligence.tools import threat_hunting
        result = await threat_hunting()
        assert isinstance(result, dict)
        assert "status" in result
        assert result["status"] == "ok"
        assert "tool" in result
        assert result["tool"] == "threat_hunting"

    @pytest.mark.asyncio
    async def test_intelligence_aggregator(self) -> None:
        """Test intelligence_aggregator tool."""
        from threat_intelligence.tools import intelligence_aggregator
        result = await intelligence_aggregator()
        assert isinstance(result, dict)
        assert "status" in result
        assert result["status"] == "ok"
        assert "tool" in result
        assert result["tool"] == "intelligence_aggregator"

    @pytest.mark.asyncio
    async def test_report_generator(self) -> None:
        """Test report_generator tool."""
        from threat_intelligence.tools import report_generator
        result = await report_generator()
        assert isinstance(result, dict)
        assert "status" in result
        assert result["status"] == "ok"
        assert "tool" in result
        assert result["tool"] == "report_generator"
