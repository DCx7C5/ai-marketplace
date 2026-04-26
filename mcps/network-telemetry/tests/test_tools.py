"""
Tests for network-monitoring MCP tools.
"""

import pytest


class TestImports:
    def test_module_imports(self) -> None:
        try:
            import network_monitoring  # noqa: F401
        except ImportError as e:
            pytest.fail(f"Failed to import: {e}")


class TestTools:

    @pytest.mark.asyncio
    async def test_interface_monitor(self) -> None:
        """Test interface_monitor tool."""
        from network_monitoring.tools import interface_monitor
        result = await interface_monitor()
        assert isinstance(result, dict)
        assert "status" in result
        assert result["status"] == "ok"

    @pytest.mark.asyncio
    async def test_bandwidth_profiler(self) -> None:
        """Test bandwidth_profiler tool."""
        from network_monitoring.tools import bandwidth_profiler
        result = await bandwidth_profiler()
        assert isinstance(result, dict)
        assert "status" in result
        assert result["status"] == "ok"

    @pytest.mark.asyncio
    async def test_connection_tracker(self) -> None:
        """Test connection_tracker tool."""
        from network_monitoring.tools import connection_tracker
        result = await connection_tracker()
        assert isinstance(result, dict)
        assert "status" in result
        assert result["status"] == "ok"

    @pytest.mark.asyncio
    async def test_packet_inspector(self) -> None:
        """Test packet_inspector tool."""
        from network_monitoring.tools import packet_inspector
        result = await packet_inspector()
        assert isinstance(result, dict)
        assert "status" in result
        assert result["status"] == "ok"

    @pytest.mark.asyncio
    async def test_latency_meter(self) -> None:
        """Test latency_meter tool."""
        from network_monitoring.tools import latency_meter
        result = await latency_meter()
        assert isinstance(result, dict)
        assert "status" in result
        assert result["status"] == "ok"

    @pytest.mark.asyncio
    async def test_throughput_analyzer(self) -> None:
        """Test throughput_analyzer tool."""
        from network_monitoring.tools import throughput_analyzer
        result = await throughput_analyzer()
        assert isinstance(result, dict)
        assert "status" in result
        assert result["status"] == "ok"
