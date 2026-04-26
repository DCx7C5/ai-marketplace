# CyberSecSuite Transition Strategy: csmcp → Marketplace MCPs

This document outlines the migration path from the monolithic `csmcp` module to distributed marketplace MCPs, including timeline, backward compatibility, and user migration process.

## Current State

- **Location:** `src/csmcp/` (monolithic, 87 tools)
- **Status:** Active, primary tool provider
- **Users:** All existing CyberSecSuite installations
- **Tools:** 87 cybersec + 12 dystopian-actors = 99 total

## Desired State

- **Location:** `ai-marketplace/mcps/` (12 independent MCPs)
- **Status:** Active, primary tool provider
- **Users:** All CyberSecSuite v2.0+ installations
- **Discovery:** Dynamic (marketplace registry + installed MCPs)

## Transition Timeline

### Phase 2-7: Dual-Mode Period (Months 1-2)

**Duration:** ~6 weeks

**Status:** ACTIVE + EXPERIMENTAL

**What's happening:**
- ✓ Marketplace MCPs extracted (Phases 2-5)
- ✓ Tests written for all MCPs (Phase 6)
- ✓ Bootstrap installer built (Phase 7)
- ✓ Skills cleaned and migrated (Phases 8-9)
- ✓ csmcp still exists (unchanged)
- ✓ CyberSecSuite can use either (prioritizes marketplace)

**User behavior:**
- No action required (system auto-detects MCPs)
- Existing installations continue working
- New installations get marketplace MCPs (if available)
- Both old and new tool names work (aliases)

**Communications:**
- Blog post: "MCPs are coming! Here's what changes..."
- Documentation: "Marketplace MCPs: Overview"
- No user action required yet

**Exit criteria:**
- All 12 MCPs extracted and tested
- 799 skills cleaned and migrated
- Bootstrap installer working
- Tool discovery verified (all 99 tools discoverable)

---

### Phase 9 Complete: Marketplace Primary (Month 2 end)

**Duration:** Release day

**Status:** DEPRECATED (soft)

**Version:** CyberSecSuite v1.10.0 (final with csmcp support)

**What's happening:**
- ✓ All marketplace MCPs released to PyPI
- ✓ Skills fully migrated to marketplace
- ✓ Old tool names marked deprecated
- ✓ csmcp becomes read-only (no new features)
- ✓ CyberSecSuite prioritizes marketplace MCPs

**User behavior:**
- Can continue on v1.9.x (csmcp still active)
- Can upgrade to v1.10.0 (marketplace + csmcp)
- Tool names change: old → new (with warnings)
- Skills auto-updated (if from marketplace)

**Communications:**
- Release notes: "MCPs are here! Upgrade for new features"
- Migration guide: "How to upgrade from csmcp to MCPs"
- FAQ: "Will my tools break?"
- Support: 1-month grace period for v1.9.x issues

**Exit criteria:**
- 70% of users on v1.10.0 or later
- Zero critical bugs in marketplace MCPs
- Skill migration complete

---

### Q3 2026: Hard Deprecation (Month 3)

**Duration:** Release day

**Status:** REMOVED

**Version:** CyberSecSuite v2.0.0 (marketplace MCPs only)

**What's happening:**
- ✗ csmcp removed from repository
- ✗ Old tool names no longer work
- ✗ Users must upgrade or fall back to v1.10.x
- ✓ Marketplace MCPs are mandatory
- ✓ 7 core MCPs auto-installed on first-start

**User behavior:**
- Must upgrade to v2.0.0 (or stay on v1.10.x)
- Skills fully updated to new tool names
- Bootstrap: automatic MCP installation
- All new features require marketplace MCPs

**Communications:**
- Release notes: "CyberSecSuite v2.0: MCPs required"
- Blog: "Migration period ended: here's what changed"
- FAQ: "I'm still on v1.9, what do I do?"
- Support: v1.9.x support ends (migration assistance provided)

**Exit criteria:**
- >90% of users on v2.0.0+
- v1.9.x support ended (3-month window)
- csmcp fully removed

---

## Backward Compatibility Strategy

### Tool Name Aliasing (Phases 7-9)

Old tool names aliased to new names to prevent breaking changes:

```python
# In csmcp wrapper or compatibility layer
TOOL_ALIASES = {
    'mcp__cybersec__add_finding': 'mcp__incident_management__add_finding',
    'mcp__cybersec__get_case': 'mcp__incident_management__get_case',
    # ... all 99 mappings
}

def resolve_tool_name(old_name):
    """Resolve old name to new name, with deprecation warning."""
    if old_name in TOOL_ALIASES:
        new_name = TOOL_ALIASES[old_name]
        log.warning(f"Tool '{old_name}' deprecated. Use '{new_name}' instead.")
        return new_name
    return old_name
```

Timeline:
- **Phases 7-9:** Aliases active, warnings logged
- **v1.10.0:** Aliases still active (grace period)
- **v2.0.0:** Aliases removed, old names fail

### Gradual Deprecation Warnings

Phase-based warning escalation:

```
Phase 7: [WARN] Tool 'mcp__cybersec__X' is deprecated. Update to 'mcp__incident_management__X'
v1.10.0: [WARN] Tool 'mcp__cybersec__X' will be removed in v2.0.0
v2.0.0:  [ERROR] Tool 'mcp__cybersec__X' not found. Use 'mcp__incident_management__X'
```

### Version Checking

CyberSecSuite version gates MCP availability:

