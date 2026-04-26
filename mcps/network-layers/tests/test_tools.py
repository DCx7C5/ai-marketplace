"""
Tests for network-layers MCP tools.
"""

import pytest


class TestImports:
    def test_module_imports(self) -> None:
        try:
            import network_layers  # noqa: F401
        except ImportError as e:
            pytest.fail(f"Failed to import: {e}")


class TestTools:

    @pytest.mark.asyncio
    async def test_packet_capture(self) -> None:
        """Test packet_capture tool."""
        from network_layers.tools import packet_capture
        result = await packet_capture()
        assert isinstance(result, dict)
        assert "status" in result
        assert result["status"] == "ok"
        assert "tool" in result
        assert result["tool"] == "packet_capture"

    @pytest.mark.asyncio
    async def test_protocol_analyzer(self) -> None:
        """Test protocol_analyzer tool."""
        from network_layers.tools import protocol_analyzer
        result = await protocol_analyzer()
        assert isinstance(result, dict)
        assert "status" in result
        assert result["status"] == "ok"
        assert "tool" in result
        assert result["tool"] == "protocol_analyzer"

    @pytest.mark.asyncio
    async def test_flow_analyzer(self) -> None:
        """Test flow_analyzer tool."""
        from network_layers.tools import flow_analyzer
        result = await flow_analyzer()
        assert isinstance(result, dict)
        assert "status" in result
        assert result["status"] == "ok"
        assert "tool" in result
        assert result["tool"] == "flow_analyzer"

    @pytest.mark.asyncio
    async def test_topology_mapper(self) -> None:
        """Test topology_mapper tool."""
        from network_layers.tools import topology_mapper
        result = await topology_mapper()
        assert isinstance(result, dict)
        assert "status" in result
        assert result["status"] == "ok"
        assert "tool" in result
        assert result["tool"] == "topology_mapper"

    @pytest.mark.asyncio
    async def test_dns_resolver(self) -> None:
        """Test dns_resolver tool."""
        from network_layers.tools import dns_resolver
        result = await dns_resolver()
        assert isinstance(result, dict)
        assert "status" in result
        assert result["status"] == "ok"
        assert "tool" in result
        assert result["tool"] == "dns_resolver"

    @pytest.mark.asyncio
    async def test_port_scanner(self) -> None:
        """Test port_scanner tool."""
        from network_layers.tools import port_scanner
        result = await port_scanner()
        assert isinstance(result, dict)
        assert "status" in result
        assert result["status"] == "ok"
        assert "tool" in result
        assert result["tool"] == "port_scanner"

    @pytest.mark.asyncio
    async def test_banner_grabber(self) -> None:
        """Test banner_grabber tool."""
        from network_layers.tools import banner_grabber
        result = await banner_grabber()
        assert isinstance(result, dict)
        assert "status" in result
        assert result["status"] == "ok"
        assert "tool" in result
        assert result["tool"] == "banner_grabber"

    @pytest.mark.asyncio
    async def test_traffic_profiler(self) -> None:
        """Test traffic_profiler tool."""
        from network_layers.tools import traffic_profiler
        result = await traffic_profiler()
        assert isinstance(result, dict)
        assert "status" in result
        assert result["status"] == "ok"
        assert "tool" in result
        assert result["tool"] == "traffic_profiler"

    @pytest.mark.asyncio
    async def test_geolocation_lookup(self) -> None:
        """Test geolocation_lookup tool."""
        from network_layers.tools import geolocation_lookup
        result = await geolocation_lookup()
        assert isinstance(result, dict)
        assert "status" in result
        assert result["status"] == "ok"
        assert "tool" in result
        assert result["tool"] == "geolocation_lookup"
