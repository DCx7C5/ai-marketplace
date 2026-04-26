"""
Tests for code-analysis MCP tools.
"""

import pytest


class TestImports:
    def test_module_imports(self) -> None:
        try:
            import code_analysis  # noqa: F401
        except ImportError as e:
            pytest.fail(f"Failed to import: {e}")


class TestTools:

    @pytest.mark.asyncio
    async def test_ast_parser(self) -> None:
        """Test ast_parser tool."""
        from code_analysis.tools import ast_parser
        result = await ast_parser()
        assert isinstance(result, dict)
        assert "status" in result
        assert result["status"] == "ok"

    @pytest.mark.asyncio
    async def test_vulnerability_scanner(self) -> None:
        """Test vulnerability_scanner tool."""
        from code_analysis.tools import vulnerability_scanner
        result = await vulnerability_scanner()
        assert isinstance(result, dict)
        assert "status" in result
        assert result["status"] == "ok"

    @pytest.mark.asyncio
    async def test_complexity_analyzer(self) -> None:
        """Test complexity_analyzer tool."""
        from code_analysis.tools import complexity_analyzer
        result = await complexity_analyzer()
        assert isinstance(result, dict)
        assert "status" in result
        assert result["status"] == "ok"

    @pytest.mark.asyncio
    async def test_dependency_auditor(self) -> None:
        """Test dependency_auditor tool."""
        from code_analysis.tools import dependency_auditor
        result = await dependency_auditor()
        assert isinstance(result, dict)
        assert "status" in result
        assert result["status"] == "ok"

    @pytest.mark.asyncio
    async def test_secret_detector(self) -> None:
        """Test secret_detector tool."""
        from code_analysis.tools import secret_detector
        result = await secret_detector()
        assert isinstance(result, dict)
        assert "status" in result
        assert result["status"] == "ok"

    @pytest.mark.asyncio
    async def test_pattern_finder(self) -> None:
        """Test pattern_finder tool."""
        from code_analysis.tools import pattern_finder
        result = await pattern_finder()
        assert isinstance(result, dict)
        assert "status" in result
        assert result["status"] == "ok"

    @pytest.mark.asyncio
    async def test_metric_calculator(self) -> None:
        """Test metric_calculator tool."""
        from code_analysis.tools import metric_calculator
        result = await metric_calculator()
        assert isinstance(result, dict)
        assert "status" in result
        assert result["status"] == "ok"

    @pytest.mark.asyncio
    async def test_report_generator(self) -> None:
        """Test report_generator tool."""
        from code_analysis.tools import report_generator
        result = await report_generator()
        assert isinstance(result, dict)
        assert "status" in result
        assert result["status"] == "ok"
