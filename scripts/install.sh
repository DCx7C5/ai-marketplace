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

  # Fetch agent list from index.json
  AGENT_LIST=$(curl -sSL "$MARKETPLACE_RAW/index.json" | python3 -c "
import sys, json
data = json.load(sys.stdin)
for a in data.get('agents', []):
    print(a['file'])
")

  for agent_file in $AGENT_LIST; do
    name=$(basename "$agent_file")
    echo "  ↓ $name"
    curl -sSL "$MARKETPLACE_RAW/$agent_file" -o "$AGENT_DIR/$name"
  done
  echo "  ✓ Agents installed"
fi

if [[ "$INSTALL_SKILLS" == "true" ]]; then
  SKILL_DIR="$TARGET_DIR/.claude/skills"
  mkdir -p "$SKILL_DIR"
  echo "📦 Installing skills → $SKILL_DIR"

  SKILL_LIST=$(curl -sSL "$MARKETPLACE_RAW/index.json" | python3 -c "
import sys, json
data = json.load(sys.stdin)
for s in data.get('skills', []):
    print(s['file'])
")

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

