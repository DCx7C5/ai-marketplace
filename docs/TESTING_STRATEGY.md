# Testing & Validation Strategy for MCP Externalization

Comprehensive CI/CD checklist for Phases 1-9 to catch issues early and enable confident rollout.

## Pre-Phase-1 Validation

**Before foundation work starts:**

- [ ] Tool count verification
  ```bash
  python scripts/audit_tool_inventory.py
  # Expected output: 99 tools found, 0 orphans, 0 collisions
  ```

- [ ] Helper import audit
  ```bash
  python scripts/audit_helper_imports.py
  # Expected: helpers mapped to core package modules
  ```

- [ ] Dependency audit
  ```bash
  python scripts/audit_dependencies.py
  # Expected: no circular dependencies, clean DAG
  ```

- [ ] Baseline tests pass
  ```bash
  pytest cybersecsuite/tests/ -q
  # Expected: all tests green (baseline for regression testing)
  ```

---

## Phase 1: Foundation Validation

**After MCP template created:**

- [ ] Template structure valid
  ```bash
  python -m py_compile mcps/template/src/template/__init__.py
  # Expected: success (no syntax errors)
  ```

- [ ] pyproject.toml schema valid
  ```bash
  python -c "import toml; toml.load('mcps/template/pyproject.toml')"
  # Expected: success (valid TOML)
  ```

- [ ] CI/CD workflow valid YAML
  ```bash
  yamllint .github/workflows/mcp-validation.yml
  # Expected: no errors
  ```

---

## Phase 2-5: MCP Extraction Validation

**For each extracted MCP (12 total):**

### Tool Uniqueness

- [ ] No two MCPs export same tool name
  ```bash
  python -c "
  import json
  tools = set()
  for mcp in mcps/*/tools.json:
      for tool in json.load(open(mcp))['tools']:
          assert tool['name'] not in tools
          tools.add(tool['name'])
  print(f'✓ {len(tools)} unique tool names')
  "
  ```

- [ ] All tools follow namespace pattern
  ```bash
  rg "mcp__\w+__\w+" mcps/*/src --type py | \
    grep -v "^mcp__[a-z_]+__[a-z_]+$" && exit 1 || echo "✓ All tools follow pattern"
  ```

- [ ] No naming collisions
  ```bash
  CI/CD: python tests/test_tool_uniqueness.py
  # Expected: exit code 0
  ```

### Dependency Resolution

- [ ] All MCPs install in order (Phase 2→3→4→5)
  ```bash
  for phase in 2 3 4 5; do
    python -m pip install mcps/*/ --quiet
    python -c "import incident_management; incident_management_server"
    echo "✓ Phase $phase MCPs installed successfully"
  done
  ```

- [ ] Install in random order succeeds
  ```bash
  CI/CD (matrix test):
  for permutation in shuffled_mcps:
    pip install permutation/... --quiet
    assert all_tools_discoverable()
    cleanup()
  echo "✓ All permutations succeeded"
  ```

- [ ] No circular dependencies
  ```bash
  python scripts/detect_circular_deps.py
  # Expected: "No circular dependencies detected"
  ```

### Import Validation

- [ ] Each MCP imports only from cybersecsuite_mcp_core
  ```bash
  python -c "
  import ast
  for mcp in glob('mcps/*/src/*.py'):
      tree = ast.parse(open(mcp).read())
      for node in ast.walk(tree):
          if isinstance(node, ast.ImportFrom):
              assert 'cybersecsuite_mcp_core' in node.module or \
                     'pydantic' in node.module, \
                     f'Bad import in {mcp}: {node.module}'
  "
  # Expected: no AssertionError
  ```

- [ ] No direct imports between MCPs
  ```bash
  rg "from ai_marketplace_mcp_" mcps/*/src --type py && exit 1 || echo "✓ No inter-MCP imports"
  ```

- [ ] All imports resolve (no dangling references)
  ```bash
  for mcp in mcps/*/; do
    python -m pytest $mcp/tests/test_imports.py --tb=short
  done
  ```

---

## Phase 6: Testing & Integration

**After all MCPs extracted and tested:**

### Tool Discovery

- [ ] CyberSecSuite discovers all 99 tools
  ```bash
  python -c "
  from cybersecsuite.utils.tool_seeds import discover_tools_from_marketplace
  tools = discover_tools_from_marketplace()
  assert len(tools) == 99, f'Expected 99 tools, got {len(tools)}'
  print(f'✓ All {len(tools)} tools discovered')
  "
  ```

- [ ] Manifest-based discovery works (tools.json)
  ```bash
  CI/CD: python tests/test_tool_discovery_manifest.py
  # Expected: discovers 99 tools from manifests
  ```

