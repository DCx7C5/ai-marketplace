#!/usr/bin/env python3
"""Generate a recursive index.json tree for agents/ and skills/."""

from __future__ import annotations

import json
import re
from hashlib import sha512
from datetime import date
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
UPDATED = date.today().isoformat()


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
    """Resolve YAML block scalars to the first content line."""
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
            if stripped and re.match(r"^\w[\w_]*:", line):
                break
    return fm_value


def file_sha512(path: Path) -> str:
    return sha512(path.read_bytes()).hexdigest()


def directory_sha512(path: Path) -> str:
    hasher = sha512()
    for item in sorted(path.rglob("*")):
        if not item.is_file() or item.name == "index.json":
            continue
        hasher.update(str(item.relative_to(path)).encode())
        hasher.update(item.read_bytes())
    return hasher.hexdigest()


def agent_entry(md_path: Path) -> dict[str, object]:
    content = md_path.read_text()
    fm = parse_frontmatter(content)
    desc = resolve_block_scalar(fm.get("description", ""), content, "description")
    entry: dict[str, object] = {
        "name": fm.get("name", md_path.stem),
        "description": desc[:200],
        "model": fm.get("model", "sonnet"),
        "sha512": file_sha512(md_path),
        "file": str(md_path.relative_to(ROOT)),
    }
    max_turns = fm.get("maxTurns")
    if max_turns:
        entry["maxTurns"] = int(max_turns or 20)
    return entry


def skill_entry(skill_md: Path) -> dict[str, object]:
    content = skill_md.read_text()
    fm = parse_frontmatter(content)
    desc = resolve_block_scalar(fm.get("description", ""), content, "description")
    rel_path = skill_md.parent.relative_to(ROOT / "skills").as_posix()
    entry: dict[str, object] = {
        "name": fm.get("name", skill_md.parent.name),
        "path": rel_path,
        "description": desc[:200],
        "domain": fm.get("domain", "cybersecurity"),
        "model": fm.get("model", "sonnet"),
        "sha512": directory_sha512(skill_md.parent),
        "file": str(skill_md.relative_to(ROOT)),
    }
    return entry


def child_index_entry(child_dir: Path, kind: str) -> dict[str, object]:
    entry: dict[str, object] = {
        "name": child_dir.name,
        "description": f"{kind} directory index",
        "sha512": directory_sha512(child_dir),
        "file": str((child_dir / "index.json").relative_to(ROOT)),
    }
    return entry


def write_agents_index(directory: Path) -> None:
    agents: list[dict[str, object]] = []
    skills: list[dict[str, object]] = []
    catalog: dict[str, object] = {
        "version": "1.0.0",
        "updated": UPDATED,
        "agents": agents,
        "skills": skills,
    }

    for md in sorted(directory.glob("*.md")):
        if md.name == "README.md":
            continue
        agents.append(agent_entry(md))

    for child in sorted(
        p for p in directory.iterdir() if p.is_dir() and not p.name.startswith(".") and not p.name.startswith("__")
    ):
        agents.append(child_index_entry(child, "agent"))
        write_agents_index(child)

    (directory / "index.json").write_text(json.dumps(catalog, indent=2) + "\n")


def write_skills_index(directory: Path) -> None:
    agents: list[dict[str, object]] = []
    skills: list[dict[str, object]] = []
    catalog: dict[str, object] = {
        "version": "1.0.0",
        "updated": UPDATED,
        "agents": agents,
        "skills": skills,
    }

    skill_md = directory / "SKILL.md"
    if skill_md.exists():
        skills.append(skill_entry(skill_md))

    for child in sorted(
        p for p in directory.iterdir() if p.is_dir() and not p.name.startswith(".") and not p.name.startswith("__")
    ):
        skills.append(child_index_entry(child, "skill"))
        write_skills_index(child)

    (directory / "index.json").write_text(json.dumps(catalog, indent=2) + "\n")


def main() -> None:
    root_catalog = {
        "version": "1.0.0",
        "updated": UPDATED,
        "agents": [
            {
                "name": "agents",
                "description": "Agents directory index",
                "sha512": directory_sha512(ROOT / "agents"),
                "file": "agents/index.json",
            }
        ],
        "skills": [
            {
                "name": "skills",
                "description": "Skills directory index",
                "sha512": directory_sha512(ROOT / "skills"),
                "file": "skills/index.json",
            }
        ],
    }

    write_agents_index(ROOT / "agents")
    write_skills_index(ROOT / "skills")

    (ROOT / "index.json").write_text(json.dumps(root_catalog, indent=2) + "\n")
    print("✓ index.json tree regenerated")


if __name__ == "__main__":
    main()
