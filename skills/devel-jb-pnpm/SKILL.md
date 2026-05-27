---
name: devel-jb-pnpm
description: **Important:** When working with pnpm projects, agents should check for `pnpm-workspace.yaml` and `.npmrc` files to understand workspace structure and configuration. Always use `--frozen-lockfile` in CI environments.
domain: cybersecurity
---
----|-------------|-----------|
| CLI Commands | Install, add, remove, update, run, exec, dlx, and workspace commands | [core-cli](references/core-cli.md) |
| Configuration | pnpm-workspace.yaml, .npmrc settings, and package.json fields | [core-config](references/core-config.md) |
| Workspaces | Monorepo support with filtering, workspace protocol, and shared lockfile | [core-workspaces](references/core-workspaces.md) |
| Store | Content-addressable storage, hard links, and disk efficiency | [core-store](references/core-store.md) |

## Features

| Topic | Description | Reference |
|-------|-------------|-----------|
| Catalogs | Centralized dependency version management for workspaces | [features-catalogs](references/features-catalogs.md) |
| Overrides | Force specific versions of dependencies including transitive | [features-overrides](references/features-overrides.md) |
| Patches | Modify third-party packages with custom fixes | [features-patches](references/features-patches.md) |
| Aliases | Install packages under custom names using npm: protocol | [features-aliases](references/features-aliases.md) |
| Hooks | Customize resolution with .pnpmfile.cjs hooks | [features-hooks](references/features-hooks.md) |
| Peer Dependencies | Auto-install, strict mode, and dependency rules | [features-peer-deps](references/features-peer-deps.md) |

## Best Practices

| Topic | Description | Reference |
|-------|-------------|-----------|
| CI/CD Setup | GitHub Actions, GitLab CI, Docker, and caching strategies | [best-practices-ci](references/best-practices-ci.md) |
| Migration | Migrating from npm/Yarn, handling phantom deps, monorepo migration | [best-practices-migration](references/best-practices-migration.md) |
| Performance | Install optimizations, store caching, workspace parallelization | [best-practices-performance](references/best-practices-performance.md) |