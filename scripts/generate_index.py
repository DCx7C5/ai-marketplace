#!/usr/bin/env python3
"""Generate index.json from agents/ and flat skills/ directories only (skills/*-*/SKILL.md)."""

import json
import re
from pathlib import Path

root = Path(__file__).parent.parent
catalog: dict = {
    "version": "1.0.0",
    "updated": __import__("datetime").date.today().isoformat(),
    "agents": [],
    "skills": [],
}


def parse_frontmatter(text: str) -> dict[str, str]:
    """Extract key: value pairs from the first YAML frontmatter block."""
    lines = text.split("\n")
    fm: dict[str, str] = {}
    in_fm = False
    for line in lines:
        if line.strip() == "---":
            if in_fm:
                break
            in_fm = True
            continue
        if in_fm:
            m = re.match(r"^([\w]+):\s*(.*)$", line)
            if m:
                fm[m.group(1)] = m.group(2).strip().strip('"')
    return fm


def resolve_block_scalar(fm_value: str, text: str, key: str) -> str:
    """Resolve YAML block scalar (> or |-) to first content line."""
    if fm_value not in (">", ">-", "|-", "|", ""):
        return fm_value
    lines = text.split("\n")
    past_key = False
    for line in lines:
        if re.match(rf"^{key}:", line):
            past_key = True
            continue
        if past_key:
            stripped = line.strip()
            if stripped and not re.match(r"^\w[\w_]*:", line) and not stripped.startswith("---"):
                return stripped
            elif stripped and re.match(r"^\w[\w_]*:", line):
                break
    return fm_value


# ── Agents ────────────────────────────────────────────────────────────────────
for f in sorted((root / "agents").glob("*.md")):
    content = f.read_text()
    fm = parse_frontmatter(content)
    desc = resolve_block_scalar(fm.get("description", ""), content, "description")
    catalog["agents"].append(
        {
            "name": fm.get("name", f.stem),
            "description": desc[:200],
            "model": fm.get("model", "sonnet"),
            "maxTurns": int(fm.get("maxTurns", "20") or 20),
            "file": f"agents/{f.name}",
        }
    )

# ── Skills (FLAT ONLY: skills/*-*/SKILL.md) ────────────────────────────────────
for skill_dir in sorted((root / "skills").glob("*")):
    if not skill_dir.is_dir() or "-" not in skill_dir.name:
        continue
    skill_md = skill_dir / "SKILL.md"
    if not skill_md.exists():
        continue
    content = skill_md.read_text()
    fm = parse_frontmatter(content)
    desc = resolve_block_scalar(fm.get("description", ""), content, "description")
    catalog["skills"].append(
        {
            "name": fm.get("name", skill_dir.name),
            "path": skill_dir.name,
            "description": desc[:200],
            "domain": fm.get("domain", "cybersecurity"),
            "model": fm.get("model", "sonnet"),
            "file": str(skill_md.relative_to(root)),
        }
    )

out = root / "index.json"
out.write_text(json.dumps(catalog, indent=2) + "\n")
print(f"✓ index.json: {len(catalog['agents'])} agents, {len(catalog['skills'])} skills (flat only)")
