---
name: ics-ics-architecture-purdue-configure
description: - When designing or retrofitting network architecture for an ICS/SCADA environment - When implementing IEC 62443 zone and conduit requirements in a brownfield plant - When creating the IT/OT DMZ (Level 3.5) to control data flow between enterprise and control networks - When remediating audit findings about flat OT networks or direct IT-to-OT connec
domain: cybersecurity
---
VLAN ASSIGNMENT ---")
        for v in vlan_plan:
            print(f"\n  {v['level_name']} (Purdue {v['purdue_level']})")
            print(f"    VLAN Range: {v['vlan_range']}")
            print(f"    Assets: {v['asset_count']}")
            print(f"    Allowed Protocols: {', '.join(v['allowed_protocols'])}")

        print(f"\n--- INTER-ZONE FIREWALL RULES ---")
        rules = self.generate_firewall_rules()
        for rule in rules:
            action_symbol = "+" if rule["action"] == "ALLOW" else "X"
            print(f"\n  [{action_symbol}] Rule {rule['rule_id']}: {rule['name']}")
            print(f"      {rule['source_zone']} -> {rule['dest_zone']}")
            print(f"      Service: {rule['service']}")
            print(f"      Reason: {rule['description']}")

if __name__ == "__main__":
    planner = PurdueSegmentationPlanner()
    if len(sys.argv) >= 2:
        planner.load_asset_inventory(sys.argv[1])
    classification = planner.classify_assets()
    planner.print_segmentation_plan(classification)
```

### Step 2: Configure Industrial DMZ (Level 3.5)

The DMZ is the critical boundary between IT and OT. All data exchange must traverse it -- no direct connections are permitted.

```yaml
# Level 3.5 DMZ Architecture Configuration
# All IT-OT data exchange flows through the DMZ

dmz_architecture:
  zone_name: "IT_OT_DMZ"
  purdue_level: 3.5
  vlan: 150

  components:
    historian_replica:
      purpose: "Read-only copy of OT historian data for IT/business access"
      direction: "OT pushes data TO DMZ (unidirectional)"
      ip: "10.10.150.10"
      services:
        - port: 1433
          protocol: "SQL"
          direction: "inbound from Level 3 historian only"
        - port: 443
          protocol: "HTTPS"
          direction: "outbound to Level 4 for IT consumers"

    jump_server:
      purpose: "Controlled remote access point for OT maintenance"
      ip: "10.10.150.20"
      services:
        - port: 3389
          protocol: "RDP"
          direction: "inbound from Level 4 with MFA"
        - port: 3389
          protocol: "RDP"
          direction: "outbound to Level 2 HMIs only"
      security_controls:
        - "Multi-factor authentication required"
        - "Session recording enabled"
        - "Maximum session duration: 4 hours"
        - "Approval-based access workflow"

    patch_server:
      purpose: "Staging area for tested patches before OT deployment"
      ip: "10.10.150.30"
      services:
        - port: 8530
          protocol: "WSUS"
          direction: "pulls from Level 4 WSUS, pushes to Level 2-3"

    antivirus_relay:
      purpose: "AV signature distribution to OT endpoints"
      ip: "10.10.150.40"
      services:
        - port: 443
          protocol: "HTTPS"
          direction: "pulls definitions from Level 4, distributes to Level 2-3"

  firewall_rules:
    north_firewall:  # Between DMZ and Level 4 Enterprise
      - allow: "Level 4 -> DMZ jump server:3389 (with MFA)"
      - allow: "Level 4 -> DMZ historian replica:443 (read-only)"
      - allow: "DMZ patch server -> Level 4 WSUS:8530 (pull only)"
      - deny: "ALL other traffic"

    south_firewall:  # Between DMZ and Level 3 Operations
      - allow: "Level 3 historian -> DMZ replica:1433 (push direction)"
      - allow: "DMZ jump server -> Level 2 HMI:3389 (session-limited)"
      - allow: "DMZ patch server -> Level 2/3:8530 (scheduled)"
      - deny: "ALL other traffic"

    critical_rule: "NO traffic passes through DMZ end-to-end. DMZ breaks all connections."
```

## Key Concepts

| Term | Definition |
|------|------------|
| Purdue Model (PERA) | Hierarchical reference architecture organizing industrial networks into levels 0-5 based on function and trust |
| Level 3.5 DMZ | Demilitarized zone between IT (Level 4) and OT (Level 3), where all cross-boundary data exchange occurs |
| Defense in Depth | Layered security approach requiring attackers to breach multiple boundaries to reach critical control systems |
| Data Diode | Hardware-enforced unidirectional communication device ensuring data flows only from OT to IT, never reverse |
| Zone | Logical grouping of assets sharing common security requirements as defined by IEC 62443 |
| Conduit | Controlled communication path between zones with defined security policies |

## Common Scenarios

### Scenario: Flat OT Network Remediation

**Context**: An audit reveals that enterprise IT systems can directly communicate with PLCs on the control network. There is no DMZ and no firewall between IT and OT.

**Approach**:
1. Perform full traffic analysis to identify all legitimate data flows crossing IT/OT boundary
2. Design DMZ architecture with historian replica, jump server, and patch staging
3. Deploy industrial firewall between IT and DMZ (north firewall) and between DMZ and OT (south firewall)
4. Migrate data flows one at a time: start with historian replication through DMZ
5. Implement jump server for remote access, deprecating direct RDP to OT systems
6. Block direct IT-to-OT traffic on the north firewall after all flows migrate through DMZ
7. Validate with penetration test from IT network confirming no direct path to Level 1 controllers

**Pitfalls**: Do not cut over all traffic simultaneously -- migrate flow by flow with rollback plans. Legacy OT systems may use protocols that cannot traverse firewalls doing DPI; test thoroughly in a lab first. Never deploy the DMZ during active production without an agreed maintenance window.

## Output Format

```
PURDUE MODEL SEGMENTATION REPORT
====================================
Assessment Date: YYYY-MM-DD
Facility: [Plant Name]

CURRENT STATE:
  Network Type: [Flat/Partially segmented/Fully segmented]
  IT-OT Boundary: [None/Firewall/DMZ with dual firewall]
  Direct IT-to-PLC paths: [count]

RECOMMENDED ARCHITECTURE:
  Level 0-1: VLAN 110 (Control Network)
  Level 2:   VLAN 120 (Supervisory Network)
  Level 3:   VLAN 130 (Operations Network)
  Level 3.5: VLAN 150 (IT/OT DMZ)
  Level 4-5: VLAN 200+ (Enterprise)

DMZ COMPONENTS:
  - Historian Replica Server
  - Jump Server (MFA-enabled)
  - Patch Staging Server
  - AV Relay Server

FIREWALL RULES: [count] rules generated
MIGRATION STEPS: [count] phases planned
```