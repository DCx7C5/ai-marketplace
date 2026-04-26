"""
Tests for email-analysis MCP tools.
"""

import pytest


class TestImports:
    def test_module_imports(self) -> None:
        try:
            import email_analysis  # noqa: F401
        except ImportError as e:
            pytest.fail(f"Failed to import: {e}")


class TestTools:

    @pytest.mark.asyncio
    async def test_eml_parser(self) -> None:
        """Test eml_parser tool."""
        from email_analysis.tools import eml_parser
        result = await eml_parser()
        assert isinstance(result, dict)
        assert "status" in result
        assert result["status"] == "ok"

    @pytest.mark.asyncio
    async def test_header_analyzer(self) -> None:
        """Test header_analyzer tool."""
        from email_analysis.tools import header_analyzer
        result = await header_analyzer()
        assert isinstance(result, dict)
        assert "status" in result
        assert result["status"] == "ok"

    @pytest.mark.asyncio
    async def test_attachment_extractor(self) -> None:
        """Test attachment_extractor tool."""
        from email_analysis.tools import attachment_extractor
        result = await attachment_extractor()
        assert isinstance(result, dict)
        assert "status" in result
        assert result["status"] == "ok"

    @pytest.mark.asyncio
    async def test_phishing_detector(self) -> None:
        """Test phishing_detector tool."""
        from email_analysis.tools import phishing_detector
        result = await phishing_detector()
        assert isinstance(result, dict)
        assert "status" in result
        assert result["status"] == "ok"

    @pytest.mark.asyncio
    async def test_sender_verifier(self) -> None:
        """Test sender_verifier tool."""
        from email_analysis.tools import sender_verifier
        result = await sender_verifier()
        assert isinstance(result, dict)
        assert "status" in result
        assert result["status"] == "ok"

    @pytest.mark.asyncio
    async def test_link_analyzer(self) -> None:
        """Test link_analyzer tool."""
        from email_analysis.tools import link_analyzer
        result = await link_analyzer()
        assert isinstance(result, dict)
        assert "status" in result
        assert result["status"] == "ok"

    @pytest.mark.asyncio
    async def test_mime_decoder(self) -> None:
        """Test mime_decoder tool."""
        from email_analysis.tools import mime_decoder
        result = await mime_decoder()
        assert isinstance(result, dict)
        assert "status" in result
        assert result["status"] == "ok"

    @pytest.mark.asyncio
    async def test_reputation_checker(self) -> None:
        """Test reputation_checker tool."""
        from email_analysis.tools import reputation_checker
        result = await reputation_checker()
        assert isinstance(result, dict)
        assert "status" in result
        assert result["status"] == "ok"
