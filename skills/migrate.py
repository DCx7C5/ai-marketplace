#!/usr/bin/env python3
"""
Migration runner for the flat skills architecture.

This tool performs the actual migration of skills to the final flat structure.

Usage:
    python migrate.py --apply                  # Run the real migration
    python migrate.py --apply --only "..."     # Migrate specific skills
    python migrate.py --dry-run                # Preview changes (safe default)

It handles:
- Copying skill directories to their new flat names at the root
- Ensuring proper frontmatter (name + description)
- Generating final tags (name-based + Ollama description keywords)
- Computing sha512 of the migrated folder
- Updating ../index.json with the new tags + sha512
"""

from __future__ import annotations
import argparse
import shutil
from pathlib import Path
from typing import List, Dict, Any

# Local modules we've been building
from linux_prefix_map import normalize_linux_path
from skill_migration_utils import ensure_skill_frontmatter, generate_tags
from index_utils import update_index_for_skill, compute_folder_sha512

# =============================================================================
# General name derivation (combines all previous rules)
# =============================================================================

# Basic category → prefix mapping (from earlier discussions)
CATEGORY_PREFIX = {
    "jbskills": "devel-jb",
    "linux-tools": "cmd",
    "linux": "linux",          # special handling below via linux_prefix_map
    "offensive": "offensive",
    "hardening": "harden",
    "forensics": "forensic",
    "threatintel": "intel",
    "mobile": "mobile",
    "osint": "osint",
    "steganography": "stego",
    "_meta": "_meta",
}

# Simple abbreviation table (user liked webapp etc.)
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


def derive_final_name(old_path: str) -> str:
    """
    Compute the final flat skill directory name.

    Key principles (updated based on feedback):
    - "mcp can have multiple actions" → "mcp-builder" should remain "mcp-builder",
      not be squished into "mcpbuilder".
    - Preserve meaningful hyphens inside tool/action names.
    - Only strip hyphens from deep organizational folders we're collapsing.
    - Keep names readable and natural.
    """
    p = Path(old_path)
    parts = list(p.parts)

    if not parts:
        return "unknown-skill"

    top = parts[0]

    # Special high-quality handling for linux/
    if top == "linux":
        return normalize_linux_path(str(p.relative_to("linux")))

    prefix = CATEGORY_PREFIX.get(top, top)

    # Drop very generic action folders
    rest = parts[1:]
    generic_actions = {
        "analyze", "audit", "detect", "exploit", "extract",
        "scan", "enum", "collect", "query", "read", "list", "get"
    }
    rest = [r for r in rest if r.lower() not in generic_actions]

    if not rest:
        return prefix

    # Special case for jbskills / devel tools:
    # Keep the original folder name with its hyphens (e.g. mcp-builder)
    if top == "jbskills":
        leaf = rest[-1]
        return f"{prefix}-{leaf}"

    # For other categories, be conservative about stripping hyphens.
    # Only strip from segments that look like broad organizational folders.
    cleaned = []
    for seg in rest:
        # If the segment is long and has hyphens, it was probably an
        # intermediate category folder → we can collapse it.
        if len(seg) > 14 and seg.count("-") >= 1:
            seg = seg.replace("-", "")
        cleaned.append(seg)

    slug = "-".join(cleaned).lower()
    slug = _apply_abbreviations(slug)

    while "--" in slug:
        slug = slug.replace("--", "-")

    final = f"{prefix}-{slug}" if slug else prefix
    return final.strip("-")


# =============================================================================
# Core migration logic
# =============================================================================

