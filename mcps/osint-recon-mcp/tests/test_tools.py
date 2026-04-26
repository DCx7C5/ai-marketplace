"""
Tests for osint-recon MCP tools.
"""

import pytest


class TestImports:
    def test_module_imports(self) -> None:
        try:
            import osint_recon  # noqa: F401
        except ImportError as e:
            pytest.fail(f"Failed to import: {e}")


class TestTools:

    @pytest.mark.asyncio
    async def test_domain_scanner(self) -> None:
        """Test domain_scanner tool."""
        from osint_recon.tools import domain_scanner
        result = await domain_scanner()
        assert isinstance(result, dict)
        assert "status" in result
        assert result["status"] == "ok"

    @pytest.mark.asyncio
    async def test_dns_enumerator(self) -> None:
        """Test dns_enumerator tool."""
        from osint_recon.tools import dns_enumerator
        result = await dns_enumerator()
        assert isinstance(result, dict)
        assert "status" in result
        assert result["status"] == "ok"

    @pytest.mark.asyncio
    async def test_subdomain_finder(self) -> None:
        """Test subdomain_finder tool."""
        from osint_recon.tools import subdomain_finder
        result = await subdomain_finder()
        assert isinstance(result, dict)
        assert "status" in result
        assert result["status"] == "ok"

    @pytest.mark.asyncio
    async def test_whois_lookup(self) -> None:
        """Test whois_lookup tool."""
        from osint_recon.tools import whois_lookup
        result = await whois_lookup()
        assert isinstance(result, dict)
        assert "status" in result
        assert result["status"] == "ok"

    @pytest.mark.asyncio
    async def test_ssl_analyzer(self) -> None:
        """Test ssl_analyzer tool."""
        from osint_recon.tools import ssl_analyzer
        result = await ssl_analyzer()
        assert isinstance(result, dict)
        assert "status" in result
        assert result["status"] == "ok"

    @pytest.mark.asyncio
    async def test_web_scraper(self) -> None:
        """Test web_scraper tool."""
        from osint_recon.tools import web_scraper
        result = await web_scraper()
        assert isinstance(result, dict)
        assert "status" in result
        assert result["status"] == "ok"

    @pytest.mark.asyncio
    async def test_metadata_extractor(self) -> None:
        """Test metadata_extractor tool."""
        from osint_recon.tools import metadata_extractor
        result = await metadata_extractor()
        assert isinstance(result, dict)
        assert "status" in result
        assert result["status"] == "ok"

    @pytest.mark.asyncio
    async def test_reverse_lookup(self) -> None:
        """Test reverse_lookup tool."""
        from osint_recon.tools import reverse_lookup
        result = await reverse_lookup()
        assert isinstance(result, dict)
        assert "status" in result
        assert result["status"] == "ok"
