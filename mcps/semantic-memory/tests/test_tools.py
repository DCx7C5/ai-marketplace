"""
Tests for ai-memory MCP tools.
"""

import pytest


class TestImports:
    def test_module_imports(self) -> None:
        try:
            import ai_memory  # noqa: F401
        except ImportError as e:
            pytest.fail(f"Failed to import: {e}")


class TestTools:

    @pytest.mark.asyncio
    async def test_memory_indexer(self) -> None:
        """Test memory_indexer tool."""
        from ai_memory.tools import memory_indexer
        result = await memory_indexer()
        assert isinstance(result, dict)
        assert "status" in result
        assert result["status"] == "ok"

    @pytest.mark.asyncio
    async def test_retrieval_engine(self) -> None:
        """Test retrieval_engine tool."""
        from ai_memory.tools import retrieval_engine
        result = await retrieval_engine()
        assert isinstance(result, dict)
        assert "status" in result
        assert result["status"] == "ok"

    @pytest.mark.asyncio
    async def test_embedding_generator(self) -> None:
        """Test embedding_generator tool."""
        from ai_memory.tools import embedding_generator
        result = await embedding_generator()
        assert isinstance(result, dict)
        assert "status" in result
        assert result["status"] == "ok"

    @pytest.mark.asyncio
    async def test_context_scorer(self) -> None:
        """Test context_scorer tool."""
        from ai_memory.tools import context_scorer
        result = await context_scorer()
        assert isinstance(result, dict)
        assert "status" in result
        assert result["status"] == "ok"

    @pytest.mark.asyncio
    async def test_memory_consolidator(self) -> None:
        """Test memory_consolidator tool."""
        from ai_memory.tools import memory_consolidator
        result = await memory_consolidator()
        assert isinstance(result, dict)
        assert "status" in result
        assert result["status"] == "ok"