def migrate_one_skill(
    old_path: Path,
    dry_run: bool = True,
    index_path: Path = Path("../index.json"),
) -> Dict[str, Any]:
    """
    Process a single skill:
    - Compute final flat name
    - Copy entire tree to new location at root (if not dry-run)
    - Ensure frontmatter
    - Generate tags (name-based + description keywords)
    - Compute sha512 of final folder
    - Update ../index.json with tags + sha512
    """
    result = {
        "old_path": str(old_path),
        "final_name": None,
        "new_location": None,
        "tags": [],
        "sha512": None,
        "index_updated": False,
        "error": None,
    }

    try:
        final_name = derive_final_name(str(old_path))
        result["final_name"] = final_name

        target_dir = Path.cwd() / final_name

        # Skip if it already looks migrated (simple guard)
        if final_name.startswith(("devel-jb-", "cmd-", "linux-", "harden-", "offensive-", "intel-", "forensic-")) and target_dir.exists():
            result["error"] = "Already migrated"
            return result

        if not dry_run:
            if target_dir.exists():
                shutil.rmtree(target_dir)
            shutil.copytree(old_path, target_dir)
            working_dir = target_dir
        else:
            working_dir = old_path

        fm = ensure_skill_frontmatter(working_dir, final_name, dry_run=dry_run)
        final_name_in_fm = fm.get("name", final_name)
        desc = fm.get("description", "")

        tags = generate_tags(final_name_in_fm, desc, use_ollama=True)
        result["tags"] = tags

        sha = compute_folder_sha512(working_dir)
        result["sha512"] = sha

        index_result = update_index_for_skill(
            old_path=str(old_path),
            new_name=final_name_in_fm,
            skill_dir=working_dir,
            description=desc,
            index_path=index_path,
            dry_run=dry_run,
        )
        result["index_updated"] = index_result.get("updated") or index_result.get("would_update")
        result["index_result"] = index_result

    except Exception as e:
        result["error"] = str(e)

    return result


def find_all_skill_roots(root: Path = Path(".")) -> list[Path]:
    """Discover all directories that contain a SKILL.md (flat or old structure)."""
    roots = []
    for path in root.rglob("SKILL.md"):
        skill_root = path.parent
        # Skip the new flat locations if they already exist (to avoid re-migrating)
        if skill_root.name.startswith(("devel-jb-", "cmd-", "linux-", "harden-", "offensive-", "intel-", "forensic-")):
            continue
        roots.append(skill_root)
    return sorted(roots)


def main():
    parser = argparse.ArgumentParser(description="Migrate skills to flat structure")
    parser.add_argument("--apply", action="store_true",
                        help="Perform the actual migration")
    parser.add_argument("--dry-run", action="store_true",
                        help="Preview only (no changes)")
    parser.add_argument("--limit", type=int, default=0,
                        help="Maximum number of skills to process (0 = all)")
    parser.add_argument("--only", type=str, default=None,
                        help="Comma-separated list of specific old paths to migrate")
    parser.add_argument("--yes", action="store_true",
                        help="Skip confirmation prompt on --apply")

    args = parser.parse_args()

    dry_run = not args.apply

    if dry_run:
        print("DRY-RUN preview (use --apply to write changes)\n")
    else:
        print("Applying migration...\n")

    # Determine which skills to process
    if args.only:
        candidates = [Path(p.strip()) for p in args.only.split(",")]
    else:
        candidates = find_all_skill_roots()

    if args.limit > 0:
        candidates = candidates[: args.limit]

    # Confirmation for real runs
    if not dry_run and not args.yes:
        print(f"About to migrate {len(candidates)} skills.")
        confirm = input("Type 'yes' to continue: ").strip().lower()
        if confirm != "yes":
            print("Aborted.")
            return

    success = 0
    failed = 0

    for old in candidates:
        old_path = Path(old)
        if not (old_path / "SKILL.md").exists():
            print(f"SKIP (no SKILL.md): {old}")
            continue

        res = migrate_one_skill(old_path, dry_run=dry_run)

        if dry_run:
            print(f"OLD: {res['old_path']}")
            print(f"NEW: {res['final_name']}")
            print(f"  Tags: {res['tags']}")
            print(f"  sha512: {res.get('sha512', 'N/A')[:16]}...")
            if res.get("index_result"):
                print(f"  Index: {res['index_result']}")
            if res["error"]:
                print(f"  ERROR: {res['error']}")
            print("-" * 50)
        else:
            if res["error"]:
                print(f"  {res['final_name']} → ERROR: {res['error']}")
                failed += 1
            else:
                print(f"  {res['final_name']} → OK")
                success += 1

    if dry_run:
        print(f"\nDry run complete. {len(candidates)} skills would be processed.")
    else:
        print(f"\nMigration complete. Success: {success}, Failed: {failed}")


if __name__ == "__main__":
    main()
