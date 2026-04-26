"""
CyberSecSuite Core MCP Package

Foundation module providing essential services for all externalized MCPs:
- Marketplace registry access
- Asset discovery & enumeration
- Configuration management
- Core logging & audit
- Scope & context management
"""

from mcp_csscore.core import (
    MarketplaceRegistry,
    ScopeContext,
    ScopeLevel,
    create_audit_logger,
    discover_assets,
    get_configuration,
    get_marketplace_registry,
    get_scope_context,
)

__version__ = "1.0.0"
__author__ = "CyberSecSuite Contributors"
__license__ = "MIT"

__all__ = [
    "__version__",
    "__author__",
    "__license__",
    "ScopeLevel",
    "ScopeContext",
    "MarketplaceRegistry",
    "get_marketplace_registry",
    "discover_assets",
    "get_configuration",
    "create_audit_logger",
    "get_scope_context",
]
