#!/usr/bin/env python3
"""Audit helper dependencies across csmcp modules."""

import re
import json
from pathlib import Path
from collections import defaultdict
from typing import Dict, List, Any

def scan_helper_imports(root_path: str) -> Dict[str, List[Dict[str, Any]]]:
    """Scan all Python files for helper imports."""
    imports = defaultdict(list)
    
    # Pattern to match: from csmcp.X import Y
    patterns = [
        r'from csmcp\.(\w+)\s+import\s+(.+)',
        r'from csmcp\.(\w+)\.(\w+)\s+import\s+(.+)',
        r'from csmcp\.cybersec\.(\w+)\s+import\s+(.+)',
    ]
    
    root = Path(root_path)
    for py_file in root.rglob('*.py'):
        if '__pycache__' in str(py_file) or py_file.name.startswith('test_'):
            continue
        
        try:
            with open(py_file) as f:
                for line_num, line in enumerate(f, 1):
                    for pattern in patterns:
                        match = re.match(pattern, line.strip())
                        if match:
                            module_info = {
                                'file': str(py_file.relative_to(root)),
                                'line': line_num,
                                'import_line': line.strip(),
                                'groups': match.groups()
                            }
                            key = str(py_file.relative_to(root))
                            imports[key].append(module_info)
        except Exception as e:
            print(f"⚠️  Error scanning {py_file}: {e}")
    
    return imports

def analyze_dependencies(imports: Dict[str, List[Dict[str, Any]]]) -> Dict[str, Any]:
    """Analyze which helpers are imported by which modules."""
    analysis = {
        'module_imports': defaultdict(set),      # module.py → set of helper modules
        'helper_usage': defaultdict(set),        # helper_module → set of importing modules
        'critical_helpers': set(),               # helpers imported by all/most MCPs
        'optional_helpers': set(),               # helpers imported by few MCPs
        'by_mcp': defaultdict(set),              # MCP → set of imported helpers
    }
    
    mcp_mapping = {
        'incident': 'incident_management',
        'threat': 'threat_intelligence',
        'forensic': 'forensic_vault',
        'network': 'network_layers',
        'session': 'session_management',
        'database': 'database_tools',
        'browser': 'browser_automation',
        'orchestration': 'orchestration',
        'dystopian': 'dystopian_actors',
        'business': 'business_tools',
        'utility': 'utility_tools',
        'advanced': 'advanced_analysis',
    }
    
    for importing_file, import_list in imports.items():
        # Determine MCP from file path
        mcp = 'unknown'
        for keyword, mcp_name in mcp_mapping.items():
            if keyword in importing_file.lower():
                mcp = mcp_name
                break
        
        for import_info in import_list:
            groups = import_info['groups']
            if len(groups) >= 2:
                module = groups[0]
                if module not in ['__future__', '__main__']:
                    analysis['module_imports'][importing_file].add(module)
                    analysis['helper_usage'][module].add(importing_file)
                    analysis['by_mcp'][mcp].add(module)
    
    # Determine critical vs optional
    num_mcps = len(set(m for m in analysis['by_mcp'].values() if m != 'unknown'))
    for helper, users in analysis['helper_usage'].items():
        usage_count = len(users)
        # Critical if used by all MCPs
        if usage_count >= num_mcps * 0.8:  # 80% threshold
            analysis['critical_helpers'].add(helper)
        else:
            analysis['optional_helpers'].add(helper)
    
    return analysis

def output_markdown_report(analysis: Dict[str, Any], output_path: str) -> None:
    """Generate markdown report of helper dependencies."""
    report = """# Helper Dependency Map

This document shows which helpers are imported by which MCPs.

## Summary

**Critical Helpers** (used by most/all MCPs):
"""
    
    for helper in sorted(analysis['critical_helpers']):
        users = analysis['helper_usage'].get(helper, set())
        report += f"\n- `{helper}` — used by {len(users)} MCPs"
    
    report += "\n\n**Optional Helpers** (used by few MCPs):\n"
    for helper in sorted(analysis['optional_helpers']):
        users = analysis['helper_usage'].get(helper, set())
        report += f"\n- `{helper}` — used by {len(users)} MCPs"
    
    report += "\n\n## Helpers by MCP\n"
    for mcp in sorted(analysis['by_mcp'].keys()):
        if mcp != 'unknown':
            helpers = analysis['by_mcp'][mcp]
            report += f"\n### {mcp}\n"
            for helper in sorted(helpers):
                report += f"- `{helper}`\n"
    
    report += "\n\n## Integration with cybersecsuite_mcp_core\n\n"
    report += """
These helpers should be extracted into the shared package:

| Helper | Core Module | Functions |
|--------|-------------|-----------|
| db.py | db | init_database, migrations, ORM helpers |
| cache.py | cache | caching decorators, TTL management |
| validation.py | validation | Pydantic validators, schemas |
| logging.py | logging | structured logging setup |
| scope.py | scope | investigation scope, context |
| exceptions.py | exceptions | custom exception classes |
"""
    
    Path(output_path).write_text(report)
    print(f"✅ Markdown report: {output_path}")

def output_json_report(analysis: Dict[str, Any], output_path: str) -> None:
    """Generate JSON report of helper dependencies."""
    report = {
        'critical_helpers': sorted(analysis['critical_helpers']),
        'optional_helpers': sorted(analysis['optional_helpers']),
        'by_mcp': {
            mcp: sorted(list(helpers))
            for mcp, helpers in analysis['by_mcp'].items()
        },
        'helper_usage': {
            helper: len(users)
            for helper, users in analysis['helper_usage'].items()
        }
    }
    
    Path(output_path).write_text(json.dumps(report, indent=2))
    print(f"✅ JSON report: {output_path}")

def print_console_report(analysis: Dict[str, Any]) -> None:
    """Print report to console."""
    print("\n" + "="*80)
    print("HELPER DEPENDENCY ANALYSIS")
    print("="*80)
    
    print(f"\nCritical Helpers ({len(analysis['critical_helpers'])}):")
    for helper in sorted(analysis['critical_helpers']):
        users = analysis['helper_usage'][helper]
        print(f"  • {helper:20} used by {len(users)} modules")
    
    print(f"\nOptional Helpers ({len(analysis['optional_helpers'])}):")
    for helper in sorted(analysis['optional_helpers']):
        users = analysis['helper_usage'][helper]
        print(f"  • {helper:20} used by {len(users)} modules")
    
    print(f"\nHelpers by MCP:")
    for mcp in sorted(analysis['by_mcp'].keys()):
        if mcp != 'unknown':
            helpers = analysis['by_mcp'][mcp]
            print(f"  • {mcp:25} {len(helpers)} helpers")
    
    print("\n" + "="*80 + "\n")

def main():
    """Main entry point."""
    csmcp_path = '/home/daen/Projects/cybersecsuite/src/csmcp'
    
    print("🔍 Scanning helper imports in csmcp...")
    imports = scan_helper_imports(csmcp_path)
    print(f"Found {len(imports)} files with imports")
    
    print("📊 Analyzing dependencies...")
    analysis = analyze_dependencies(imports)
    
    print("📝 Generating reports...")
    output_markdown_report(analysis, 'docs/HELPER_DEPENDENCY_MAP.md')
    output_json_report(analysis, 'helper_dependency_map.json')
    
    print_console_report(analysis)
    
    print("✅ Helper dependency analysis complete")
    return 0

if __name__ == '__main__':
    import sys
    sys.exit(main())
