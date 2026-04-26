"""
Tests for encoding-analysis MCP tools.
"""

import pytest


class TestImports:
    def test_module_imports(self) -> None:
        try:
            import encoding_analysis  # noqa: F401
        except ImportError as e:
            pytest.fail(f"Failed to import: {e}")


class TestTools:

    @pytest.mark.asyncio
    async def test_base64_decoder(self) -> None:
        """Test base64_decoder tool."""
        from encoding_analysis.tools import base64_decoder
        result = await base64_decoder()
        assert isinstance(result, dict)
        assert "status" in result
        assert result["status"] == "ok"

    @pytest.mark.asyncio
    async def test_hex_converter(self) -> None:
        """Test hex_converter tool."""
        from encoding_analysis.tools import hex_converter
        result = await hex_converter()
        assert isinstance(result, dict)
        assert "status" in result
        assert result["status"] == "ok"

    @pytest.mark.asyncio
    async def test_url_decoder(self) -> None:
        """Test url_decoder tool."""
        from encoding_analysis.tools import url_decoder
        result = await url_decoder()
        assert isinstance(result, dict)
        assert "status" in result
        assert result["status"] == "ok"

    @pytest.mark.asyncio
    async def test_unicode_analyzer(self) -> None:
        """Test unicode_analyzer tool."""
        from encoding_analysis.tools import unicode_analyzer
        result = await unicode_analyzer()
        assert isinstance(result, dict)
        assert "status" in result
        assert result["status"] == "ok"

    @pytest.mark.asyncio
    async def test_obfuscation_detector(self) -> None:
        """Test obfuscation_detector tool."""
        from encoding_analysis.tools import obfuscation_detector
        result = await obfuscation_detector()
        assert isinstance(result, dict)
        assert "status" in result
        assert result["status"] == "ok"

    @pytest.mark.asyncio
    async def test_polyglot_finder(self) -> None:
        """Test polyglot_finder tool."""
        from encoding_analysis.tools import polyglot_finder
        result = await polyglot_finder()
        assert isinstance(result, dict)
        assert "status" in result
        assert result["status"] == "ok"

    @pytest.mark.asyncio
    async def test_charset_detector(self) -> None:
        """Test charset_detector tool."""
        from encoding_analysis.tools import charset_detector
        result = await charset_detector()
        assert isinstance(result, dict)
        assert "status" in result
        assert result["status"] == "ok"

    @pytest.mark.asyncio
    async def test_encoding_chain_parser(self) -> None:
        """Test encoding_chain_parser tool."""
        from encoding_analysis.tools import encoding_chain_parser
        result = await encoding_chain_parser()
        assert isinstance(result, dict)
        assert "status" in result
        assert result["status"] == "ok"
