Add new agents as Markdown files in agents/ with valid YAML frontmatter and keep name aligned with filename.
Keep agent metadata valid: short description (<200 chars), supported model (sonnet|haiku|opus), and bounded maxTurns.
Add new skills as skills/<skill-name>/SKILL.md with valid YAML frontmatter containing at least name and description.
Use recursive skill directories with hyphenated leaf names and keep the skill name aligned with its directory.
Run bash scripts/validate.sh before opening a PR and only proceed if validation passes.
Contribute through a fork and feature branch, then open pull requests targeting main.
Use Conventional Commits for commit messages.
Treat index.json as generated output and keep index.json.sha512 updated after regeneration.
Expect CI validation on changes under agents/** and skills/** and fix failures before merge.
Use Python 3.11+ and uv-based workflows for MCP development.
Keep MCP implementations async-first, strongly typed, and tested.
Do not contribute weaponized exploit or malicious payload content.
Use scripts/refresh-flat-index.sh for one-shot index-tree refresh, hash update, and validation.
Use scripts/install.sh to install marketplace agents and skills into local Claude directories.
Use scripts/install-mcp.sh and scripts/install-mcp-core.sh for MCP list/install/verify/bootstrap workflows.
Use `~/.copilot` as the canonical home for Copilot hooks, rules, workflows, and scripts.
Keep IntelliJ Copilot config paths symlinked to `~/.copilot` (hooks, rules, workflows) instead of duplicating client-local copies.
Create new git worktrees for this project under `~/.copilot/session-state/<uuid>/wt<n>`.
Keep TODO workflow visualization in `~/.copilot/workflows/todo-workflow.md` as a vertical start-to-end Mermaid flow (no loop).
20. Never read all .md files. Only fetch frontmatter header to get info.
