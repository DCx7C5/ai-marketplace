---
name: devel-jb-codebase-audit
description: **Scope**: This skill only READS and REPORTS. It does not modify any files. Use `implement-feature` to fix issues or `update-docs` to fix documentation gaps.
domain: cybersecurity
---
--------|-------------|--------------|
| install   | --force     | OK           |
| install   | --into      | UNDOCUMENTED |

### Specs (N issues)
| Spec File            | Status      |
|----------------------|-------------|
| copy-sync-mode.md    | IMPLEMENTED |
| some-feature.md      | MISMATCH    |

### Test Coverage (N issues)
| Command   | Status  | Notes              |
|-----------|---------|--------------------|
| sync      | COVERED |                    |
| audit     | PARTIAL | missing edge cases |
| target    | MISSING |                    |

### Targets (N issues)
| Target    | Status     | Notes         |
|-----------|------------|---------------|
| claude    | OK         |               |
| newagent  | INCOMPLETE | no project_path |

== Summary: X OK / Y issues found ==
```

### 5. Handler Split Audit

For commands with >300 lines in `cmd/skillshare/<cmd>.go`, verify the handler split convention is followed:

```bash
# Find large command files
wc -l cmd/skillshare/*.go | sort -rn | head -20
```

Check that large commands are properly split:

| Suffix | Expected for large commands |
|--------|---------------------------|
| `_handlers.go` | Core logic extracted |
| `_render.go` | Output rendering separated |
| `_tui.go` | TUI components isolated |

Report:
- **SPLIT**: Large command properly follows handler split convention
- **MONOLITH**: >300 lines without split (should be refactored)
- **N/A**: Small command, no split needed

### 6. Oplog Coverage

Verify all mutating commands have oplog instrumentation:

```bash
# Find commands that modify state
grep -rn 'func handle\|func cmd' cmd/skillshare/*.go

# Check for oplog.Write calls
grep -rn 'oplog.Write' cmd/skillshare/
```

Mutating commands (install, uninstall, sync, update, init, collect, backup, restore, trash) should all write to oplog. Read-only commands (list, status, check, search, audit, log, version) should not.

Report:
- **INSTRUMENTED**: Mutating command has oplog.Write
- **MISSING**: Mutating command lacks oplog instrumentation
- **N/A**: Read-only command (no oplog expected)

### 7. Web API Consistency

Verify `internal/server/handler_*.go` routes match CLI commands:

```bash
# List all handler files
ls internal/server/handler_*.go | grep -v _test.go

# Check route registration in server.go
grep -n 'HandleFunc\|Handle(' internal/server/server.go
```

Report:
- **SYNCED**: CLI command has corresponding API handler
- **CLI-ONLY**: Command exists in CLI but not in Web API (may be intentional)
- **API-ONLY**: API handler without CLI counterpart (unusual)

## Output Format

```
== Skillshare Codebase Audit ==

### CLI Flags (N issues)
| Command   | Flag        | Status       |
|-----------|-------------|--------------|
| install   | --force     | OK           |
| install   | --into      | UNDOCUMENTED |

### Specs (N issues)
| Spec File            | Status      |
|----------------------|-------------|
| copy-sync-mode.md    | IMPLEMENTED |
| some-feature.md      | MISMATCH    |

### Test Coverage (N issues)
| Command   | Status  | Notes              |
|-----------|---------|--------------------|
| sync      | COVERED |                    |
| audit     | PARTIAL | missing edge cases |
| target    | MISSING |                    |

### Targets (N issues)
| Target    | Status     | Notes         |
|-----------|------------|---------------|
| claude    | OK         |               |
| newagent  | INCOMPLETE | no project_path |

### Handler Split (N issues)
| Command   | Lines | Status    | Notes              |
|-----------|-------|-----------|--------------------|
| install   | 450   | SPLIT     | 6 sub-files        |
| audit     | 320   | MONOLITH  | should split render |
| status    | 80    | N/A       |                    |

### Oplog (N issues)
| Command   | Mutating? | Status        |
|-----------|-----------|---------------|
| install   | Yes       | INSTRUMENTED  |
| trash     | Yes       | MISSING       |
| list      | No        | N/A           |

### Web API (N issues)
| Command   | CLI | API | Status   |
|-----------|-----|-----|----------|
| install   | Yes | Yes | SYNCED   |
| diff      | Yes | No  | CLI-ONLY |

== Summary: X OK / Y issues found ==
```

## Rules

- **Read-only** — never modify files, only report
- **Evidence-based** — every finding must include file path and line number
- **No false positives** — verify with grep before flagging
- **Scope $ARGUMENTS** — if user specifies "flags", only run dimension 1; "handlers" for dimension 5, "oplog" for dimension 6, "api" for dimension 7