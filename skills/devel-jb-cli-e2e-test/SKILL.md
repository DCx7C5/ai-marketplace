---
name: devel-jb-cli-e2e-test
description: 1. Confirm devcontainer is running and get container ID:
domain: cybersecurity
---
---|--------|-------------|---------|
| Substring | plain text | Simple output check | `- hello world` |
| Negated | `Not`/`Should NOT` prefix | Verify absence | `- Not FAIL` |
| Exit code | `exit_code: N` | Every step should have this | `- exit_code: 0` |
| Regex | `regex:` prefix | Pattern matching | `- regex: v\d+\.\d+` |
| jq | `jq:` prefix | **JSON output (preferred)** | `- jq: .extras \| length == 1` |
| Snapshot | `snapshot:` prefix | Stable output comparison | `- snapshot: api-response` |

**`jq:` best practices:**
```markdown
# Simple field check
- jq: .name == "rules"

# Array length
- jq: .extras | length == 3

# Sorted array comparison
- jq: [.extras[].name] | sort | . == ["a","b","c"]

# Null/missing field (omitempty)
- jq: .extras == null

# Nested access
- jq: .[0].targets[0].status == "synced"

# Boolean
- jq: .source_exists == true
```

## Rules

- **Always execute inside devcontainer** — use `docker exec`, never run CLI on host
- **Always use `ssenv` for HOME isolation** — don't pollute container default HOME
- **Always create fresh ssenv environments** — never reuse an environment from a previous run; stale config/state causes confusing cascade failures (e.g. duplicate YAML keys, "already exists" errors)
- **ssenv only isolates `$HOME`** — `/tmp/`, `/var/`, and other system paths are shared across all environments. Runbook steps using `/tmp/` must include `rm -rf` cleanup at the start
- **Verify every step** — never skip Expected checks
- **Don't abort on failure** — record FAIL, continue to next step, summarize at end
- **Ask before cleanup** — Phase 4 must prompt user before deleting ssenv environment
- **`ss` = `skillshare`** — same binary in runbooks
- **`~` = ssenv-isolated HOME** — `ssenv enter` auto-sets `HOME`
- **Use `--init`** — simplify setup by using `ssenv create <name> --init`
- **`--init` already runs init** — the env is pre-initialized; runbook steps calling `ss init` again will fail unless the step explicitly resets state first

## ssenv Quick Reference

| Command | Purpose |
|---------|---------|
| `sshelp` | Show shortcuts and usage |
| `ssls` | List isolated environments |
| `ssnew <name>` | Create + enter isolated shell (interactive) |
| `ssuse <name>` | Enter existing isolated shell (interactive) |
| `ssback` | Leave isolated context |
| `ssenv enter <name> -- <cmd>` | Run single command in isolation (automation) |

- For interactive debugging: `ssnew <env>` then `exit` when done
- For deterministic automation: prefer `ssenv enter <env> -- <command>` one-liners

## Test Command Policy

When running Go tests inside devcontainer (not via runbook):

```bash
# ssenv changes HOME, so always cd to /workspace first for Go test commands
cd /workspace
go build -o bin/skillshare ./cmd/skillshare
SKILLSHARE_TEST_BINARY="$PWD/bin/skillshare" go test ./tests/integration -count=1
go test ./...
```

Always run in devcontainer unless there is a documented exception.
Note: `ssenv enter` changes HOME, which may affect Go module resolution — always `cd /workspace` before running `go test` or `go build`.

## `--json` Quick Reference

Most commands support `--json` for structured output, making assertions more reliable than text matching.

| Command | `--json` | Notes |
|---------|----------|-------|
| `ss status` | `--json` | Skills, targets, sync status |
| `ss list` | `--json` / `-j` | All skills with metadata |
| `ss target list` | `--json` | Configured targets |
| `ss install <src>` | `--json` | Implies `--force --all` (skip prompts) |
| `ss uninstall <name>` | `--json` | Implies `--force` (skip prompts) |
| `ss collect <path>` | `--json` | Implies `--force` (skip prompts) |
| `ss check` | `--json` | Update availability per repo |
| `ss update` | `--json` | Update results per skill |
| `ss diff` | `--json` | Per-file diff details |
| `ss sync` | `--json` | Sync stats per target |
| `ss audit` | `--format json` | Also accepts `--json` (deprecated alias) |
| `ss log` | `--json` | Raw JSONL (one object per line) |

