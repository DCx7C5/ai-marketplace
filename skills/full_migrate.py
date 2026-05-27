#!/usr/bin/env python3
"""
Full Flat Migration Runner for the entire remaining skill taxonomy.

Respects all historical rules from the jbskills migration:
- CATEGORY_PREFIX + linux_prefix_map
- Drop generic action verbs at the end
- Name tags = only atomic hyphen parts (no combinations)
- Ollama (fast optimized prompt) + heuristic for keywords
- Ensure name + description frontmatter
- Run with skills/ as CWD (worktree pattern)
- Safe dry-run first

Usage in the worktree:
    cd /tmp/migration-full-flat/skills
    python3 full_migrate.py --dry-run --limit 20
    python3 full_migrate.py --apply --categories "steganography,database" --yes
"""
from __future__ import annotations
import argparse
import shutil
import hashlib
import re
import json
from pathlib import Path
from typing import Any

# Historical modules (present in this dir)
from linux_prefix_map import normalize_linux_path, LINUX_COMPONENT_MAP
from skill_migration_utils import ensure_skill_frontmatter, generate_tags

# Extended prefixes (respecting original spirit)
CATEGORY_PREFIX = {
    "linux": "linux",
    "linux-tools": "cmd",
    "offensive": "offensive",
    "mobile": "mobile",
    "osint": "osint",
    "steganography": "stego",
    "browser": "browser",
    "cloud": "cloud",
    "compliance": "compliance",
    "crypto": "crypto",
    "database": "db",
    "deception": "deception",
    "email": "email",
    "identity": "identity",
    "industrial": "ics",
    "intel": "intel",
    "malware": "malware",
    "network": "net",
    "soc": "soc",
    "vulnerabilities": "vuln",
    "web-application": "webapp",
    "windows": "windows",
    "deception": "deception",
}

GENERIC_ACTIONS = {
    "analyze", "audit", "detect", "exploit", "extract", "scan", "enum",
    "collect", "query", "read", "list", "get", "execute", "run", "deploy",
    "implement", "harden", "forensic"
}

ABBREVIATIONS = {
    "webapplication": "webapp",
    "application": "app",
    "authentication": "auth",
    "filesystem": "fs",
    "network": "net",
    "configuration": "config",
    "vulnerability": "vuln",
    "vulnerabilities": "vulns",
    "information": "info",
    "management": "mgmt",
}

def _apply_abbreviations(slug: str) -> str:
    for long, short in ABBREVIATIONS.items():
        slug = slug.replace(long, short)
    return slug

def derive_flat_name(skill_dir: Path) -> str:
    """
    Core naming rule, extended for full deep taxonomy.
    Respects all historical conventions.
    """
    parts = list(skill_dir.parts)
    if not parts:
        return "unknown-skill"

    top = parts[0]

    # Linux gets special high-quality treatment
    if top == "linux":
        try:
            return normalize_linux_path(str(skill_dir.relative_to("linux")))
        except Exception:
            pass  # fall through

    prefix = CATEGORY_PREFIX.get(top, top)

    # Take the path after the category, drop generic trailing actions
    rest = parts[1:]
    rest = [r for r in rest if r.lower() not in GENERIC_ACTIONS]

    if not rest:
        return prefix

    # Collapse long hyphenated intermediate folders (historical rule)
    cleaned = []
    for seg in rest:
        if len(seg) > 14 and seg.count("-") >= 1:
            seg = seg.replace("-", "")
        cleaned.append(seg)

    slug = "-".join(cleaned).lower()
    slug = _apply_abbreviations(slug)

    while "--" in slug:
        slug = slug.replace("--", "-")

    final = f"{prefix}-{slug}" if slug else prefix
    return final.strip("-")

def find_all_real_skills(root: Path = Path(".")) -> list[Path]:
    """Find every actual skill leaf (dir containing SKILL.md that isn't already flat-migrated)."""
    skills = []
    for f in root.rglob("SKILL.md"):
        skill_dir = f.parent
        name = skill_dir.name
        # Skip anything that looks already migrated to flat style
        if any(name.startswith(p + "-") for p in ["devel-jb", "linux", "cmd", "offensive", "stego", "db", "net", "vuln", "webapp", "ics", "malware"]):
            continue
        # Skip obvious non-skill markers
        if name in {"templates", "references", "scripts", "assets", "examples", "docs"}:
            continue
        skills.append(skill_dir)
    return sorted(skills)

def compute_sha512(skill_dir: Path) -> str:
    h = hashlib.sha512()
    for p in sorted(skill_dir.rglob("*")):
        if p.is_file():
            h.update(str(p.relative_to(skill_dir)).encode())
            h.update(p.read_bytes())
    return h.hexdigest()

def migrate_skill(skill_dir: Path, dry_run: bool = True, root_index: Path = Path("../index.json")) -> dict[str, Any]:
    result = {
        "old": str(skill_dir),
        "new_name": None,
        "tags": [],
        "sha512": None,
        "error": None,
    }
    try:
        new_name = derive_flat_name(skill_dir)
        result["new_name"] = new_name

        target = Path.cwd() / new_name
        if target.exists() and not dry_run:
            shutil.rmtree(target)

        if not dry_run:
            shutil.copytree(skill_dir, target)
            working = target
        else:
            working = skill_dir

        # Ensure frontmatter
        fm = ensure_skill_frontmatter(working, new_name, dry_run=dry_run)
        desc = fm.get("description", "") or ""

        # Tags: name parts + Ollama keywords (uses the updated fast prompt in the module)
        tags = generate_tags(new_name, desc, use_ollama=True)
        result["tags"] = tags

        sha = compute_sha512(working)
        result["sha512"] = sha

    except Exception as e:
        result["error"] = str(e)
    return result

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true", default=True)
    ap.add_argument("--apply", action="store_true")
    ap.add_argument("--limit", type=int, default=0)
    ap.add_argument("--categories", type=str, default=None, help="Comma list of top-level dirs to include")
    ap.add_argument("--yes", action="store_true")
    args = ap.parse_args()

    dry = not args.apply

    if dry:
        print("=== DRY RUN — no changes will be made ===\n")
    else:
        print("=== APPLY MODE — will modify filesystem and index ===\n")

    all_skills = find_all_real_skills()

    if args.categories:
        wanted = {c.strip() for c in args.categories.split(",")}
        def matches(cat: str) -> bool:
            for w in wanted:
                if w.endswith("*"):
                    if cat.startswith(w[:-1]):
                        return True
                elif cat == w:
                    return True
            return False
        all_skills = [s for s in all_skills if matches(s.parts[0])]

    if args.limit:
        all_skills = all_skills[:args.limit]

    print(f"Found {len(all_skills)} skills to consider.\n")

    if not dry and not args.yes:
        resp = input(f"Really migrate {len(all_skills)} skills? Type 'MIGRATE' to continue: ")
        if resp.strip() != "MIGRATE":
            print("Aborted.")
            return

    success = 0
    for i, skill in enumerate(all_skills, 1):
        res = migrate_skill(skill, dry_run=dry)
        print(f"[{i}/{len(all_skills)}] {res['old']}  →  {res['new_name']}")
        if res["tags"]:
            print(f"    tags: {', '.join(res['tags'][:8])}")
        if res["error"]:
            print(f"    ERROR: {res['error']}")
        else:
            success += 1
        print()

    print(f"\nComplete. {success} processed (dry={dry}).")

if __name__ == "__main__":
    main()
