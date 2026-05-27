#!/usr/bin/env python3
"""
Skill Migration Utilities

Handles common operations required during the flat migration:

- Ensuring every SKILL.md has a proper YAML frontmatter with at least
  `name` and `description`.
- Generating useful `tags` from the final name + description.
- Preparing updates for ../index.json (tags + sha512, etc.)

This module is meant to be used by both the dry-run tooling and the
final migration script.
"""

from __future__ import annotations
import re
import json
import hashlib
from pathlib import Path
from typing import Any

# -----------------------------------------------------------------------------
# Frontmatter handling
# -----------------------------------------------------------------------------

FRONTMATTER_RE = re.compile(
    r"^---\s*\n(.*?)\n---\s*\n", re.DOTALL | re.MULTILINE
)

def has_frontmatter(text: str) -> bool:
    return bool(FRONTMATTER_RE.match(text))

def parse_frontmatter(text: str) -> tuple[dict[str, Any], str]:
    """Returns (frontmatter_dict, body)"""
    match = FRONTMATTER_RE.match(text)
    if not match:
        return {}, text

    fm_text = match.group(1)
    body = text[match.end():]

    # Very simple key: value parser (good enough for our needs)
    fm: dict[str, Any] = {}
    for line in fm_text.splitlines():
        if ":" not in line:
            continue
        key, _, val = line.partition(":")
        key = key.strip()
        val = val.strip()
        if val.startswith("[") and val.endswith("]"):
            # very naive list support
            items = [x.strip().strip("'\"") for x in val[1:-1].split(",") if x.strip()]
            fm[key] = items
        else:
            fm[key] = val.strip("'\"")
    return fm, body

def build_frontmatter(fm: dict[str, Any]) -> str:
    lines = ["---"]
    for k, v in fm.items():
        if isinstance(v, list):
            items = ", ".join(f'"{x}"' for x in v)
            lines.append(f"{k}: [{items}]")
        else:
            lines.append(f'{k}: "{v}"')
    lines.append("---\n")
    return "\n".join(lines)

def ensure_skill_frontmatter(
    skill_dir: Path,
    final_name: str,
    description: str | None = None,
    *,
    dry_run: bool = True,
) -> dict[str, Any]:
    """
    Guarantees that SKILL.md inside `skill_dir` has a frontmatter with at
    least `name` and `description`.

    Returns the (possibly updated) frontmatter dict.
    If dry_run=False, the file is actually written.
    """
    skill_file = skill_dir / "SKILL.md"
    if not skill_file.exists():
        raise FileNotFoundError(f"No SKILL.md in {skill_dir}")

    original = skill_file.read_text(encoding="utf-8")
    fm, body = parse_frontmatter(original)

    changed = False

    if "name" not in fm or not fm["name"]:
        fm["name"] = final_name
        changed = True

    if "description" not in fm or not fm.get("description"):
        if description:
            fm["description"] = description
            changed = True
        else:
            # Fallback: take first sentence from body if possible
            first_line = next((l.strip() for l in body.splitlines() if l.strip()), "")
            fm["description"] = first_line[:200] or f"Skill: {final_name}"
            changed = True

    if changed and not dry_run:
        new_text = build_frontmatter(fm) + body
        skill_file.write_text(new_text, encoding="utf-8")

    return fm

# -----------------------------------------------------------------------------
# Tag generation - following user rules
# -----------------------------------------------------------------------------

def _generate_name_tags(name: str) -> list[str]:
    """
    From the final flat skill name, extract tags that are ONLY the parts
    between the hyphens.

    Rules:
    - Tags must NOT contain hyphens.
    - Only the atomic segments between '-' in the name are used.
    - No combinations (no "linux-fs", no "linux-fs-permissions", etc.)

    Example:
        "linux-fs-permissions-analyze" → ["linux", "fs", "permissions", "analyze"]
    """
    parts = [p for p in name.split("-") if p]
    # Ensure no hyphens sneak in (shouldn't happen, but defensive)
    return [p.replace("-", "") for p in parts if p.replace("-", "")]


