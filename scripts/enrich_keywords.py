#!/usr/bin/env python3
"""
Keyword enrichment for skills using local Ollama.

Designed for two workflows:
1. Normal: run from ai-marketplace root (scans ./skills/)
2. Migration worktree: cd into the skills/ tree (or a worktree copy of it)
   so that "." acts as the skills root. The script auto-detects this.

Usage (normal):
    python scripts/enrich_keywords.py --model qwen2.5:3b --limit 50 --only "devel-jb-*"

Usage (worktree where skills/ is your CWD):
    cd /tmp/my-migration-worktree/skills
    python3 /path/to/original/ai-marketplace/scripts/enrich_keywords.py \
        --model gemma2:2b --dry-run --paths "devel-jb-react*"

The optimized prompt is tuned for low latency on small local models.
"""

import argparse
import json
import re
import sys
import time
from pathlib import Path
from typing import Optional
from urllib import request, error

# ── Optimized prompt (fast + high signal for local Ollama) ─────────────────────
# Key optimizations for response time:
# - Very short system-like instruction (low prefill cost)
# - Hard output contract right up front ("ONLY a single comma-separated line")
# - Strong completion cue ("Keywords:") so the model stops quickly
# - Explicit "no explanations / no JSON" guardrails
# - Focus list keeps the model from overthinking generic terms
# - Caller truncates description to ~800 chars before formatting

OPTIMIZED_PROMPT = """You are a precise keyword tagger for an AI skill marketplace search index.

Output ONLY 4-10 lowercase keywords as a single comma-separated line.
No explanations, no JSON, no bullets, no intro text, no markdown.

Prioritize exact tech names, frameworks, libraries, platforms, and specific actions.

Description:
{description}

Keywords:"""


def is_skills_root(p: Path) -> bool:
    """Heuristic: are we inside a skills tree (many top-level domain dirs or devel-jb-*)?"""
    candidates = [
        "linux", "network", "web-application", "malware", "identity",
        "devel-jb-react-best-practices", "devel-jb-vueuse-functions", "cloud"
    ]
    return any((p / c).exists() for c in candidates)


def find_skills_root() -> Path:
    """Return the directory that contains the skill trees.

    Honors the "skills as root in worktree" pattern:
    - If CWD looks like it contains the domains directly → use CWD
    - Otherwise fall back to <repo>/skills from the script location
    """
    cwd = Path.cwd().resolve()
    if is_skills_root(cwd):
        return cwd

    # Normal case: script lives in ai-marketplace/scripts/
    script_dir = Path(__file__).resolve().parent
    candidate = script_dir.parent / "skills"
    if candidate.exists():
        return candidate

    # Last resort: current dir
    return cwd


def truncate(text: str, max_chars: int = 850) -> str:
    """Aggressive truncate — critical for low latency on local models."""
    text = text.strip()
    if len(text) <= max_chars:
        return text
    # Try to cut at a sentence or paragraph boundary
    cut = text[:max_chars]
    for sep in ("\n\n", ". ", "\n", " "):
        idx = cut.rfind(sep)
        if idx > max_chars * 0.6:
            return cut[:idx].strip()
    return cut


def call_ollama(
    prompt: str,
    model: str = "qwen2.5:3b",
    timeout: int = 45,
    temperature: float = 0.0,
    num_predict: int = 48,
) -> str:
    """Call Ollama /api/generate. Returns raw response text (stripped)."""
    url = "http://localhost:11434/api/generate"
    payload = {
        "model": model,
        "prompt": prompt,
        "stream": False,
        "options": {
            "temperature": temperature,
            "num_predict": num_predict,
            "top_p": 0.9,
            "repeat_penalty": 1.15,
        },
    }
    data = json.dumps(payload).encode("utf-8")
    req = request.Request(url, data=data, headers={"Content-Type": "application/json"})

    try:
        with request.urlopen(req, timeout=timeout) as resp:
            result = json.loads(resp.read().decode("utf-8"))
            return result.get("response", "").strip()
    except error.URLError as e:
        raise RuntimeError(f"Ollama API error (is ollama running?): {e}") from e


