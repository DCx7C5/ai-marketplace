"""
Tests for incident-management MCP tools.
"""

import pytest


class TestImports:
    def test_module_imports(self) -> None:
        try:
            import incident_management  # noqa: F401
        except ImportError as e:
            pytest.fail(f"Failed to import: {e}")


class TestTools:

    @pytest.mark.asyncio
    async def test_incident_creator(self) -> None:
        """Test incident_creator tool."""
        from incident_management.tools import incident_creator
        result = await incident_creator()
        assert isinstance(result, dict)
        assert "status" in result
        assert result["status"] == "ok"

    @pytest.mark.asyncio
    async def test_incident_updater(self) -> None:
        """Test incident_updater tool."""
        from incident_management.tools import incident_updater
        result = await incident_updater()
        assert isinstance(result, dict)
        assert "status" in result
        assert result["status"] == "ok"

    @pytest.mark.asyncio
    async def test_incident_resolver(self) -> None:
        """Test incident_resolver tool."""
        from incident_management.tools import incident_resolver
        result = await incident_resolver()
        assert isinstance(result, dict)
        assert "status" in result
        assert result["status"] == "ok"

    @pytest.mark.asyncio
    async def test_playbook_executor(self) -> None:
        """Test playbook_executor tool."""
        from incident_management.tools import playbook_executor
        result = await playbook_executor()
        assert isinstance(result, dict)
        assert "status" in result
        assert result["status"] == "ok"

    @pytest.mark.asyncio
    async def test_escalation_handler(self) -> None:
        """Test escalation_handler tool."""
        from incident_management.tools import escalation_handler
        result = await escalation_handler()
        assert isinstance(result, dict)
        assert "status" in result
        assert result["status"] == "ok"

    @pytest.mark.asyncio
    async def test_notification_sender(self) -> None:
        """Test notification_sender tool."""
        from incident_management.tools import notification_sender
        result = await notification_sender()
        assert isinstance(result, dict)
        assert "status" in result
        assert result["status"] == "ok"
