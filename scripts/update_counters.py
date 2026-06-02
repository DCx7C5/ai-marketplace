#!/usr/bin/env python3
"""Update marketplace counters in README.md based on index.json files."""

from __future__ import annotations

import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent


def get_counts() -> dict[str, int]:
    """Extract counts from all index.json files."""
    counts = {}
    
    # Count agents
    agents_idx = json.loads((ROOT / "agents" / "index.json").read_text())
    counts["agents"] = len(agents_idx.get("agents", []))
    
    # Count skills
    skills_idx = json.loads((ROOT / "skills" / "index.json").read_text())
    counts["skills"] = len(skills_idx.get("skills", []))
    
    # Count rules
    rules_idx = json.loads((ROOT / "rules" / "index.json").read_text())
    counts["rules"] = len(rules_idx.get("rules", []))
    
    # Count teams
    teams_idx = json.loads((ROOT / "teams" / "index.json").read_text())
    counts["teams"] = len(teams_idx.get("teams", []))
    
    # Count workflows
    workflows_idx = json.loads((ROOT / "workflows" / "index.json").read_text())
    counts["workflows"] = len(workflows_idx.get("workflows", []))
    
    # Count MCPs
    mcps_idx = json.loads((ROOT / "mcps" / "index.json").read_text())
    counts["mcps"] = len(mcps_idx.get("mcps", []))
    
    return counts


def update_readme(counts: dict[str, int]) -> None:
    """Update README.md with current counts."""
    readme_path = ROOT / "README.md"
    content = readme_path.read_text()
    
    # Update agents badge
    content = re.sub(
        r'!\[Agents\]\(https://img\.shields\.io/badge/agents-\d+-',
        f"![Agents](https://img.shields.io/badge/agents-{counts['agents']}-",
        content,
    )
    
    # Update skills badge
    content = re.sub(
        r'!\[Skills\]\(https://img\.shields\.io/badge/skills-[\d,%]+\?',
        f"![Skills](https://img.shields.io/badge/skills-{counts['skills']:,}?",
        content,
    )
    
    # Update agents count in table
    content = re.sub(
        r'\| \[\*\*Agents\*\*\]\(agents/\) \| \d+ \|',
        f"| [**Agents**](agents/) | {counts['agents']} |",
        content,
    )
    
    # Update skills count in table
    content = re.sub(
        r'\| \[\*\*Skills\*\*\]\(skills/\) \| [\d,]+ \|',
        f"| [**Skills**](skills/) | {counts['skills']:,} |",
        content,
    )
    
    # Update MCPs count in table
    content = re.sub(
        r'\| \[\*\*MCPs\*\*\]\(mcps/\) \| \d+ \|',
        f"| [**MCPs**](mcps/) | {counts['mcps']} |",
        content,
    )
    
    # Add/update rules, teams, workflows rows if they don't exist or update them
    # For now, just update if they exist
    if "| [**Rules**](rules/) |" in content:
        content = re.sub(
            r'\| \[\*\*Rules\*\*\]\(rules/\) \| \d+ \|',
            f"| [**Rules**](rules/) | {counts['rules']} |",
            content,
        )
    
    if "| [**Teams**](teams/) |" in content:
        content = re.sub(
            r'\| \[\*\*Teams\*\*\]\(teams/\) \| \d+ \|',
            f"| [**Teams**](teams/) | {counts['teams']} |",
            content,
        )
    
    if "| [**Workflows**](workflows/) |" in content:
        content = re.sub(
            r'\| \[\*\*Workflows\*\*\]\(workflows/\) \| \d+ \|',
            f"| [**Workflows**](workflows/) | {counts['workflows']} |",
            content,
        )
    
    readme_path.write_text(content)


def main() -> None:
    counts = get_counts()
    print(f"Agents: {counts['agents']}")
    print(f"Skills: {counts['skills']:,}")
    print(f"Rules: {counts['rules']}")
    print(f"Teams: {counts['teams']}")
    print(f"Workflows: {counts['workflows']}")
    print(f"MCPs: {counts['mcps']}")
    
    update_readme(counts)
    print("✓ README.md counters updated")


if __name__ == "__main__":
    main()
