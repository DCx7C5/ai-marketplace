# Tool Name Migration Map

Tools are being migrated from monolithic `mcp__cybersec__*` namespace to specific MCP namespaces during the 9-phase externalization (Phases 2-5).

## Migration Strategy

1. **Before Phase 2 starts:** Tool mapping document finalized (this file)
2. **During Phase 2-5:** Tools extracted into specific MCPs with new names
3. **In Phase 8:** Use this mapping to rewrite all SKILL.md tool references
4. **Result:** 799 skills reference correct new tool names post-migration

## Full Mapping Table

| Old Tool Name | New Tool Name | New MCP | Phase | Category |
|---|---|---|---|---|
| `mcp__cybersec__add_finding` | `mcp__incident_management__add_finding` | incident_management | 3 | Finding Management |
| `mcp__cybersec__get_case` | `mcp__incident_management__get_case` | incident_management | 3 | Case Management |
| `mcp__cybersec__update_finding` | `mcp__incident_management__update_finding` | incident_management | 3 | Finding Management |
| `mcp__cybersec__close_case` | `mcp__incident_management__close_case` | incident_management | 3 | Case Management |
| `mcp__cybersec__add_ioc` | `mcp__threat_intelligence__add_ioc` | threat_intelligence | 2 | IOC Management |
| `mcp__cybersec__suggest_mitre` | `mcp__threat_intelligence__suggest_mitre` | threat_intelligence | 2 | MITRE Mapping |
| `mcp__cybersec__query_intelligence` | `mcp__threat_intelligence__query_intelligence` | threat_intelligence | 2 | Intelligence Query |
| `mcp__cybersec__enrich_ioc` | `mcp__threat_intelligence__enrich_ioc` | threat_intelligence | 2 | IOC Enrichment |
| `mcp__cybersec__add_vault_finding` | `mcp__forensic_vault__add_finding` | forensic_vault | 2 | Knowledge Base |
| `mcp__cybersec__search_vault` | `mcp__forensic_vault__search` | forensic_vault | 2 | Knowledge Query |
| `mcp__cybersec__persist_artifact` | `mcp__forensic_vault__persist_artifact` | forensic_vault | 2 | Artifact Storage |
| `mcp__cybersec__query_network` | `mcp__network_layers__query` | network_layers | 2 | Network Query |
| `mcp__cybersec__trace_connection` | `mcp__network_layers__trace_connection` | network_layers | 2 | Network Tracing |
| `mcp__cybersec__analyze_protocol` | `mcp__network_layers__analyze_protocol` | network_layers | 2 | Protocol Analysis |
| `mcp__cybersec__init_session` | `mcp__session_management__init_session` | session_management | 3 | Session Management |
| `mcp__cybersec__get_user_context` | `mcp__session_management__get_user_context` | session_management | 3 | Context Retrieval |
| `mcp__cybersec__extend_session` | `mcp__session_management__extend_session` | session_management | 3 | Session Control |
| `mcp__dystopian__simulate_apt` | `mcp__dystopian_actors__simulate_apt` | dystopian_actors | 5 | APT Simulation |
| `mcp__dystopian__red_team` | `mcp__dystopian_actors__red_team` | dystopian_actors | 5 | Red Team |
| `mcp__cybersec__orchestrate_tools` | `mcp__orchestration__orchestrate_tools` | orchestration | 4 | Orchestration |

**Total mappings: 99 tools** (speculative; exact mapping auto-generated in Phase 2)

## Mapping Principles

1. **Naming Convention**
   - Format: `mcp__{mcp_name}__{function_name}`
   - All lowercase with underscores
   - MCP name matches directory name (kebab-case in dirs, snake_case in tool name)

2. **Consistency**
   - All tools from same MCP share namespace prefix
   - No cross-namespace tool names
   - Function names kept consistent where possible

3. **No Collisions**
   - Each tool name globally unique across all 12 MCPs
   - Namespace prefix prevents accidental duplicates

## Phase 8 Implementation: Skill Reference Migration

When Phase 8 runs (Skills Cleanup), this mapping is used to rewrite SKILL.md files:

```python
# scripts/migrate_skill_tool_references.py (pseudocode)
import re
from pathlib import Path

MAPPING = {
    'mcp__cybersec__add_finding': 'mcp__incident_management__add_finding',
    'mcp__cybersec__get_case': 'mcp__incident_management__get_case',
    # ... all 99 mappings
}

def migrate_skill_file(file_path):
    """Update tool references in a SKILL.md file."""
    content = Path(file_path).read_text()
    
    for old_name, new_name in MAPPING.items():
        # Replace in code blocks and text
        content = content.replace(old_name, new_name)
    
    Path(file_path).write_text(content)
    return content

def validate_after_migration():
    """Verify all new tool names exist in installed MCPs."""
    for old_name, new_name in MAPPING.items():
        if not tool_exists(new_name):
            raise ValueError(f"Tool not found after migration: {new_name}")
```

## Validation Strategy

**Before Migration (Phase 6):**
- [ ] Generate mapping from extracted MCPs
- [ ] Verify all 99 tools accounted for
- [ ] Check for gaps (old tools with no new mapping)
- [ ] Detect collisions (same new name, different old names)

**During Migration (Phase 8):**
- [ ] Run migration script on all 799 SKILL.md files
- [ ] Verify markdown integrity post-migration
- [ ] Log any unmappable references
- [ ] Report success count vs failed count

**After Migration (Phase 8 validation):**
- [ ] Scan all skills for remaining old tool names
- [ ] Verify all new tool names are valid (exist in MCPs)
- [ ] Run skill validation test suite
- [ ] Compare skill functionality before/after

## Automation in Phase 2

Early in Phase 2, run `scripts/generate_tool_mapping.py`:

```bash
python scripts/generate_tool_mapping.py \
  --source /path/to/csmcp \
  --target /path/to/ai-marketplace/mcps \
  --output tools_inventory.csv \
  --mapping-output docs/TOOL_NAME_MAPPING.md
```

This will:
1. Scan extracted MCPs for all tool definitions
2. Generate TOOL_NAME_MAPPING.md automatically
3. Output tools_inventory.csv with exact counts
4. Verify 100% mapping coverage
5. Exit code 0 (success) or 1 (gaps found)

## Success Criteria

✓ All 99 tools mapped (old → new)
✓ No orphaned tools (unmapped)
✓ No collisions (duplicate new names)
✓ All new names valid (tools exist in MCPs)
✓ All 799 skills updated with new names
✓ Zero broken skill references post-migration
✓ Phase 8 validation passes
