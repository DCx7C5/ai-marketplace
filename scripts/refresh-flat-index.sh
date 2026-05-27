#!/bin/bash
set -euo pipefail

echo "=== Refreshing flat-only index and hashes ==="
echo ""

# 1. Verify all flat skills have name: matching directory
echo "[1/4] Verifying name: matches directory name for all flat skills..."
MISMATCH_COUNT=$(python3 -c '
import re
from pathlib import Path
root = Path("skills")
mismatches = 0
for d in root.glob("*"):
    if not d.is_dir() or "-" not in d.name: continue
    md = d / "SKILL.md"
    if not md.exists(): continue
    m = re.search(r"^name:\s*(.+)$", md.read_text(), re.MULTILINE)
    if m:
        name = m.group(1).strip().strip("\"'\''")
        if name != d.name:
            mismatches += 1
print(mismatches)
')

if [ "$MISMATCH_COUNT" -ne 0 ]; then
    echo "ERROR: Found $MISMATCH_COUNT name mismatches. Fix before continuing."
    python3 -c '
import re
from pathlib import Path
root = Path("skills")
for d in root.glob("*"):
    if not d.is_dir() or "-" not in d.name: continue
    md = d / "SKILL.md"
    if not md.exists(): continue
    m = re.search(r"^name:\s*(.+)$", md.read_text(), re.MULTILINE)
    if m:
        name = m.group(1).strip().strip("\"'\''")
        if name != d.name:
            print(f"MISMATCH: {d.name} -> {name}")
    '
    exit 1
fi
echo "✓ All flat names match directory names"
echo ""

# 2. Regenerate index.json (flat only)
echo "[2/4] Regenerating index.json (flat skills only)..."
python3 scripts/generate_index.py
echo ""

# 3. Update sha512
echo "[3/4] Updating index.json.sha512..."
sha512sum index.json | cut -d' ' -f1 > index.json.sha512
echo "New hash: $(cat index.json.sha512)"
echo ""

# 4. Run validation
echo "[4/4] Running validate.sh..."
./scripts/validate.sh
echo ""

echo "=== Done. index.json and index.json.sha512 are now up to date. ==="
