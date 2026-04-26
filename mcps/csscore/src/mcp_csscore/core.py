"""
Core utility functions for CyberSecSuite externalized MCPs.

Provides generic utilities for:
- Marketplace registry access
- Asset discovery
- Configuration management
- Structured logging
- Scope and context tracking
"""

import json
import logging
from dataclasses import asdict, dataclass
from enum import Enum
from typing import Any, Dict, List, Optional


class ScopeLevel(str, Enum):
    """Scope hierarchy levels for CyberSecSuite context."""

    GLOBAL = "global"
    APP = "app"
    PROJECT = "project"
    RUNTIME = "runtime"
    SESSION = "session"


@dataclass
class ScopeContext:
    """Runtime scope context for tracking execution hierarchy."""

    scope_level: ScopeLevel
    runtime_id: str
    worktree_path: str
    project_id: Optional[str] = None
    session_id: Optional[str] = None


@dataclass
class MarketplaceRegistry:
    """Marketplace registry containing MCP metadata."""

    mcp_name: str
    version: str
    dependencies: List[str]
    tools: List[str]
    metadata: Dict[str, Any]


async def get_marketplace_registry() -> Dict[str, Any]:
    """
    Query available MCPs and their metadata from marketplace registry.

    Returns:
        Dictionary mapping MCP names to their registry entries
    """
    registry: Dict[str, Any] = {
        "csscore": {
            "version": "1.0.0",
            "dependencies": [],
            "tools": [
                "get_marketplace_registry",
                "discover_assets",
                "get_configuration",
                "create_audit_logger",
                "get_scope_context",
            ],
            "description": "Core MCP foundation",
        }
    }
    return registry


async def discover_assets(
    scope: ScopeContext, asset_type: Optional[str] = None
) -> List[Dict[str, Any]]:
    """
    Enumerate discovered systems, assets, and targets.

    Args:
        scope: Execution scope context
        asset_type: Optional filter (e.g., 'host', 'network', 'credential')

    Returns:
        List of discovered assets with metadata
    """
    assets: List[Dict[str, Any]] = [
        {
            "id": "asset-001",
            "type": "host",
            "name": "target-system",
            "scope": asdict(scope),
            "metadata": {},
        }
    ]
    if asset_type:
        assets = [a for a in assets if a["type"] == asset_type]
    return assets


async def get_configuration(
    config_key: str, scope: ScopeContext
) -> Optional[Any]:
    """
    Read and validate CyberSecSuite configuration.

    Args:
        config_key: Configuration key path (e.g., 'logging.level')
        scope: Execution scope context

    Returns:
        Configuration value or None if not found
    """
    config: Dict[str, Any] = {
        "logging": {"level": "INFO", "format": "json"},
        "marketplace": {"cache_ttl": 3600, "registry_url": "local"},
    }

    parts = config_key.split(".")
    value: Any = config
    for part in parts:
        if isinstance(value, dict):
            value = value.get(part)
        else:
            return None
    return value if isinstance(value, dict) else {"value": value}


async def create_audit_logger(
    service_name: str, scope: ScopeContext
) -> logging.Logger:
    """
    Create structured audit logger for MCP operations.

    Args:
        service_name: Name of the service creating the logger
        scope: Execution scope context

    Returns:
        Configured logger with audit context
    """
    logger = logging.getLogger(f"csscore.audit.{service_name}")

    if not logger.handlers:
        handler = logging.StreamHandler()
        formatter = logging.Formatter(
            json.dumps(
                {
                    "timestamp": "%(asctime)s",
                    "service": service_name,
                    "level": "%(levelname)s",
                    "message": "%(message)s",
                }
            )
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        logger.setLevel(logging.INFO)

    return logger


async def get_scope_context(
    scope_level: ScopeLevel, runtime_id: str, worktree_path: str
) -> ScopeContext:
    """
    Retrieve or create scope and context tracking.

    Args:
        scope_level: Level in scope hierarchy
        runtime_id: Unique runtime identifier
        worktree_path: Working tree path for execution

    Returns:
        ScopeContext object with tracking metadata
    """
    return ScopeContext(
        scope_level=scope_level,
        runtime_id=runtime_id,
        worktree_path=worktree_path,
    )
