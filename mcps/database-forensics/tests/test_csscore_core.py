"""
Unit tests for CyberSecSuite Core MCP foundation functions.

Tests all 5 core functions with 100% coverage requirement for Phase 0.75.
"""

import pytest

from mcp_csscore.core import (
    ScopeContext,
    ScopeLevel,
    create_audit_logger,
    discover_assets,
    get_configuration,
    get_marketplace_registry,
    get_scope_context,
)


@pytest.fixture
def sample_scope() -> ScopeContext:
    """Create a sample scope context for testing."""
    return ScopeContext(
        scope_level=ScopeLevel.RUNTIME,
        runtime_id="runtime-001",
        worktree_path="/tmp/csscore-test",
    )


@pytest.mark.asyncio
async def test_get_marketplace_registry():
    """Test marketplace registry retrieval."""
    registry = await get_marketplace_registry()

    assert isinstance(registry, dict)
    assert "csscore" in registry
    assert registry["csscore"]["version"] == "1.0.0"
    assert isinstance(registry["csscore"]["tools"], list)
    assert len(registry["csscore"]["tools"]) > 0
    assert "get_marketplace_registry" in registry["csscore"]["tools"]


@pytest.mark.asyncio
async def test_discover_assets_no_filter(sample_scope):
    """Test asset discovery without type filter."""
    assets = await discover_assets(sample_scope)

    assert isinstance(assets, list)
    assert len(assets) > 0
    assert all("id" in asset for asset in assets)
    assert all("type" in asset for asset in assets)
    assert all("name" in asset for asset in assets)
    assert all("scope" in asset for asset in assets)


@pytest.mark.asyncio
async def test_discover_assets_with_filter(sample_scope):
    """Test asset discovery with type filter."""
    assets = await discover_assets(sample_scope, asset_type="host")

    assert isinstance(assets, list)
    assert all(asset["type"] == "host" for asset in assets)


@pytest.mark.asyncio
async def test_discover_assets_filtered_empty(sample_scope):
    """Test asset discovery with non-matching filter."""
    assets = await discover_assets(sample_scope, asset_type="nonexistent")

    assert isinstance(assets, list)
    assert len(assets) == 0


@pytest.mark.asyncio
async def test_get_configuration_nested_key(sample_scope):
    """Test configuration retrieval for nested key."""
    result = await get_configuration("logging.level", sample_scope)

    assert result is not None
    assert isinstance(result, dict)


@pytest.mark.asyncio
async def test_get_configuration_top_level(sample_scope):
    """Test configuration retrieval for top-level key."""
    result = await get_configuration("logging", sample_scope)

    assert result is not None
    assert isinstance(result, dict)
    assert "level" in result or "format" in result


@pytest.mark.asyncio
async def test_get_configuration_not_found(sample_scope):
    """Test configuration retrieval for missing key."""
    result = await get_configuration("nonexistent.key", sample_scope)

    assert result is None


@pytest.mark.asyncio
async def test_get_configuration_deep_nesting(sample_scope):
    """Test configuration retrieval for deep nested key."""
    result = await get_configuration("marketplace.cache_ttl", sample_scope)

    assert result is not None


@pytest.mark.asyncio
async def test_create_audit_logger(sample_scope):
    """Test audit logger creation."""
    logger = await create_audit_logger("test-service", sample_scope)

    assert logger is not None
    assert logger.name == "csscore.audit.test-service"
    assert len(logger.handlers) > 0


@pytest.mark.asyncio
async def test_create_audit_logger_idempotent(sample_scope):
    """Test that creating logger multiple times is idempotent."""
    logger1 = await create_audit_logger("test-service-2", sample_scope)
    logger2 = await create_audit_logger("test-service-2", sample_scope)

    # Same logger instance
    assert logger1 is logger2


@pytest.mark.asyncio
async def test_create_audit_logger_different_services(sample_scope):
    """Test creating loggers for different services."""
    logger1 = await create_audit_logger("service-1", sample_scope)
    logger2 = await create_audit_logger("service-2", sample_scope)

    assert logger1.name != logger2.name
    assert "service-1" in logger1.name
    assert "service-2" in logger2.name


@pytest.mark.asyncio
async def test_get_scope_context_all_levels():
    """Test scope context creation for all levels."""
    for level in ScopeLevel:
        scope = await get_scope_context(level, f"runtime-{level.value}", "/tmp/test")

        assert scope.scope_level == level
        assert scope.runtime_id == f"runtime-{level.value}"
        assert scope.worktree_path == "/tmp/test"
        assert scope.project_id is None
        assert scope.session_id is None


@pytest.mark.asyncio
async def test_get_scope_context_global():
    """Test scope context creation for global level."""
    scope = await get_scope_context(
        ScopeLevel.GLOBAL, "runtime-global", "/tmp/csscore-test"
    )

    assert scope.scope_level == ScopeLevel.GLOBAL
    assert scope.runtime_id == "runtime-global"
    assert scope.worktree_path == "/tmp/csscore-test"


@pytest.mark.asyncio
async def test_get_scope_context_session():
    """Test scope context creation for session level."""
    scope = await get_scope_context(
        ScopeLevel.SESSION, "runtime-session", "/tmp/csscore-test"
    )

    assert scope.scope_level == ScopeLevel.SESSION
    assert scope.runtime_id == "runtime-session"


@pytest.mark.asyncio
async def test_scope_context_fields(sample_scope):
    """Test all fields of scope context."""
    assert sample_scope.scope_level == ScopeLevel.RUNTIME
    assert sample_scope.runtime_id == "runtime-001"
    assert sample_scope.worktree_path == "/tmp/csscore-test"
    assert sample_scope.project_id is None
    assert sample_scope.session_id is None


@pytest.mark.asyncio
async def test_marketplace_registry_structure():
    """Test marketplace registry has expected structure."""
    registry = await get_marketplace_registry()

    for _mcp_name, mcp_data in registry.items():
        assert "version" in mcp_data
        assert "dependencies" in mcp_data
        assert isinstance(mcp_data["dependencies"], list)
        assert "tools" in mcp_data
        assert isinstance(mcp_data["tools"], list)


@pytest.mark.asyncio
async def test_discover_assets_scope_context(sample_scope):
    """Test that discovered assets include scope context."""
    assets = await discover_assets(sample_scope)

    for asset in assets:
        assert "scope" in asset
        assert asset["scope"]["scope_level"] == ScopeLevel.RUNTIME.value
        assert asset["scope"]["runtime_id"] == "runtime-001"


@pytest.mark.asyncio
async def test_scope_level_enum_values():
    """Test ScopeLevel enum has all expected values."""
    levels = list(ScopeLevel)

    assert len(levels) == 5
    assert ScopeLevel.GLOBAL in levels
    assert ScopeLevel.APP in levels
    assert ScopeLevel.PROJECT in levels
    assert ScopeLevel.RUNTIME in levels
    assert ScopeLevel.SESSION in levels


@pytest.mark.asyncio
async def test_marketplace_registry_csscore_tools():
    """Test csscore is in registry with all core tools."""
    registry = await get_marketplace_registry()
    csscore_tools = registry["csscore"]["tools"]

    expected_tools = [
        "get_marketplace_registry",
        "discover_assets",
        "get_configuration",
        "create_audit_logger",
        "get_scope_context",
    ]
    for tool in expected_tools:
        assert tool in csscore_tools
