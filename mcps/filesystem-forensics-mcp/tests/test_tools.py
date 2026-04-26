"""
Tests for filesystem-forensics MCP tools.
"""

import pytest


class TestImports:
    def test_module_imports(self) -> None:
        try:
            import filesystem_forensics  # noqa: F401
        except ImportError as e:
            pytest.fail(f"Failed to import: {e}")


class TestTools:

    @pytest.mark.asyncio
    async def test_file_hasher(self) -> None:
        """Test file_hasher tool."""
        from filesystem_forensics.tools import file_hasher
        result = await file_hasher()
        assert isinstance(result, dict)
        assert "status" in result
        assert result["status"] == "ok"

    @pytest.mark.asyncio
    async def test_carving_engine(self) -> None:
        """Test carving_engine tool."""
        from filesystem_forensics.tools import carving_engine
        result = await carving_engine()
        assert isinstance(result, dict)
        assert "status" in result
        assert result["status"] == "ok"

    @pytest.mark.asyncio
    async def test_metadata_extractor(self) -> None:
        """Test metadata_extractor tool."""
        from filesystem_forensics.tools import metadata_extractor
        result = await metadata_extractor()
        assert isinstance(result, dict)
        assert "status" in result
        assert result["status"] == "ok"

    @pytest.mark.asyncio
    async def test_timeline_generator(self) -> None:
        """Test timeline_generator tool."""
        from filesystem_forensics.tools import timeline_generator
        result = await timeline_generator()
        assert isinstance(result, dict)
        assert "status" in result
        assert result["status"] == "ok"

    @pytest.mark.asyncio
    async def test_access_tracker(self) -> None:
        """Test access_tracker tool."""
        from filesystem_forensics.tools import access_tracker
        result = await access_tracker()
        assert isinstance(result, dict)
        assert "status" in result
        assert result["status"] == "ok"

    @pytest.mark.asyncio
    async def test_signature_validator(self) -> None:
        """Test signature_validator tool."""
        from filesystem_forensics.tools import signature_validator
        result = await signature_validator()
        assert isinstance(result, dict)
        assert "status" in result
        assert result["status"] == "ok"

    @pytest.mark.asyncio
    async def test_deletion_recovery(self) -> None:
        """Test deletion_recovery tool."""
        from filesystem_forensics.tools import deletion_recovery
        result = await deletion_recovery()
        assert isinstance(result, dict)
        assert "status" in result
        assert result["status"] == "ok"

    @pytest.mark.asyncio
    async def test_archive_analyzer(self) -> None:
        """Test archive_analyzer tool."""
        from filesystem_forensics.tools import archive_analyzer
        result = await archive_analyzer()
        assert isinstance(result, dict)
        assert "status" in result
        assert result["status"] == "ok"
