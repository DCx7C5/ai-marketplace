# MCP Dependency Graph & Installation Order

This document maps dependencies between 12 externalized MCPs and establishes the correct installation order for bootstrap.

## Dependency Analysis

### Foundation Level (No Dependencies)

**database-tools** (Phase 2)
- Provides: Core database initialization, Tortoise ORM patterns, migrations
- Required by: All other 11 MCPs
- Tools: 12
- Critical: YES

### Mid-Tier Level (Depend on Foundation)

**forensic-vault** (Phase 2)
- Dependencies: → database-tools
- Provides: Case management, findings storage, knowledge base queries
- Required by: incident_management, threat_intelligence
- Tools: 6
- Critical: YES

**network-layers** (Phase 2)
- Dependencies: → database-tools
- Provides: Network protocol analysis, connection tracing
- Required by: (none, but recommended for orchestration)
- Tools: 9
- Critical: NO

**threat-intelligence** (Phase 2)
- Dependencies: → database-tools, forensic-vault
- Provides: IOC enrichment, MITRE mapping, threat intelligence queries
- Required by: incident_management (optional)
- Tools: 14
- Critical: NO

### Upper-Tier Level (Depend on Mid-Tier)

**incident-management** (Phase 3)
- Dependencies: → database-tools, forensic-vault
- Provides: Finding management, case operations, incident tracking
- Required by: orchestration
- Tools: 18
- Critical: YES

**session-management** (Phase 3)
- Dependencies: → database-tools
- Provides: User authentication, session tracking, scope context
- Required by: All MCPs (for multi-user support)
- Tools: 7
- Critical: YES

**advanced-analysis** (Phase 3)
- Dependencies: → database-tools
- Provides: Extended thinking, structured analysis output
- Required by: (optional, power-user feature)
- Tools: 5
- Critical: NO

### Operational Level (Depend on Others or Standalone)

**browser-automation** (Phase 4)
- Dependencies: → database-tools
- Provides: Browser reconnaissance, JavaScript execution
- Required by: (optional)
- Tools: 4
- Critical: NO

**utility-tools** (Phase 4)
- Dependencies: → database-tools
- Provides: QoL helpers, data transformations
- Required by: (optional, recommended)
- Tools: 6
- Critical: NO

**business-tools** (Phase 4)
- Dependencies: → database-tools
- Provides: PoC tracking, pricing, business metrics
- Required by: (optional)
- Tools: 7
- Critical: NO

### Aggregator Level (Depends on All)

**orchestration** (Phase 4)
- Dependencies: → All other 11 MCPs
- Provides: Tool orchestration, multi-MCP workflows, automation
- Required by: (none, but should be installed last)
- Tools: 10
- Critical: YES

**dystopian-actors** (Phase 5)
- Dependencies: → database-tools (optional: incident_management, threat_intelligence)
- Provides: Red team simulation, APT behavior training
- Required by: (optional, training/simulation)
- Tools: 12
- Critical: NO

## Installation Order

For bootstrapping, MCPs **must** be installed in this dependency order:

```
Level 1 (Foundation):
  1. database-tools          (no deps)

Level 2 (Mid-tier):
  2. forensic-vault         (→ database-tools)
  3. network-layers         (→ database-tools)
  4. threat-intelligence    (→ database-tools, forensic-vault)

Level 3 (Upper-tier):
  5. incident-management    (→ database-tools, forensic-vault)
  6. session-management     (→ database-tools)
  7. advanced-analysis      (→ database-tools)

Level 4 (Operational):
  8. browser-automation     (→ database-tools)
  9. utility-tools          (→ database-tools)
  10. business-tools        (→ database-tools)
  11. dystopian-actors      (→ database-tools)

Level 5 (Aggregator):
  12. orchestration         (→ all others, install LAST)
```

## Phase Extraction Plan Validation

- **Phase 2** extracts: database-tools, forensic-vault, network-layers, threat-intelligence
  - Rationale: Foundation + mid-tier MCPs with minimal cross-dependencies
  - No circular deps: ✓
  - Can be installed in order: ✓

- **Phase 3** extracts: incident-management, session-management, advanced-analysis
  - Rationale: Depend on Phase 2 MCPs
  - Can be installed after Phase 2: ✓
  - No new circular deps: ✓