```python
# In tool_seeds.py
if __version__ >= '2.0.0':
    # Marketplace MCPs only
    discover_tools_from_marketplace()
elif __version__ >= '1.10.0':
    # Try marketplace first, fall back to csmcp
    try:
        discover_tools_from_marketplace()
    except Exception:
        discover_tools_from_csmcp()
else:
    # v1.9.x and earlier: csmcp only
    discover_tools_from_csmcp()
```

## User Migration Process

### For Existing v1.9.x Users

**Goal:** Migrate from csmcp to marketplace MCPs smoothly

**Steps:**

1. **Check compatibility**
   ```bash
   cybersecsuite check --migration
   # Output:
   #   ✓ 799 skills compatible
   #   ✓ All tools have new names
   #   ✓ Ready to upgrade
   ```

2. **Update CyberSecSuite**
   ```bash
   pip install --upgrade cybersecsuite>=2.0.0
   ```

3. **Run first-start setup**
   ```bash
   cybersecsuite init
   # Downloads and installs 7 core MCPs (~2 minutes)
   ```

4. **Verify all tools work**
   ```bash
   cybersecsuite test --tools
   # Runs smoke tests on all 99 tools
   # Output: ✓ 99/99 tools verified
   ```

5. **Optional: Install marketplace MCPs**
   ```bash
   cybersecsuite mcp install advanced-analysis
   cybersecsuite mcp install dystopian-actors
   # Install additional MCPs as needed
   ```

6. **Update skills (if needed)**
   ```bash
   cybersecsuite skills update
   # Re-downloads skills from marketplace
   # Applies new tool name references
   ```

**Estimated time:** 10-15 minutes

**Fallback:** Stay on v1.10.0 (csmcp + marketplace MCPs coexist)

### For New Installations

**Goal:** First-time users get marketplace MCPs directly

**Steps:**

1. **Install CyberSecSuite**
   ```bash
   pip install cybersecsuite>=2.0.0
   ```

2. **First-start automatically runs**
   ```bash
   cybersecsuite init
   # Auto-installs 7 core MCPs
   # Completes in <2 minutes
   ```

3. **Start using**
   ```bash
   cybersecsuite case new --title "Investigation"
   # All marketplace tools available
   ```

**No manual steps required**

## Communication Plan

### Month 1: Announcement

**Channels:** Blog, social media, email newsletter

**Message:**
```
MCPs are Coming!

We're externalizing CyberSecSuite's tools into 12 independent Marketplace MCPs
for better modularity and distribution. Here's what that means for you:

✓ More features with less bloat
✓ Install only what you need
✓ Automatic first-start setup
✓ No manual configuration

**No action required** — Your existing setup will keep working!

Learn more: [link to migration guide]
```

### Month 2: Launch Announcement

**Channels:** Blog, release notes, Discord

**Message:**
```
CyberSecSuite v2.0: MCPs Are Here!

All 99 tools are now available as independent Marketplace MCPs.
Auto-install on first-start. Opt-in marketplace install for power users.

For existing users:
- Upgrade when ready (no rush!)
- Existing skills still work (auto-migrated)
- Tool names updated (old names aliased)

For new users:
- First-start handles everything automatically
- All 7 core MCPs ready to go

Migration Guide: [link]
FAQ: [link]
```

### Month 3: End of Support

**Channels:** Email, support portal

**Message:**
```
CyberSecSuite v1.9 Support Ending

We're sunsetting support for v1.9 (csmcp-only) at [date].

To continue receiving updates:
- Upgrade to v2.0 (recommended)
- Or stay on v1.10.0 (transitional, limited support)

Migration takes ~15 minutes. Need help? [support link]
```

## Rollback Plan

**If marketplace MCPs have critical bugs:**

1. Keep csmcp available as fallback
2. Users can explicitly opt-in:
   ```bash
   export CYBERSECSUITE_PREFER_CSMCP=1
   cybersecsuite
   ```
3. Support period: 1 month (while bugs are fixed)
4. After fixes: rollback to marketplace MCPs

**If bootstrap fails:**

1. Keep local embedded MCPs as fallback
2. Skip marketplace download, use local copies
3. Try marketplace again on next startup
4. Inform user via UI: "Using offline MCPs, check internet"

## Success Metrics

**Adoption:**
- 70% of users on v1.10.0+ within 1 month (Phase 9)
- 90% of users on v2.0.0+ within 3 months (Q3)
- <5% still on v1.9.x after 3-month window

**Quality:**
- 0 tool functionality loss during transition
- <5% of skills break during migration
- >98% successful tool discovery post-transition

**User Experience:**
- First-start <2 minutes (98th percentile)
- 0 manual configuration required
- Smooth upgrade path (99% success rate)

**Support:**
- <10% increase in support tickets during Phase 9-Q3
- <5% migration-related issues post-Q3

## FAQ

**Q: Will my existing skills still work?**
A: Yes! All 799 skills are migrated with updated tool names. They'll work seamlessly post-upgrade.

**Q: Can I stay on v1.9?**
A: Yes, but with limitations. No new features. We recommend upgrading to v2.0 when ready.

**Q: How long is the migration window?**
A: We support v1.9 for 3 months post-launch. Upgrade at your own pace.

**Q: Will marketplace MCPs be available offline?**
A: Yes! 7 core MCPs are embedded in the distribution. Optional MCPs require internet for first install.

**Q: Do I have to install all 12 MCPs?**
A: No! Only 7 core MCPs auto-install. Install optional MCPs as needed.

**Q: What if I find a bug in marketplace MCPs?**
A: Report it! We'll fix it and push an update. Easy rollback available.

## Success Criteria

✓ Timeline communicated clearly
✓ User migration process is straightforward
✓ Backward compatibility during transition
✓ Deprecation warnings in place
✓ Rollback procedures documented
✓ Support team prepared
