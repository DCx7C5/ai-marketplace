# Marketplace Metadata Schema

**Version:** 1.0  
**Status:** Production  
**Date:** 2026-04-26  

## Overview

This document defines the canonical metadata schema for all marketplace assets (tools, skills, MCPs). Metadata enables discovery, categorization, versioning, and compatibility tracking.

## Schema Structure

### Tool-Level Metadata

```json
{
  "id": "unique-tool-id",
  "name": "Tool Display Name",
  "version": "1.0.0",
  "category": "category/subcategory",
  "mcp": "parent-mcp-id",
  "status": "available|deprecated|experimental",
  "description": "Detailed description of tool functionality",
  "tags": ["tag1", "tag2", "tag3"],
  "keywords": ["keyword1", "keyword2"],
  "author": "author-name",
  "license": "MIT|Apache-2.0|etc",
  "homepage": "https://example.com",
  "repository": "https://github.com/example/repo",
  "documentation": "https://docs.example.com",
  "parameters": {
    "param_name": {
      "type": "string|number|boolean|object|array",
      "description": "Parameter description",
      "required": true,
      "default": "default-value",
      "enum": ["option1", "option2"]
    }
  },
  "returns": {
    "type": "object|string|array",
    "description": "Return value description",
    "schema": {}
  },
  "dependencies": [
    {
      "name": "dependency-name",
      "version": ">=1.0.0",
      "mcp": "mcp-id"
    }
  ],
  "rating": 4.5,
  "downloads": 1250,
  "compatibility": {
    "minVersion": "1.0.0",
    "maxVersion": "2.0.0",
    "platforms": ["linux", "macos", "windows"]
  },
  "examples": [
    {
      "description": "Example description",
      "code": "example code block"
    }
  ],
  "metadata": {
    "created": "2026-01-01T00:00:00Z",
    "modified": "2026-04-26T00:00:00Z",
    "maintainer": "maintainer-email@example.com"
  }
}
```

### Skill-Level Metadata

```json
{
  "id": "unique-skill-id",
  "name": "Skill Display Name",
  "category": "category/subcategory",
  "skill_type": "detect|analyze|exploit|monitor|audit|etc",
  "path": "path/to/SKILL.md",
  "tags": ["tag1", "tag2"],
  "description": "Brief skill description",
  "file_size": 5000,
  "status": "available|deprecated|experimental",
  "tier": "blue|red|purple",
  "dependencies": ["skill-id-1", "skill-id-2"],
  "metadata": {
    "created": "2026-01-01T00:00:00Z",
    "modified": "2026-04-26T00:00:00Z"
  }
}
```

### MCP-Level Metadata

```json
{
  "id": "mcp-id",
  "name": "MCP Display Name",
  "version": "1.0.0",
  "status": "available|deprecated|experimental",
  "pythonPackage": "mcp-python-package-name",
  "description": "MCP description and capabilities",
  "modules": 22,
  "tools": 85,
  "categories": [
    {
      "name": "category-name",
      "count": 10,
      "tools": ["tool-id-1", "tool-id-2"]
    }
  ],
  "dependencies": ["csscore-mcp", "dystopian-crypto-mcp"],
  "metadata": {
    "created": "2026-01-01T00:00:00Z",
    "modified": "2026-04-26T00:00:00Z",
    "maintainer": "maintainer-email@example.com"
  }
}
```

## Required Fields

### For Tools:
- `id`: Unique identifier (kebab-case, alphanumeric + hyphens)
- `name`: Display name (max 100 chars)
- `version`: SemVer format (MAJOR.MINOR.PATCH)
- `category`: Hierarchical category (e.g., "forensics/memory")
- `mcp`: Parent MCP identifier
- `status`: One of: `available`, `deprecated`, `experimental`
- `description`: Clear description of functionality
- `parameters`: At minimum, parameter types and descriptions

### For Skills:
- `id`: Unique identifier
- `name`: Display name
- `category`: Category path
- `skill_type`: Type of skill (detect, analyze, exploit, monitor, audit)
- `status`: availability status
- `tags`: Categorization tags

### For MCPs:
- `id`: Unique identifier
- `name`: Display name
- `version`: SemVer version
- `status`: Availability status
- `description`: Capabilities description

## Optional Fields

- `keywords`: Search keywords beyond name/description
- `rating`: Numeric rating (0-5) from user reviews
- `downloads`: Download/usage count
- `compatibility`: Platform and version compatibility
- `author`: Author/creator name
- `license`: SPDX license identifier
- `homepage`: Official website
- `repository`: Version control repository
- `documentation`: Link to full documentation
- `examples`: Usage examples with code
- `tier`: Blue/Red/Purple team alignment
- `dependencies`: Tool/Skill dependencies with versions