def parse_keywords(raw: str, min_k: int = 1, max_k: int = 12) -> list[str]:
    """Turn the model's raw output into a clean list of keywords."""
    if not raw:
        return []

    # Remove any accidental "Keywords:" prefix or quotes the model added
    raw = re.sub(r'^(keywords?:?\s*)', '', raw, flags=re.I).strip(' "`\'')

    # Split on commas or whitespace runs
    parts = re.split(r'[,\s]+', raw)
    kws = []
    seen = set()
    for p in parts:
        p = p.strip().lower().strip('.,;:()[]{}"\'')
        if not p or len(p) < 2:
            continue
        if p in seen:
            continue
        seen.add(p)
        kws.append(p)
        if len(kws) >= max_k:
            break

    # Enforce minimum (pad with generic fallback if the model was too terse)
    while len(kws) < min_k and len(kws) > 0:
        # This almost never triggers with the optimized prompt
        kws.append(f"kw{len(kws)+1}")

    return kws[:max_k]


def enrich_skill(skill_path: Path, model: str, dry_run: bool = False) -> Optional[list[str]]:
    """Read one SKILL.md, call Ollama for keywords, optionally write back."""
    content = skill_path.read_text(encoding="utf-8", errors="ignore")

    # Extract description (frontmatter or first heading + first para)
    desc = ""
    if "---" in content:
        after_fm = content.split("---", 2)[-1] if content.count("---") >= 2 else content
        desc = after_fm[:600]
    else:
        desc = content[:700]

    desc = truncate(desc, 850)

    prompt = OPTIMIZED_PROMPT.format(description=desc)

    t0 = time.time()
    try:
        raw = call_ollama(prompt, model=model, num_predict=48, temperature=0.0)
        kws = parse_keywords(raw, min_k=1, max_k=12)
        dt = time.time() - t0

        if not kws:
            print(f"  [WARN] no keywords from model for {skill_path.parent.name} (raw={raw[:60]!r})")
            return None

        print(f"  ✓ {skill_path.parent.name}: {', '.join(kws)}  ({dt:.1f}s)")

        if dry_run:
            return kws

        # Write back into frontmatter as "keywords:" if not present
        # (simple, safe append for migration work)
        if "keywords:" not in content.split("---")[0] if "---" in content else content:
            # Append a keywords line right before the closing --- of frontmatter
            if content.startswith("---"):
                head, rest = content.split("---", 2)[1:3]
                new_head = head.rstrip() + f'\nkeywords: {", ".join(kws)}\n'
                new_content = f"---{new_head}---{rest}"
                skill_path.write_text(new_content, encoding="utf-8")
                print(f"    → wrote keywords into frontmatter")

        return kws

    except Exception as e:
        print(f"  [ERROR] {skill_path}: {e}")
        return None


def main():
    ap = argparse.ArgumentParser(description="Fast keyword enrichment via local Ollama")
    ap.add_argument("--model", default="qwen2.5:3b", help="Ollama model (prefer 3B-7B quantized for speed)")
    ap.add_argument("--paths", default="*", help="Glob relative to skills root (e.g. 'devel-jb-*' or 'linux/**/detect')")
    ap.add_argument("--limit", type=int, default=0, help="Process at most N skills")
    ap.add_argument("--dry-run", action="store_true", help="Do not write changes")
    ap.add_argument("--only-missing", action="store_true", help="Skip skills that already have keywords in frontmatter")
    args = ap.parse_args()

    root = find_skills_root()
    print(f"Skills root: {root}  (worktree mode: {is_skills_root(Path.cwd().resolve())})")

    # Collect targets
    pattern = args.paths
    targets = []
    for f in sorted(root.rglob("SKILL.md")):
        rel = f.relative_to(root)
        if not rel.match(pattern) and not any(part.startswith(pattern.rstrip("*")) for part in rel.parts):
            # simple glob support for common cases
            if pattern != "*" and pattern not in str(rel):
                continue
        if args.only_missing:
            txt = f.read_text(errors="ignore")
            if "keywords:" in txt.split("---")[0] if "---" in txt else txt:
                continue
        targets.append(f)
        if args.limit and len(targets) >= args.limit:
            break

    print(f"Found {len(targets)} skill(s) to process with model={args.model}")
    if not targets:
        return

    successes = 0
    for i, skill in enumerate(targets, 1):
        print(f"[{i}/{len(targets)}] {skill.relative_to(root)}")
        if enrich_skill(skill, model=args.model, dry_run=args.dry_run):
            successes += 1
        # Small polite pause so we don't hammer a CPU-bound local model
        time.sleep(0.15)

    print(f"\nDone. {successes}/{len(targets)} enriched.")


if __name__ == "__main__":
    main()