- **Phase 4** extracts: browser-automation, utility-tools, business-tools, orchestration
  - Rationale: Operational MCPs + aggregator
  - Orchestration depends on all Phase 2-3: ✓
  - Install orchestration last: ✓

- **Phase 5** extracts: dystopian-actors
  - Rationale: Special/optional MCP
  - Can be installed anytime after Phase 2: ✓

## Dependency Constraints in pyproject.toml

Each MCP explicitly declares its dependencies:

```toml
# Example: incident_management/pyproject.toml
[project]
name = "ai-marketplace-mcp-incident-management"
dependencies = [
    "cybersecsuite-mcp-core==0.1.0",
    "pydantic>=2.0",
    "tortoise-orm>=0.21.0",
    "ai-marketplace-mcp-database-tools>=0.1.0",
    "ai-marketplace-mcp-forensic-vault>=0.1.0",
]
```

Version constraints:
- Core package: Always pinned (==0.1.0)
- Other MCPs: Allow minor updates (>=0.1.0)
- External: Allow patches (>=2.0)

## Bootstrap Dependency Resolution (Phase 7)

The bootstrap installer must respect dependencies:

```python
# scripts/bootstrap-mcps.py (Phase 7)

def install_mcp_with_dependencies(mcp_name, registry):
    """Recursively install MCP and all required MCPs."""
    if is_installed(mcp_name):
        return True
    
    # Get dependencies for this MCP
    deps = get_mcp_dependencies(mcp_name)
    
    # Install each dependency first
    for dep_name in deps:
        if not install_mcp_with_dependencies(dep_name, registry):
            log.error(f"Failed to install dependency {dep_name} for {mcp_name}")
            return False
    
    # Now install this MCP
    if download_and_install(mcp_name):
        registry[mcp_name] = {
            "version": "0.1.0",
            "installed": datetime.now().isoformat(),
            "dependencies": deps
        }
        return True
    else:
        return False

# When user requests: cybersecsuite mcp install orchestration
# Bootstrap will automatically install:
#   database-tools → forensic-vault → incident-management → orchestration
# In correct dependency order
```

## Circular Dependency Check

**Result:** ✓ No circular dependencies detected

Verification:
- database-tools: depends on nothing
- forensic-vault: depends on database-tools only
- incident-management: depends on database-tools, forensic-vault (both one-directional)
- orchestration: depends on all others (one-directional)
- All dependencies form DAG (directed acyclic graph)

## CI/CD Testing: Random Installation Order

**Test:** Install all 12 MCPs in random order, verify success

```bash
# scripts/test_mcp_dependency_resolution.py

for permutation in all_permutations(12_mcps):
    # Install MCPs in random order
    for mcp in permutation:
        result = install_mcp(mcp)
        if not result:
            fail(f"Installation order {permutation} failed at {mcp}")
    
    # Verify all tools discoverable
    all_tools = discover_tools()
    assert len(all_tools) == 99, "Tool count mismatch"
    
    # Clean up for next iteration
    uninstall_all()

print("✓ All 12 MCPs install successfully in any order")
```

Expected: All permutations succeed (dependency resolution working)

## Testing Scenarios

1. **Sequential Install (Happy Path)**
   - Install in order: Phase 2 → Phase 3 → Phase 4 → Phase 5
   - Expected: All succeed

2. **Out-of-Order Install (Dependency Resolution)**
   - Try: orchestration (should auto-install all deps)
   - Expected: All 12 MCPs installed, all deps satisfied

3. **Partial Install (Explicit Selection)**
   - Install only: database-tools, forensic-vault, incident-management
   - Expected: Succeeds, session-management/other not installed

4. **Skip Level (Dependency Failure)**
   - Try: Install incident-management without database-tools
   - Expected: Auto-installs database-tools first, then incident-management

## Success Criteria

✓ All 12 MCPs mapped with explicit dependencies
✓ No circular dependencies exist
✓ Installation order derived from dependency graph
✓ Bootstrap installer respects dependency order
✓ Random installation order test passes
✓ Partial installation works (with dep resolution)
✓ Phase extraction plan validated against graph
