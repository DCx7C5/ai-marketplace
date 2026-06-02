#!/usr/bin/env bash
# install.sh — Install agents and/or skills from the marketplace
# Usage: bash install.sh [--agents] [--skills] [--all] [--target <dir>]
set -euo pipefail

MARKETPLACE_RAW="https://raw.githubusercontent.com/Dystopian/ai-marketplace/main"
TARGET_DIR="${PWD}"
INSTALL_AGENTS=false
INSTALL_SKILLS=false

usage() {
  echo "Usage: $0 [--agents] [--skills] [--all] [--target <directory>]"
  echo ""
  echo "Options:"
  echo "  --agents    Install all agents to .claude/agents/"
  echo "  --skills    Install all skills to .claude/skills/"
  echo "  --all       Install both agents and skills"
  echo "  --target    Target project directory (default: current directory)"
  exit 1
}

while [[ $# -gt 0 ]]; do
  case $1 in
    --agents) INSTALL_AGENTS=true; shift ;;
    --skills) INSTALL_SKILLS=true; shift ;;
    --all)    INSTALL_AGENTS=true; INSTALL_SKILLS=true; shift ;;
    --target) TARGET_DIR="$2"; shift 2 ;;
    *) usage ;;
  esac
done

if [[ "$INSTALL_AGENTS" == "false" && "$INSTALL_SKILLS" == "false" ]]; then
  usage
fi

echo "🛒 AI Marketplace Installer"
echo "   Target: $TARGET_DIR"
echo ""

if [[ "$INSTALL_AGENTS" == "true" ]]; then
  AGENT_DIR="$TARGET_DIR/.claude/agents"
  mkdir -p "$AGENT_DIR"
  echo "📦 Installing agents → $AGENT_DIR"

  collect_files() {
    local start_url="$1"
    local section="$2"
    python3 - "$start_url" "$section" <<'PY'
import json
import sys
from urllib.request import urlopen

start_url = sys.argv[1]
section = sys.argv[2]
repo_base = start_url.rsplit('/', 1)[0]
seen: set[str] = set()


def walk(url: str) -> None:
    if url in seen:
        return
    seen.add(url)
    with urlopen(url) as response:
        data = json.load(response)
    for entry in data.get(section, []):
        file = entry.get("file")
        if not file:
            continue
        if file.endswith("index.json"):
            walk(f"{repo_base}/{file}")
        else:
            print(file)


walk(start_url)
PY
  }

  # Fetch agent list from the recursive index tree
  AGENT_LIST=$(collect_files "$MARKETPLACE_RAW/index.json" agents)

  for agent_file in $AGENT_LIST; do
    dest="$AGENT_DIR/${agent_file#agents/}"
    mkdir -p "$(dirname "$dest")"
    echo "  ↓ $agent_file"
    curl -sSL "$MARKETPLACE_RAW/$agent_file" -o "$dest"
  done
  echo "  ✓ Agents installed"
fi

if [[ "$INSTALL_SKILLS" == "true" ]]; then
  SKILL_DIR="$TARGET_DIR/.claude/skills"
  mkdir -p "$SKILL_DIR"
  echo "📦 Installing skills → $SKILL_DIR"

  collect_files() {
    local start_url="$1"
    local section="$2"
    python3 - "$start_url" "$section" <<'PY'
import json
import sys
from urllib.request import urlopen

start_url = sys.argv[1]
section = sys.argv[2]
repo_base = start_url.rsplit('/', 1)[0]
seen: set[str] = set()


def walk(url: str) -> None:
    if url in seen:
        return
    seen.add(url)
    with urlopen(url) as response:
        data = json.load(response)
    for entry in data.get(section, []):
        file = entry.get("file")
        if not file:
            continue
        if file.endswith("index.json"):
            walk(f"{repo_base}/{file}")
        else:
            print(file)


walk(start_url)
PY
  }

  SKILL_LIST=$(collect_files "$MARKETPLACE_RAW/index.json" skills)

  for skill_file in $SKILL_LIST; do
    dest="$SKILL_DIR/${skill_file#skills/}"
    mkdir -p "$(dirname "$dest")"
    echo "  ↓ $skill_file"
    curl -sSL "$MARKETPLACE_RAW/$skill_file" -o "$dest"
  done
  echo "  ✓ Skills installed"
fi

echo ""
echo "✅ Done! Restart Claude Code to pick up new agents and skills."
