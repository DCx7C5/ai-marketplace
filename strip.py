#!/usr/bin/env python3
import re
import yaml
from pathlib import Path

def strip_frontmatter(file_path: Path):
    try:
        content = file_path.read_text(encoding="utf-8")
    except Exception as e:
        print(f"❌ Error reading {file_path}: {e}")
        return False

    # Quick pre-check: look for --- in first 150 characters
    if '---' not in content[:150]:
        print(f"⚠️  No frontmatter marker in first 150 chars: {file_path}")
        return False

    # Match the first frontmatter block
    match = re.search(r"^(?:---\s*\n(.*?)^\s*---\s*\n)", content, re.DOTALL | re.MULTILINE)
    if not match:
        print(f"⚠️  No valid frontmatter block found: {file_path}")
        return False

    front_text = match.group(1)
    body = content[match.end():]

    try:
        front = yaml.safe_load(front_text) or {}
        new_front = {k: front.get(k) for k in ["name", "description"] if k in front}
        
        new_front_text = "---\n" + yaml.dump(new_front, sort_keys=False, allow_unicode=True).strip() + "\n---\n"
        new_content = new_front_text + body
        
        file_path.write_text(new_content, encoding="utf-8")
        print(f"✅ Stripped: {file_path}")
        return True
    except yaml.YAMLError as e:
        print(f"❌ YAML error in {file_path}: {e}")
        return False
    except Exception as e:
        print(f"❌ Unexpected error in {file_path}: {e}")
        return False

if __name__ == "__main__":
    count = 0
    
    print("=== Processing agents/ ===")
    for md_file in Path("agents").rglob("*.md"):
        if strip_frontmatter(md_file):
            count += 1
    
    print("\n=== Processing skills/ (ONLY SKILL.md files) ===")
    for md_file in Path("skills").rglob("SKILL.md"):
        if strip_frontmatter(md_file):
            count += 1
    
    print(f"\nDone! Successfully stripped {count} files.")
