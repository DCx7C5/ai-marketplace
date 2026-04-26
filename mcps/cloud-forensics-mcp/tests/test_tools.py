"""
Tests for cloud-forensics MCP tools.
"""

import pytest


class TestImports:
    def test_module_imports(self) -> None:
        try:
            import cloud_forensics  # noqa: F401
        except ImportError as e:
            pytest.fail(f"Failed to import: {e}")


class TestTools:

    @pytest.mark.asyncio
    async def test_aws_auditor(self) -> None:
        """Test aws_auditor tool."""
        from cloud_forensics.tools import aws_auditor
        result = await aws_auditor()
        assert isinstance(result, dict)
        assert "status" in result
        assert result["status"] == "ok"

    @pytest.mark.asyncio
    async def test_azure_analyzer(self) -> None:
        """Test azure_analyzer tool."""
        from cloud_forensics.tools import azure_analyzer
        result = await azure_analyzer()
        assert isinstance(result, dict)
        assert "status" in result
        assert result["status"] == "ok"

    @pytest.mark.asyncio
    async def test_gcp_scanner(self) -> None:
        """Test gcp_scanner tool."""
        from cloud_forensics.tools import gcp_scanner
        result = await gcp_scanner()
        assert isinstance(result, dict)
        assert "status" in result
        assert result["status"] == "ok"

    @pytest.mark.asyncio
    async def test_bucket_enumerator(self) -> None:
        """Test bucket_enumerator tool."""
        from cloud_forensics.tools import bucket_enumerator
        result = await bucket_enumerator()
        assert isinstance(result, dict)
        assert "status" in result
        assert result["status"] == "ok"

    @pytest.mark.asyncio
    async def test_log_collector(self) -> None:
        """Test log_collector tool."""
        from cloud_forensics.tools import log_collector
        result = await log_collector()
        assert isinstance(result, dict)
        assert "status" in result
        assert result["status"] == "ok"

    @pytest.mark.asyncio
    async def test_vm_inspector(self) -> None:
        """Test vm_inspector tool."""
        from cloud_forensics.tools import vm_inspector
        result = await vm_inspector()
        assert isinstance(result, dict)
        assert "status" in result
        assert result["status"] == "ok"

    @pytest.mark.asyncio
    async def test_snapshot_analyzer(self) -> None:
        """Test snapshot_analyzer tool."""
        from cloud_forensics.tools import snapshot_analyzer
        result = await snapshot_analyzer()
        assert isinstance(result, dict)
        assert "status" in result
        assert result["status"] == "ok"

    @pytest.mark.asyncio
    async def test_credential_finder(self) -> None:
        """Test credential_finder tool."""
        from cloud_forensics.tools import credential_finder
        result = await credential_finder()
        assert isinstance(result, dict)
        assert "status" in result
        assert result["status"] == "ok"