- [ ] Dynamic import discovery works (get_tools())
  ```bash
  CI/CD: python tests/test_tool_discovery_dynamic.py
  # Expected: discovers 99 tools from get_tools()
  ```

- [ ] Fallback logic correct
  ```bash
  CI/CD: Test with broken manifests → should use dynamic import
  CI/CD: Test with missing get_tools() → should use manifest
  ```

### Tool Name Validation

- [ ] Tool name mapping complete
  ```bash
  python scripts/validate_tool_mapping.py
  # Expected: 99 old → new mappings, no orphans
  ```

- [ ] No collisions across 12 MCPs
  ```bash
  python -c "
  tools = {}
  for mcp in mcps/*/tools.json:
      for tool in load_json(mcp)['tools']:
          assert tool['name'] not in tools, f'Collision: {tool[\"name\"]}'
          tools[tool['name']] = mcp
  print(f'✓ {len(tools)} unique tool names across all MCPs')
  "
  ```

### Skill Integrity (Pre-Cleanup)

- [ ] All 799 skills load without errors
  ```bash
  CI/CD: python tests/validate_skills.py --all
  # Expected: 799 skills parsed successfully
  ```

- [ ] Tool references are valid (tools exist in MCPs)
  ```bash
  CI/CD: python tests/validate_skill_references.py
  # Expected: all tool references found
  ```

- [ ] Markdown parsing succeeds
  ```bash
  for skill in templates/skills/*/*.md; do
    python -c "import markdown; markdown.markdown(open('$skill').read())"
  done
  echo "✓ All skills parse as valid markdown"
  ```

- [ ] Baseline: X skills broken (or 0)
  ```bash
  python tests/validate_skills.py --baseline
  # Output: "Baseline: 0 skills broken"
  ```

---

## Phase 7: Bootstrap Verification

**After bootstrap installer created:**

### Bootstrap Installation

- [ ] 7 core MCPs download correctly
  ```bash
  CI/CD (mock marketplace):
  python scripts/bootstrap-mcps.py --core-only --mock-marketplace
  # Expected: all 7 MCPs downloaded
  ```

- [ ] Installation time < 2 minutes (99th percentile)
  ```bash
  CI/CD: time bootstrap-mcps.py --mock
  # Expected: < 120 seconds
  ```

- [ ] Registry file created (~/.cybersecsuite/INSTALLED.json)
  ```bash
  python -c "
  import json
  from pathlib import Path
  registry = Path.home() / '.cybersecsuite' / 'INSTALLED.json'
  assert registry.exists(), 'Registry file not created'
  data = json.load(open(registry))
  assert len(data) == 7, f'Expected 7 MCPs, got {len(data)}'
  print(f'✓ Registry created with {len(data)} core MCPs')
  "
  ```

### Post-Bootstrap Verification

- [ ] All 99 tools still discoverable
  ```bash
  python -c "
  from cybersecsuite.utils.tool_seeds import discover_tools_from_marketplace
  tools = discover_tools_from_marketplace()
  assert len(tools) == 99
  print(f'✓ All {len(tools)} tools discoverable post-bootstrap')
  "
  ```

- [ ] Registry integrity check
  ```bash
  python scripts/verify_registry.py
  # Expected: all MCPs valid, all versions correct, hashes match
  ```

- [ ] Restart persistence
  ```bash
  python -c "
  # Simulate app restart
  import cybersecsuite
  cybersecsuite.init()
  # Registry should still exist, tools should load
  assert len(discover_tools()) == 99
  print('✓ Tools persist across restart')
  "
  ```

---

## Phase 8: Skills Cleanup

**After skill reference migration:**

### Pre-Migration Snapshot

- [ ] Current state captured
  ```bash
  python tests/validate_skills.py --baseline > baseline.txt
  # Output: "Baseline: 0 skills with broken tool refs"
  ```

### Migration Execution

- [ ] Tool name mapping complete
  ```bash
  python scripts/generate_tool_mapping.py --validate
  # Expected: 99 mappings, no gaps, no collisions
  ```

- [ ] Skills rewritten correctly
  ```bash
  python scripts/migrate_skill_tool_references.py --all
  # Expected: all 799 skills updated, markdown valid
  ```

### Post-Migration Validation

- [ ] No old tool names remain
  ```bash
  grep -r "mcp__cybersec__" templates/skills/ && exit 1 || echo "✓ No old tool names"
  ```

- [ ] All new tool names are valid
  ```bash
  python tests/validate_skill_references.py --post-migration
  # Expected: all tool references found, no errors
  ```