## Versioning

Uses Semantic Versioning (SemVer):
- **MAJOR**: Incompatible API changes
- **MINOR**: Backward-compatible functionality additions
- **PATCH**: Backward-compatible bug fixes

Example: `1.2.3` = Major 1, Minor 2, Patch 3

## Categories

Standardized category hierarchy:

```
forensics/
  - memory
  - disk
  - network
  - registry
  - browser
  - application

security/
  - vulnerability
  - threat-intel
  - incident-response
  - compliance

crypto/
  - encryption
  - hashing
  - signing
  - key-management

network/
  - analysis
  - mapping
  - monitoring
  - forensics

etc...
```

## Validation Rules

1. **ID Uniqueness**: Tool `id` must be globally unique across all MCPs
2. **SemVer Format**: Version must match `\d+\.\d+\.\d+` pattern
3. **Description Length**: Min 10, max 1000 chars
4. **Name Length**: Min 1, max 100 chars
5. **Parameter Types**: Must be one of: string, number, boolean, object, array
6. **Status Values**: Must be one of: available, deprecated, experimental
7. **Rating**: Must be 0-5 (if provided)
8. **Downloads**: Must be non-negative integer

## JSON Schema Validation

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "type": "object",
  "properties": {
    "id": {
      "type": "string",
      "pattern": "^[a-z0-9-]+$",
      "minLength": 1,
      "maxLength": 100
    },
    "name": {
      "type": "string",
      "minLength": 1,
      "maxLength": 100
    },
    "version": {
      "type": "string",
      "pattern": "^\\d+\\.\\d+\\.\\d+$"
    },
    "status": {
      "type": "string",
      "enum": ["available", "deprecated", "experimental"]
    },
    "description": {
      "type": "string",
      "minLength": 10,
      "maxLength": 1000
    },
    "tags": {
      "type": "array",
      "items": {
        "type": "string",
        "minLength": 1,
        "maxLength": 50
      }
    }
  },
  "required": ["id", "name", "version", "status", "description"]
}
```

## Backwards Compatibility

- Schema version pinned to 1.0
- Fields can be added as optional in minor versions
- Breaking changes require major version increment
- Deprecated fields marked in changelog

## Examples

### Example Tool Metadata (JSON)

```json
{
  "id": "cache-lookup",
  "name": "Cache Lookup",
  "version": "1.0.0",
  "category": "cache-management",
  "mcp": "csscore-mcp",
  "status": "available",
  "description": "Look up cached information by key. Returns cached value or null if not found.",
  "tags": ["cache", "lookup", "retrieval"],
  "keywords": ["memory", "storage", "fast-access"],
  "parameters": {
    "key": {
      "type": "string",
      "description": "The cache key to look up",
      "required": true
    },
    "namespace": {
      "type": "string",
      "description": "Optional namespace for the cache key",
      "required": false,
      "default": "default"
    }
  },
  "returns": {
    "type": "object",
    "description": "Cached value or error response",
    "schema": {
      "type": "object",
      "properties": {
        "value": { "type": ["string", "object", "null"] },
        "cached_at": { "type": "string", "format": "date-time" },
        "ttl": { "type": "integer" }
      }
    }
  },
  "rating": 4.8,
  "downloads": 5230,
  "compatibility": {
    "minVersion": "1.0.0",
    "platforms": ["linux", "macos", "windows"]
  },
  "metadata": {
    "created": "2026-01-15T10:30:00Z",
    "modified": "2026-04-26T00:00:00Z",
    "maintainer": "core-team@cybersecsuite.local"
  }
}
```

### Example Skill Metadata (JSON)

```json
{
  "id": "linux-kernel-module-detection",
  "name": "Linux Kernel Module Detection",
  "category": "linux/rootkit-detection",
  "skill_type": "detect",
  "path": "linux/rootkit-detection/detect/SKILL.md",
  "tags": ["linux", "rootkit", "kernel", "modules"],
  "description": "Detect suspicious kernel modules and LKM rootkits using module enumeration and signature analysis",
  "file_size": 12500,
  "status": "available",
  "tier": "blue",
  "dependencies": ["linux-file-analysis"],
  "metadata": {
    "created": "2026-02-10T14:22:00Z",
    "modified": "2026-04-26T00:00:00Z"
  }
}
```

## Migration Notes

All existing tools and skills migrated to schema v1.0:
- Tool IDs standardized to kebab-case
- Versions normalized to SemVer
- Categories created from existing path structures
- Status inferred from availability markers
- Dependencies extracted from documentation

## Future Extensions

Planned additions for schema v2.0:
- Performance metrics and benchmarks
- Security audit trail
- Integration test results
- Deprecation timeline with migration paths
- Internationalization support (i18n)
- Custom field extensibility