def _extract_keywords_heuristic(description: str, max_keywords: int = 10) -> list[str]:
    """
    Strong heuristic keyword extractor.
    Used when Ollama returns nothing usable (common with very small models).
    Tuned to pull high-signal technical terms from cybersecurity skill descriptions.
    """
    STOPWORDS = {
        "the", "a", "an", "and", "or", "but", "in", "on", "at", "to", "for",
        "with", "by", "of", "is", "are", "was", "were", "be", "this", "that",
        "use", "using", "when", "user", "users", "skill", "skills", "helps",
        "during", "analyzes", "guides", "performs", "provides", "covers",
        "common", "that", "can", "lead", "with", "from",
    }

    text = description.lower()
    words = re.findall(r"[a-z][a-z0-9\-]{3,}", text)

    candidates = []
    for w in words:
        w = w.strip("-")
        if w in STOPWORDS or len(w) < 4:
            continue
        if any(x in w for x in ["ing", "tion", "ment", "ness", "able"]) and len(w) > 6:
            continue
        candidates.append(w)

    # Boost known technical terms
    tech_boost = [
        "linux", "fs", "kernel", "net", "auth", "perm", "priv", "exploit",
        "bypass", "detect", "scan", "enum", "inject", "escalat", "config",
        "misconfig", "capab", "sudo", "acl", "binary", "firmware", "web",
        "api", "db", "cloud", "docker", "k8s", "setuid", "capability",
    ]

    scored = []
    for w in candidates:
        score = 1
        for boost in tech_boost:
            if boost in w:
                score += 4
        scored.append((score, w))

    scored.sort(key=lambda x: (-x[0], -len(x[1])))

    seen = set()
    result = []
    for _, w in scored:
        if w not in seen:
            seen.add(w)
            result.append(w)
            if len(result) >= max_keywords:
                break

    return result


def is_ollama_responsive(model: str = "qwen3:0.6b", timeout: int = 4) -> bool:
    """Fast lightweight check to see if Ollama is up and the model is loaded."""
    import urllib.request
    import json as jsonlib

    payload = {
        "model": model,
        "prompt": "hi",
        "stream": False,
        "options": {"num_predict": 1}
    }
    url = "http://localhost:11434/api/generate"
    data = jsonlib.dumps(payload).encode("utf-8")

    try:
        req = urllib.request.Request(url, data=data, headers={"Content-Type": "application/json"})
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            resp.read()
        return True
    except Exception:
        return False


def _extract_keywords_ollama(
    description: str,
    model: str = "qwen3:0.6b",
    timeout: int = 28,
) -> list[str] | None:
    """
    Optimized Ollama keyword extractor for tiny models (like qwen3:0.6b).

    Optimizations:
    - Aggressively truncate description (small models are slow on long input)
    - Very tight, directive prompt
    - Low num_predict + temperature 0 for speed + consistency
    - Better parsing tolerance
    """
    import urllib.request
    import json as jsonlib

    # === Optimization 1: Truncate description heavily ===
    # For keyword extraction we rarely need more than the first ~350-400 chars.
    short_desc = description.strip()[:420]

    # === Practical prompt for very small models ===
    # We ask the model to "think" a little, then we do smart extraction ourselves
    # on whatever it outputs. This is much more reliable than forcing perfect format.
    prompt = (
        "Read the description and list the most important technical topics, "
        "tools, or concepts mentioned. Be brief.\n\n"
        f"{short_desc}"
    )

    # Using /api/chat instead of /api/generate — often more reliable with tiny models
    payload = {
        "model": model,
        "messages": [
            {"role": "system", "content": "You are a helpful assistant that extracts keywords."},
            {"role": "user", "content": prompt}
        ],
        "stream": False,
        "options": {
            "temperature": 0.0,
            "num_predict": 80,
        }
    }

    url = "http://localhost:11434/api/chat"
    data = jsonlib.dumps(payload).encode("utf-8")

    try:
        req = urllib.request.Request(
            url, 
            data=data, 
            headers={"Content-Type": "application/json"},
            method="POST"
        )
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            raw = resp.read().decode("utf-8")
            result = jsonlib.loads(raw)
            # Chat endpoint returns content inside message
            message = result.get("message", {})
            content = message.get("content", "").strip()

            # === Hybrid approach: Use model's raw output + our good extractor ===
            # Small models are bad at following strict output formats.
            # Better strategy: let the model surface relevant terms in any form,
            # then run our strong heuristic on whatever it said.
            if not content or len(content) < 5:
                return None

            # Run the heuristic extractor on the model's entire response.
            # This usually gives much better results than trusting the format.
            keywords = _extract_keywords_heuristic(content, max_keywords=12)

            # Clean one more time
            final = []
            seen = set()
            for k in keywords or []:
                clean = k.replace("-", "")
                if clean and len(clean) > 2 and clean not in seen:
                    seen.add(clean)
                    final.append(clean)

            return final[:10] if final else None

    except Exception:
        return None


