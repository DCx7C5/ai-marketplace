"""
Tests for session-management MCP tools.
"""

import pytest


class TestImports:
    def test_module_imports(self) -> None:
        try:
            import session_management  # noqa: F401
        except ImportError as e:
            pytest.fail(f"Failed to import: {e}")


class TestTools:

    @pytest.mark.asyncio
    async def test_session_tracker(self) -> None:
        """Test session_tracker tool."""
        from session_management.tools import session_tracker
        result = await session_tracker()
        assert isinstance(result, dict)
        assert "status" in result
        assert result["status"] == "ok"

    @pytest.mark.asyncio
    async def test_context_manager(self) -> None:
        """Test context_manager tool."""
        from session_management.tools import context_manager
        result = await context_manager()
        assert isinstance(result, dict)
        assert "status" in result
        assert result["status"] == "ok"

    @pytest.mark.asyncio
    async def test_token_limiter(self) -> None:
        """Test token_limiter tool."""
        from session_management.tools import token_limiter
        result = await token_limiter()
        assert isinstance(result, dict)
        assert "status" in result
        assert result["status"] == "ok"

    @pytest.mark.asyncio
    async def test_state_serializer(self) -> None:
        """Test state_serializer tool."""
        from session_management.tools import state_serializer
        result = await state_serializer()
        assert isinstance(result, dict)
        assert "status" in result
        assert result["status"] == "ok"

    @pytest.mark.asyncio
    async def test_history_manager(self) -> None:
        """Test history_manager tool."""
        from session_management.tools import history_manager
        result = await history_manager()
        assert isinstance(result, dict)
        assert "status" in result
        assert result["status"] == "ok"

    @pytest.mark.asyncio
    async def test_cache_invalidator(self) -> None:
        """Test cache_invalidator tool."""
        from session_management.tools import cache_invalidator
        result = await cache_invalidator()
        assert isinstance(result, dict)
        assert "status" in result
        assert result["status"] == "ok"

    @pytest.mark.asyncio
    async def test_session_auditor(self) -> None:
        """Test session_auditor tool."""
        from session_management.tools import session_auditor
        result = await session_auditor()
        assert isinstance(result, dict)
        assert "status" in result
        assert result["status"] == "ok"
