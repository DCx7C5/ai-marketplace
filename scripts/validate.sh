#!/usr/bin/env bash
# validate.sh — Validate agent and skill files in the marketplace
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
ERRORS=0

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

pass() { echo -e "${GREEN}✓${NC} $1"; }
fail() { echo -e "${RED}✗${NC} $1"; ((ERRORS++)); }
warn() { echo -e "${YELLOW}!${NC} $1"; }

# ── Validate agents ──────────────────────────────────────────────────────────
echo ""
echo "=== Validating Agents ==="
echo ""

for file in "$ROOT"/agents/*.md; do
  [[ -f "$file" ]] || continue
  filename=$(basename "$file" .md)
  normalized_filename=$(echo "$filename" | tr '[:upper:]_' '[:lower:]-')
  case "$normalized_filename" in
    agent-factory) allowed_names=("agent-factory") ;;
    vuln-scanner) allowed_names=("vuln-scanner" "vulnerability-scanner") ;;
    *) allowed_names=("$normalized_filename") ;;
  esac

  # Extract frontmatter (between first two ---)
  frontmatter=$(awk '/^---$/{if(f)exit;f=1;next}f' "$file")

  # Check required fields
  name=$(echo "$frontmatter" | grep '^name:' | sed 's/name: *//' | tr -d '"' || true)
  description=$(echo "$frontmatter" | grep '^description:' | sed 's/description: *//' || true)
  model=$(echo "$frontmatter" | grep '^model:' | sed 's/model: *//' || true)
  maxTurns=$(echo "$frontmatter" | grep '^maxTurns:' | sed 's/maxTurns: *//' || true)

  if [[ -z "$name" ]]; then
    fail "agents/$filename.md: missing 'name' field"
  else
    normalized_name=$(echo "$name" | tr '[:upper:]_' '[:lower:]-')
    matched=false
    for allowed in "${allowed_names[@]}"; do
      if [[ "$normalized_name" == "$allowed" ]]; then
        matched=true
        break
      fi
    done
    if [[ "$matched" == "false" ]]; then
      fail "agents/$filename.md: name '$name' does not match filename '$filename'"
    else
      pass "agents/$filename.md: name matches"
    fi
  fi

  if [[ -z "$description" ]]; then
    fail "agents/$filename.md: missing 'description' field"
  else
    desc_len=${#description}
    if [[ $desc_len -gt 220 ]]; then
      warn "agents/$filename.md: description is long ($desc_len chars), keep under 200"
    else
      pass "agents/$filename.md: description present"
    fi
  fi

  if [[ -z "$model" ]]; then
    warn "agents/$filename.md: missing 'model' field"
  elif [[ "$model" != "sonnet" && "$model" != "haiku" && "$model" != "opus" ]]; then
    warn "agents/$filename.md: model '$model' is non-standard"
  else
    pass "agents/$filename.md: model=$model"
  fi

  if [[ -z "$maxTurns" ]]; then
    warn "agents/$filename.md: missing 'maxTurns' field"
  fi
done

# ── Validate skills ───────────────────────────────────────────────────────────
echo ""
echo "=== Validating Skills ==="
echo ""

while IFS= read -r -d '' file; do
  rel="${file#"${ROOT}"/skills/}"
  dir=$(dirname "$rel")

  frontmatter=$(awk '/^---$/{if(f)exit;f=1;next}f' "$file")
  name=$(echo "$frontmatter" | grep '^name:' | sed 's/name: *//' | tr -d '"' || true)
  description=$(echo "$frontmatter" | grep '^description:' | sed 's/description: *//' || true)

  if [[ -z "$name" ]]; then
    fail "skills/$rel: missing 'name' field"
  else
    pass "skills/$rel: name='$name'"
  fi

  if [[ -z "$description" ]]; then
    fail "skills/$rel: missing 'description' field"
  else
    pass "skills/$rel: description present"
  fi
done < <(find "$ROOT/skills" -name "SKILL.md" -print0)

# ── Summary ───────────────────────────────────────────────────────────────────
echo ""
if [[ $ERRORS -eq 0 ]]; then
  echo -e "${GREEN}All validations passed!${NC}"
  exit 0
else
  echo -e "${RED}$ERRORS error(s) found.${NC}"
  exit 1
fi