def generate_tags(
    name: str,
    description: str,
    *,
    use_ollama: bool = True,
    ollama_model: str = "qwen3:0.6b",
    max_tags: int = 10,
) -> list[str]:
    """
    Generate tags according to the user's rules:

    - **Automated name extraction**: Tags are automatically derived from the
      final flat skill name by splitting on hyphens. Only the individual
      parts between hyphens are used (e.g. "linux-fs-permissions-analyze"
      produces: linux, fs, permissions, analyze). No hyphenated combinations.

    - **Ollama for description keyword detection**: High-quality keywords are
      extracted from the description using the local Ollama model
      (default: qwen3:0.6b). This is the primary method. Hyphens are removed
      from any keywords.

    Total is limited to ~10 tags (hard max 10).
    """
    tags: set[str] = set()

    # === Name-based tags (user requirement) ===
    # Only the parts between hyphens, no hyphenated combinations
    name_tags = _generate_name_tags(name)

    # === Description keyword detection (Ollama primary) ===
    keywords = None

    if use_ollama:
        # Simple in-memory cache for the current migration run
        if not hasattr(generate_tags, "_ollama_cache"):
            generate_tags._ollama_cache = {}  # type: ignore

        cache_key = description[:400]
        if cache_key in generate_tags._ollama_cache:  # type: ignore
            keywords = generate_tags._ollama_cache[cache_key]  # type: ignore
        else:
            # Primary path: use local Ollama for good keyword extraction
            keywords = _extract_keywords_ollama(description, model=ollama_model)
            if keywords:
                generate_tags._ollama_cache[cache_key] = keywords  # type: ignore

    # Only fall back to heuristic if Ollama is disabled or returned nothing
    if not keywords:
        keywords = _extract_keywords_heuristic(description)

    # Build final list aiming for ~10 tags total
    ordered = []
    seen = set()

    # First add name tags (these have no hyphens by design)
    for t in name_tags:
        if t and t not in seen:
            seen.add(t)
            ordered.append(t)

    # Then fill with description keywords (strip any hyphens from them)
    for t in (keywords or []):
        if t and t not in seen:
            clean_t = t.replace("-", "")
            if clean_t and clean_t not in seen:
                seen.add(clean_t)
                ordered.append(clean_t)
                if len(ordered) >= 10:
                    break

    # Hard cap at 10 (user requirement)
    return ordered[:10]

# -----------------------------------------------------------------------------
# Index.json update helpers (for ../index.json)
# -----------------------------------------------------------------------------

def compute_folder_sha512(skill_dir: Path) -> str:
    """Compute sha512 of the entire skill directory (files + structure)."""
    hasher = hashlib.sha512()
    for path in sorted(skill_dir.rglob("*")):
        if path.is_file():
            hasher.update(str(path.relative_to(skill_dir)).encode())
            hasher.update(path.read_bytes())
    return hasher.hexdigest()

def update_index_entry(
    index_path: Path,
    skill_name: str,
    *,
    tags: list[str] | None = None,
    sha512: str | None = None,
    dry_run: bool = True,
) -> bool:
    """
    Update (or add) tags and/or sha512 for a skill entry in ../index.json.

    Matching is currently done on the 'name' field.
    Returns True if the file would be / was modified.
    """
    data = json.loads(index_path.read_text(encoding="utf-8"))
    skills = data.get("skills", [])

    updated = False
    for entry in skills:
        if entry.get("name") == skill_name:
            if tags is not None:
                entry["tags"] = tags
                updated = True
            if sha512 is not None:
                entry["sha512"] = sha512
                updated = True
            break

    if updated and not dry_run:
        index_path.write_text(json.dumps(data, indent=2), encoding="utf-8")

    return updated


if __name__ == "__main__":
    # Quick self-test
    print("Testing tag generation...")
    name = "harden-webapp-auth"
    desc = "Helps with web application authentication hardening and bypass detection."
    print("Tags:", generate_tags(name, desc))

    print("\nFrontmatter test would go here (dry-run mode).")
