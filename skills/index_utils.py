"""
Utilities for updating the parent ../index.json after migration.

This file lives directly in the skills root (as requested).
It handles:
- Computing sha512 of a migrated skill folder
- Generating final tags (name parts + Ollama description keywords)
- Finding the corresponding entry in ../index.json
- Writing tags + sha512 back into the index
"""

from __future__ import annotations
import json
from pathlib import Path
from typing import List, Dict, Any, Optional

from skill_migration_utils import generate_tags, compute_folder_sha512


def find_index_entry(
    index_path: Path,
    old_path: str,
    new_name: str,
) -> Optional[Dict[str, Any]]:
    """
    Try to find the matching entry in ../index.json.

    Matching strategy (in order):
    1. Exact match on the new flat name (best case after migration)
    2. Match on the old relative path (if still stored)
    3. Fuzzy match on name components
    """
    data = json.loads(index_path.read_text(encoding="utf-8"))
    skills: List[Dict[str, Any]] = data.get("skills", [])

    # Try new name first
    for entry in skills:
        if entry.get("name") == new_name:
            return entry

    # Try old path
    for entry in skills:
        if entry.get("path") == old_path or entry.get("file") == old_path:
            return entry

    # Last resort: try to match by last component of the name
    last_part = new_name.split("-")[-1] if "-" in new_name else new_name
    for entry in skills:
        if last_part in str(entry.get("name", "")):
            return entry

    return None


def update_index_for_skill(
    old_path: str,
    new_name: str,
    skill_dir: Path,
    description: str = "",
    index_path: Path = Path("../index.json"),
    dry_run: bool = True,
) -> Dict[str, Any]:
    """
    Main function to update ../index.json after a skill has been migrated.

    - Computes sha512 of the skill folder
    - Generates final tags (respecting current rules)
    - Finds the right entry and patches tags + sha512
    """
    result = {
        "old_path": old_path,
        "new_name": new_name,
        "matched": False,
        "tags": [],
        "sha512": None,
        "updated": False,
        "dry_run": dry_run,
    }

    # Compute sha512 of the final skill directory
    sha = compute_folder_sha512(skill_dir)
    result["sha512"] = sha

    # Generate tags (Ollama preferred for description)
    tags = generate_tags(new_name, description, use_ollama=True)
    result["tags"] = tags

    # Find the entry
    entry = find_index_entry(index_path, old_path, new_name)
    if not entry:
        result["error"] = "Could not find matching entry in ../index.json"
        return result

    result["matched"] = True

    if not dry_run:
        # Load, update, and write back
        data = json.loads(index_path.read_text(encoding="utf-8"))
        for e in data.get("skills", []):
            if e.get("name") == entry.get("name"):
                e["tags"] = tags
                e["sha512"] = sha
                break

        index_path.write_text(json.dumps(data, indent=2), encoding="utf-8")
        result["updated"] = True
    else:
        result["would_update"] = {
            "tags": tags,
            "sha512": sha,
            "target_name": entry.get("name"),
        }

    return result