- [ ] Markdown integrity maintained
  ```bash
  for skill in templates/skills/*/*.md; do
    python -c "import markdown; markdown.markdown(open('$skill').read())"
  done
  echo "✓ All skills still valid markdown"
  ```

- [ ] No skill functionality loss
  ```bash
  python tests/validate_skills.py --post-migration > post_migration.txt
  diff baseline.txt post_migration.txt
  # Expected: no new broken skills
  ```

---

## Phase 9: Skills Migration to Marketplace

**After skills moved to ai-marketplace:**

- [ ] All 19 domains copied
  ```bash
  python -c "
  import os
  domains = set(d for d in os.listdir('ai-marketplace/skills') if os.path.isdir(f'ai-marketplace/skills/{d}'))
  assert len(domains) == 19, f'Expected 19 domains, got {len(domains)}'
  print(f'✓ All {len(domains)} domains in marketplace')
  "
  ```

- [ ] File counts match
  ```bash
  csmcp_count=$(find cybersecsuite/templates/skills -name "*.md" | wc -l)
  marketplace_count=$(find ai-marketplace/skills -name "*.md" | wc -l)
  assert [ "$csmcp_count" -eq "$marketplace_count" ]
  echo "✓ File counts match: $marketplace_count skills"
  ```

- [ ] CyberSecSuite skill loader updated
  ```bash
  python -c "
  # Test that CyberSecSuite can load skills from marketplace
  from cybersecsuite.utils import skill_loader
  skills = skill_loader.load_all()
  assert len(skills) == 799, f'Expected 799 skills, got {len(skills)}'
  print(f'✓ All {len(skills)} skills loaded from marketplace')
  "
  ```

---

## Final Integration Test

**After all phases complete:**

- [ ] Fresh install works end-to-end
  ```bash
  # Clean environment
  rm -rf ~/.cybersecsuite/
  
  # Install latest CyberSecSuite
  pip install cybersecsuite
  
  # Run first-start
  cybersecsuite init
  
  # Verify
  cybersecsuite test --tools
  # Expected: ✓ 99/99 tools verified
  
  cybersecsuite skills list
  # Expected: ✓ 799 skills loaded
  ```

- [ ] All tools functional
  ```bash
  python tests/test_all_tools.py
  # Expected: all 99 tools callable, no errors
  ```

- [ ] All skills functional
  ```bash
  python tests/validate_skills.py --full
  # Expected: all 799 skills parse and reference valid tools
  ```

- [ ] No regressions vs baseline
  ```bash
  pytest cybersecsuite/tests/ -q
  # Expected: same pass rate as Phase 1 baseline
  ```

---

## Rollback Procedures

**If validation fails at any phase:**

### Phase 1-2 (Template/Extraction)
1. Stop extraction (don't push broken MCPs)
2. Fix issues in template/csmcp
3. Re-run validation
4. Resume from next MCP

### Phase 3-5 (More Extractions)
1. Revert last extracted MCP
2. Fix dependencies
3. Re-extract with corrected deps
4. Resume extraction

### Phase 6 (Testing)
1. Fix MCP code based on test failures
2. Re-run tests until passing
3. Resume next phase

### Phase 7 (Bootstrap)
1. If bootstrap fails: restore embedded MCPs
2. Fix bootstrap installer
3. Test with mocks
4. Re-run deployment

### Phase 8 (Skills Cleanup)
1. If skills break: restore from git backup
2. Fix tool name mapping
3. Re-run migration with fixed mapping
4. Validate before committing

### Phase 9 (Skills Migration)
1. If migration fails: keep skills in csmcp as fallback
2. Fix migration script
3. Re-run to marketplace
4. Verify loader works

---

## Success Criteria (Must All Pass)

**Phases 1-6:**
✓ All 12 MCPs extracted without errors
✓ All tool names unique (no collisions)
✓ All dependencies resolve correctly
✓ All 99 tools discoverable
✓ All imports valid (no dangling refs)
✓ >70% test coverage per MPC
✓ All CI/CD checks passing

**Phase 7:**
✓ Bootstrap completes in <2 minutes
✓ Registry created with 7 core MCPs
✓ All 99 tools discoverable post-bootstrap
✓ Restart persistence verified

**Phase 8:**
✓ All 799 skills migrated to new tool names
✓ Zero new broken skills (post = baseline)
✓ Markdown integrity maintained
✓ No old tool names remain

**Phase 9:**
✓ All 19 domains copied to marketplace
✓ File counts match (799 files)
✓ CyberSecSuite loads skills from marketplace
✓ All 799 skills still functional

**Final:**
✓ Fresh install: all 99 tools + 799 skills
✓ All regression tests passing
✓ Zero user-facing breakage
✓ Rollback procedures ready
