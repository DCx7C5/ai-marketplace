#!/usr/bin/env python3
"""Generate index.json from agents/ and skills/ directories."""
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

# ── Skills ────────────────────────────────────────────────────────────────────
for f in sorted((root / "skills").rglob("SKILL.md")):
    content = f.read_text()
    fm = parse_frontmatter(content)
    parts = f.parent.relative_to(root / "skills").parts
    desc = resolve_block_scalar(fm.get("description", ""), content, "description")
    catalog["skills"].append(
        {
            "name": fm.get("name", "-".join(parts) if parts else f.parent.name),
            "path": "/".join(parts),
            "description": desc[:200],
            "domain": fm.get("domain", "cybersecurity"),
            "model": fm.get("model", "sonnet"),
            "file": str(f.relative_to(root)),
        }
    )

out = root / "index.json"
out.write_text(json.dumps(catalog, indent=2) + "\n")
print(f"✓ index.json: {len(catalog['agents'])} agents, {len(catalog['skills'])} skills")

