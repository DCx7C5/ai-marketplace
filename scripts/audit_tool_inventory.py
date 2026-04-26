#!/usr/bin/env python3
"""Audit all tools in csmcp and generate inventory CSV."""

import re
import json
from pathlib import Path
from collections import defaultdict
from typing import List, Dict, Any

# Tool mapping heuristics
TOOL_MAPPING = {
    'incident': 'incident_management',
    'finding': 'incident_management',
    'case': 'incident_management',
    'ioc': 'threat_intelligence',
    'mitre': 'threat_intelligence',
    'intelligence': 'threat_intelligence',
    'vault': 'forensic_vault',
    'forensic': 'forensic_vault',
    'network': 'network_layers',
    'protocol': 'network_layers',
    'connection': 'network_layers',
    'session': 'session_management',
    'user_context': 'session_management',
    'browser': 'browser_automation',
    'query': 'advanced_analysis',
    'orchestrate': 'orchestration',
    'orchestrator': 'orchestration',
    'dystopian': 'dystopian_actors',
    'apt': 'dystopian_actors',
}

def discover_tools(root_path: str) -> List[Dict[str, Any]]:
    """Find all tool definitions in csmcp."""
    tools = []
    pattern = r'^async def (mcp__\w+__\w+)\('
    
    root = Path(root_path)
    for py_file in root.rglob('*.py'):
        # Skip test/cache files
        if '__pycache__' in str(py_file) or py_file.name.startswith('test_'):
            continue
            
        try:
            with open(py_file) as f:
                for line_num, line in enumerate(f, 1):
                    match = re.match(pattern, line.strip())
                    if match:
                        tool_name = match.group(1)
                        tools.append({
                            'name': tool_name,
                            'source_file': str(py_file.relative_to(root)),
                            'line_number': line_num,
                        })
        except Exception as e:
            print(f"⚠️  Error parsing {py_file}: {e}")
    
    return tools

def determine_target_mcp(tool_name: str) -> str:
    """Map tool name to target MCP using heuristics."""
    # Extract function name from tool_name: mcp__namespace__function
    parts = tool_name.split('__')
    if len(parts) < 3:
        return 'unknown'
    
    namespace = parts[1]
    function = parts[2]
    
    # Check namespace first
    if namespace == 'dystopian':
        return 'dystopian_actors'
    elif namespace == 'cybersec':
        # Use function name to determine MCP
        for keyword, mcp in TOOL_MAPPING.items():
            if keyword in function.lower():
                return mcp
        return 'utility_tools'  # default fallback
    
    return namespace

def map_tools(tools: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Map each tool to target MCP."""
    for tool in tools:
        tool['target_mcp'] = determine_target_mcp(tool['name'])
        # Determine phase based on MCP
        mcp_phases = {
            'database_tools': 2,
            'forensic_vault': 2,
            'network_layers': 2,
            'threat_intelligence': 2,
            'incident_management': 3,
            'session_management': 3,
            'advanced_analysis': 3,
            'browser_automation': 4,
            'utility_tools': 4,
            'business_tools': 4,
            'orchestration': 4,
            'dystopian_actors': 5,
        }
        tool['phase'] = mcp_phases.get(tool['target_mcp'], 0)
        tool['status'] = 'mapped'
    
    return tools

def validate_tools(tools: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Validate tool inventory."""
    validation = {
        'total_tools': len(tools),
        'orphaned_tools': [],
        'collisions': [],
        'by_mcp': defaultdict(int),
        'by_phase': defaultdict(int),
    }
    
    seen_names = {}
    
    for tool in tools:
        # Check for orphans
        if tool['target_mcp'] == 'unknown':
            validation['orphaned_tools'].append(tool['name'])
            tool['status'] = 'orphan'
        
        # Check for collisions
        if tool['name'] in seen_names:
            collision = {
                'name': tool['name'],
                'files': [seen_names[tool['name']]['source_file'], tool['source_file']]
            }
            validation['collisions'].append(collision)
            tool['status'] = 'collision'
        else:
            seen_names[tool['name']] = tool
        
        # Count by MCP
        validation['by_mcp'][tool['target_mcp']] += 1
        
        # Count by phase
        validation['by_phase'][tool['phase']] += 1
    
    return validation

def output_csv(tools: List[Dict[str, Any]], output_path: str) -> None:
    """Write tools to CSV file."""
    import csv
    
    csv_path = Path(output_path)
    csv_path.parent.mkdir(parents=True, exist_ok=True)
    
    fields = ['name', 'source_file', 'target_mcp', 'phase', 'status', 'line_number']
    
    with open(csv_path, 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writeheader()
        
        for tool in sorted(tools, key=lambda t: (t['target_mcp'], t['name'])):
            writer.writerow({field: tool.get(field, '') for field in fields})
    
    print(f"✅ CSV output: {csv_path}")

def print_report(validation: Dict[str, Any]) -> None:
    """Print validation report."""
    print("\n" + "="*80)
    print("TOOL INVENTORY AUDIT RESULTS")
    print("="*80)
    
    print(f"\nTotal tools found: {validation['total_tools']}")
    
    print("\nTools by MCP:")
    for mcp in sorted(validation['by_mcp'].keys()):
        count = validation['by_mcp'][mcp]
        print(f"  • {mcp:30} {count:3} tools")
    
    print(f"\nTools by Phase:")
    for phase in sorted(validation['by_phase'].keys()):
        if phase > 0:
            count = validation['by_phase'][phase]
            print(f"  • Phase {phase}: {count} tools")
    
    if validation['orphaned_tools']:
        print(f"\n⚠️  Orphaned tools ({len(validation['orphaned_tools'])}):")
        for tool in validation['orphaned_tools']:
            print(f"  • {tool}")
    else:
        print("\n✓ No orphaned tools")
    
    if validation['collisions']:
        print(f"\n⚠️  Tool collisions ({len(validation['collisions'])}):")
        for collision in validation['collisions']:
            print(f"  • {collision['name']}")
            for file in collision['files']:
                print(f"    - {file}")
    else:
        print("✓ No tool collisions")
    
    # Verify total
    total_by_phase = sum(validation['by_phase'].values())
    if total_by_phase == validation['total_tools'] and not validation['orphaned_tools']:
        print(f"\n✅ SUCCESS: All {validation['total_tools']} tools accounted for")
        return 0
    else:
        print(f"\n❌ FAILURE: Tool count mismatch or orphans found")
        return 1

def main():
    """Main entry point."""
    csmcp_path = '/home/daen/Projects/cybersecsuite/src/csmcp'
    output_csv_path = 'tools_inventory.csv'
    
    print("🔍 Discovering tools in csmcp...")
    tools = discover_tools(csmcp_path)
    print(f"Found {len(tools)} tools")
    
    print("🗺️  Mapping tools to MCPs...")
    tools = map_tools(tools)
    
    print("✅ Validating inventory...")
    validation = validate_tools(tools)
    
    print("📝 Writing CSV...")
    output_csv(tools, output_csv_path)
    
    exit_code = print_report(validation)
    
    print("="*80 + "\n")
    return exit_code

if __name__ == '__main__':
    import sys
    sys.exit(main())
