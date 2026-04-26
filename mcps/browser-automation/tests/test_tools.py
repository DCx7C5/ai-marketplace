"""
Tests for browser-automation MCP tools.
"""

import pytest


class TestImports:
    def test_module_imports(self) -> None:
        try:
            import browser_automation  # noqa: F401
        except ImportError as e:
            pytest.fail(f"Failed to import: {e}")


class TestTools:

    @pytest.mark.asyncio
    async def test_headless_browser(self) -> None:
        """Test headless_browser tool."""
        from browser_automation.tools import headless_browser
        result = await headless_browser()
        assert isinstance(result, dict)
        assert "status" in result
        assert result["status"] == "ok"

    @pytest.mark.asyncio
    async def test_screenshot_capture(self) -> None:
        """Test screenshot_capture tool."""
        from browser_automation.tools import screenshot_capture
        result = await screenshot_capture()
        assert isinstance(result, dict)
        assert "status" in result
        assert result["status"] == "ok"

    @pytest.mark.asyncio
    async def test_click_element(self) -> None:
        """Test click_element tool."""
        from browser_automation.tools import click_element
        result = await click_element()
        assert isinstance(result, dict)
        assert "status" in result
        assert result["status"] == "ok"

    @pytest.mark.asyncio
    async def test_type_text(self) -> None:
        """Test type_text tool."""
        from browser_automation.tools import type_text
        result = await type_text()
        assert isinstance(result, dict)
        assert "status" in result
        assert result["status"] == "ok"

    @pytest.mark.asyncio
    async def test_navigate_url(self) -> None:
        """Test navigate_url tool."""
        from browser_automation.tools import navigate_url
        result = await navigate_url()
        assert isinstance(result, dict)
        assert "status" in result
        assert result["status"] == "ok"

    @pytest.mark.asyncio
    async def test_wait_for_element(self) -> None:
        """Test wait_for_element tool."""
        from browser_automation.tools import wait_for_element
        result = await wait_for_element()
        assert isinstance(result, dict)
        assert "status" in result
        assert result["status"] == "ok"
