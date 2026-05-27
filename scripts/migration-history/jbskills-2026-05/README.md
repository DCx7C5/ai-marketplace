# jbskills → devel-jb-* Migration (May 2026)

This directory contains the exact migration tooling used for the "Group 1" flat skills migration.

## Context
- 85 high-quality development / JetBrains / frontend / tooling skills were imported and flattened.
- Tooling was intentionally written to live *inside* the `skills/` directory (skills as root in the worktree).
- Ran from a git worktree with `cd skills` so `Path(".")` and `rglob` worked directly on the tree.
- Used Ollama (various small models) + strong heuristic fallback for keyword extraction from descriptions.
- Special rules for `jbskills/` source → `devel-jb-{leaf}` naming (preserving internal hyphens).

## Key Files (recovered from db846a4)
- `migrate.py` — main driver, derive_final_name logic, CATEGORY_PREFIX
- `skill_migration_utils.py` — frontmatter enforcement + the Ollama + heuristic tag/keyword generation
- `index_utils.py` — sha512 + index.json updates
- `linux_prefix_map.py` — detailed rules for flattening the linux/ hierarchy

## Original Source for jbskills
The source material lived in a transient `jbskills/` directory (one subdir per skill) during the worktree session.
It was never a long-lived committed top-level folder in main history. The migration copied them to root-level `devel-jb-*` siblings.

## Post-Migration Cleanups
- Later commit aa03079 removed these four scripts.
- Commit 0a60197 removed remaining old category folders (`_meta/`, deep osint remnants, linux-tools/ etc.).

See also the worktree at /tmp/explore-pre-migration for a live checkout of the state right after the jbskills migration (devel-jb-* present + old hierarchy + remnants).

