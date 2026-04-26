"""
Tests for api-security MCP tools.
"""

import pytest


class TestImports:
    def test_module_imports(self) -> None:
        try:
            import api_security  # noqa: F401
        except ImportError as e:
            pytest.fail(f"Failed to import: {e}")


class TestTools:

    @pytest.mark.asyncio
    async def test_endpoint_scanner(self) -> None:
        """Test endpoint_scanner tool."""
        from api_security.tools import endpoint_scanner
        result = await endpoint_scanner()
        assert isinstance(result, dict)
        assert "status" in result
        assert result["status"] == "ok"

    @pytest.mark.asyncio
    async def test_payload_fuzzer(self) -> None:
        """Test payload_fuzzer tool."""
        from api_security.tools import payload_fuzzer
        result = await payload_fuzzer()
        assert isinstance(result, dict)
        assert "status" in result
        assert result["status"] == "ok"

    @pytest.mark.asyncio
    async def test_auth_tester(self) -> None:
        """Test auth_tester tool."""
        from api_security.tools import auth_tester
        result = await auth_tester()
        assert isinstance(result, dict)
        assert "status" in result
        assert result["status"] == "ok"

    @pytest.mark.asyncio
    async def test_rate_limiter_checker(self) -> None:
        """Test rate_limiter_checker tool."""
        from api_security.tools import rate_limiter_checker
        result = await rate_limiter_checker()
        assert isinstance(result, dict)
        assert "status" in result
        assert result["status"] == "ok"

    @pytest.mark.asyncio
    async def test_header_analyzer(self) -> None:
        """Test header_analyzer tool."""
        from api_security.tools import header_analyzer
        result = await header_analyzer()
        assert isinstance(result, dict)
        assert "status" in result
        assert result["status"] == "ok"

    @pytest.mark.asyncio
    async def test_response_validator(self) -> None:
        """Test response_validator tool."""
        from api_security.tools import response_validator
        result = await response_validator()
        assert isinstance(result, dict)
        assert "status" in result
        assert result["status"] == "ok"

    @pytest.mark.asyncio
    async def test_injection_detector(self) -> None:
        """Test injection_detector tool."""
        from api_security.tools import injection_detector
        result = await injection_detector()
        assert isinstance(result, dict)
        assert "status" in result
        assert result["status"] == "ok"

    @pytest.mark.asyncio
    async def test_schema_validator(self) -> None:
        """Test schema_validator tool."""
        from api_security.tools import schema_validator
        result = await schema_validator()
        assert isinstance(result, dict)
        assert "status" in result
        assert result["status"] == "ok"