**Key behaviors:**
- `--json` that implies `--force` / `--all` skips interactive prompts — safe for automation
- Output goes to **stdout only** (progress/spinners suppressed)
- `audit` prefers `--format json`; `--json` still works but is the deprecated form
- `log --json` outputs JSONL (newline-delimited), not a JSON array

### Assertion Patterns with `jq`

```bash
# Count installed skills
ss list --json | jq 'length'

# Check a specific skill exists
ss list --json | jq -e '.[] | select(.name == "my-skill")'

# Verify target is configured
ss target list --json | jq -e '.[] | select(.name == "claude")'

# Assert no critical audit findings
ss audit --format json | jq -e '.summary.critical == 0'

# Check update availability
ss check --json | jq -e '.tracked_repos | length > 0'

# Verify sync succeeded (zero errors)
ss sync --json | jq -e '.errors == 0'

# Install and verify result
ss install https://github.com/user/repo --json | jq -e '.skills | length > 0'
```

When a `jq -e` expression fails (exit code 1 = false, 5 = no output), the step FAILs — no ambiguous text matching needed.

## Container Command Templates

```bash
# Single command
docker exec $CONTAINER ssenv enter "$ENV_NAME" -- ss status

# JSON assertion (preferred for verification)
docker exec $CONTAINER ssenv enter "$ENV_NAME" -- bash -c '
  ss list --json | jq -e ".[] | select(.name == \"my-skill\")"
'

# Multi-line compound command (use bash -c) — global mode flags
docker exec $CONTAINER ssenv enter "$ENV_NAME" -- bash -c '
  ss init --no-copy --all-targets --no-git --no-skill
  ss status
'

# Project mode init (different flag set!)
docker exec $CONTAINER env SKILLSHARE_DEV_ALLOW_WORKSPACE_PROJECT=1 \
  ssenv enter "$ENV_NAME" -- bash -c '
  cd /tmp/test-project && ss init -p --targets claude
'

# Check files (HOME is set to isolated path by ssenv)
docker exec $CONTAINER ssenv enter "$ENV_NAME" -- bash -c '
  cat ~/.config/skillshare/config.yaml
'

# With environment variables
docker exec $CONTAINER ssenv enter "$ENV_NAME" -- bash -c '
  TARGET=~/.claude/skills
  ls -la "$TARGET"
'

# Go tests (must cd /workspace because ssenv changes HOME)
docker exec $CONTAINER ssenv enter "$ENV_NAME" -- bash -c '
  cd /workspace
  go test ./internal/install -run TestParseSource -count=1
'
```

## Relationship with `/mdproof` Skill

This skill (`/cli-e2e-test`) and the `/mdproof` skill are **complementary**, not competing:

| Concern | `/cli-e2e-test` | `/mdproof` |
|---------|-----------------|------------|
| **Scope** | Skillshare project-specific E2E | General-purpose runbook authoring |
| **Infrastructure** | Devcontainer, ssenv, binary build | None — format and assertions only |
| **Config** | `ai_docs/tests/runbook.json` (build, setup, teardown) | Assertion types, snapshot, coverage |
| **Lessons** | Checklist items, CLI flag gotchas | `.mdproof/lessons-learned.md` |
| **When** | Running or debugging a test | Writing or improving a runbook |

### How they work together

1. **Writing a new runbook** → invoke `/mdproof` first for format guidance (assertion types, `jq:` patterns, snapshot usage), then `/cli-e2e-test` to execute it in isolation
2. **Improving existing runbooks** → invoke `/mdproof` for assertion quality review (python3 → jq:, idempotency), then `/cli-e2e-test` to verify changes pass
3. **Debugging failures** → `/cli-e2e-test` Phase 3 step 4 handles manual docker exec; `/mdproof` lessons-learned captures recurring patterns
4. **After a test run** → `/mdproof` Self-Learning section guides recording discoveries to `.mdproof/lessons-learned.md`

### Rule of thumb

- Need to **run** tests or **debug** in devcontainer? → `/cli-e2e-test`
- Need to **write** assertions or **improve** runbook quality? → `/mdproof`
- User says "run extras E2E" → `/cli-e2e-test`
- User says "improve runbook assertions" → `/mdproof` then `/cli-e2e-test` to verify