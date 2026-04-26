"""
Tests for forensic-vault MCP tools.
"""

import pytest


class TestImports:
    def test_module_imports(self) -> None:
        try:
            import forensic_vault  # noqa: F401
        except ImportError as e:
            pytest.fail(f"Failed to import: {e}")


class TestTools:

    @pytest.mark.asyncio
    async def test_case_management(self) -> None:
        """Test case_management tool."""
        from forensic_vault.tools import case_management
        result = await case_management()
        assert isinstance(result, dict)
        assert "status" in result
        assert result["status"] == "ok"
        assert "tool" in result
        assert result["tool"] == "case_management"

    @pytest.mark.asyncio
    async def test_evidence_handler(self) -> None:
        """Test evidence_handler tool."""
        from forensic_vault.tools import evidence_handler
        result = await evidence_handler()
        assert isinstance(result, dict)
        assert "status" in result
        assert result["status"] == "ok"
        assert "tool" in result
        assert result["tool"] == "evidence_handler"

    @pytest.mark.asyncio
    async def test_ioc_extractor(self) -> None:
        """Test ioc_extractor tool."""
        from forensic_vault.tools import ioc_extractor
        result = await ioc_extractor()
        assert isinstance(result, dict)
        assert "status" in result
        assert result["status"] == "ok"
        assert "tool" in result
        assert result["tool"] == "ioc_extractor"

    @pytest.mark.asyncio
    async def test_malware_analyzer(self) -> None:
        """Test malware_analyzer tool."""
        from forensic_vault.tools import malware_analyzer
        result = await malware_analyzer()
        assert isinstance(result, dict)
        assert "status" in result
        assert result["status"] == "ok"
        assert "tool" in result
        assert result["tool"] == "malware_analyzer"

    @pytest.mark.asyncio
    async def test_timeline_builder(self) -> None:
        """Test timeline_builder tool."""
        from forensic_vault.tools import timeline_builder
        result = await timeline_builder()
        assert isinstance(result, dict)
        assert "status" in result
        assert result["status"] == "ok"
        assert "tool" in result
        assert result["tool"] == "timeline_builder"

    @pytest.mark.asyncio
    async def test_chain_of_custody(self) -> None:
        """Test chain_of_custody tool."""
        from forensic_vault.tools import chain_of_custody
        result = await chain_of_custody()
        assert isinstance(result, dict)
        assert "status" in result
        assert result["status"] == "ok"
        assert "tool" in result
        assert result["tool"] == "chain_of_custody"

    @pytest.mark.asyncio
    async def test_artifact_vault(self) -> None:
        """Test artifact_vault tool."""
        from forensic_vault.tools import artifact_vault
        result = await artifact_vault()
        assert isinstance(result, dict)
        assert "status" in result
        assert result["status"] == "ok"
        assert "tool" in result
        assert result["tool"] == "artifact_vault"

    @pytest.mark.asyncio
    async def test_evidence_validator(self) -> None:
        """Test evidence_validator tool."""
        from forensic_vault.tools import evidence_validator
        result = await evidence_validator()
        assert isinstance(result, dict)
        assert "status" in result
        assert result["status"] == "ok"
        assert "tool" in result
        assert result["tool"] == "evidence_validator"

    @pytest.mark.asyncio
    async def test_signature_matcher(self) -> None:
        """Test signature_matcher tool."""
        from forensic_vault.tools import signature_matcher
        result = await signature_matcher()
        assert isinstance(result, dict)
        assert "status" in result
        assert result["status"] == "ok"
        assert "tool" in result
        assert result["tool"] == "signature_matcher"

    @pytest.mark.asyncio
    async def test_hash_analyzer(self) -> None:
        """Test hash_analyzer tool."""
        from forensic_vault.tools import hash_analyzer
        result = await hash_analyzer()
        assert isinstance(result, dict)
        assert "status" in result
        assert result["status"] == "ok"
        assert "tool" in result
        assert result["tool"] == "hash_analyzer"

    @pytest.mark.asyncio
    async def test_yara_scanner(self) -> None:
        """Test yara_scanner tool."""
        from forensic_vault.tools import yara_scanner
        result = await yara_scanner()
        assert isinstance(result, dict)
        assert "status" in result
        assert result["status"] == "ok"
        assert "tool" in result
        assert result["tool"] == "yara_scanner"

    @pytest.mark.asyncio
    async def test_memory_forensics(self) -> None:
        """Test memory_forensics tool."""
        from forensic_vault.tools import memory_forensics
        result = await memory_forensics()
        assert isinstance(result, dict)
        assert "status" in result
        assert result["status"] == "ok"
        assert "tool" in result
        assert result["tool"] == "memory_forensics"

    @pytest.mark.asyncio
    async def test_log_parser(self) -> None:
        """Test log_parser tool."""
        from forensic_vault.tools import log_parser
        result = await log_parser()
        assert isinstance(result, dict)
        assert "status" in result
        assert result["status"] == "ok"
        assert "tool" in result
        assert result["tool"] == "log_parser"

    @pytest.mark.asyncio
    async def test_entropy_analyzer(self) -> None:
        """Test entropy_analyzer tool."""
        from forensic_vault.tools import entropy_analyzer
        result = await entropy_analyzer()
        assert isinstance(result, dict)
        assert "status" in result
        assert result["status"] == "ok"
        assert "tool" in result
        assert result["tool"] == "entropy_analyzer"
