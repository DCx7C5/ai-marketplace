---
name: net-layer3-bgp-hijack
description: - Assessing an organization's exposure to BGP prefix hijacking and route leak attacks - Testing RPKI (Resource Public Key Infrastructure) deployment and route origin validation effectiveness - Validating BGP monitoring and alerting systems detect unauthorized route announcements - Simulating BGP hijacking in isolated lab environments to train netwo
domain: cybersecurity
---
")
PYEOF

# Check RPKI status via RIPEstat
curl -s "https://stat.ripe.net/data/rpki-validation/data.json?resource=AS65001&prefix=10.0.0.0/24" | python3 -m json.tool
```

## Key Concepts

| Term | Definition |
|------|------------|
| **BGP Hijacking** | Unauthorized announcement of IP prefixes by an AS that does not own them, diverting traffic through the attacker's network |
| **More-Specific Hijack** | Announcing longer (more-specific) prefixes than the victim's, which always win in IP routing due to longest-prefix-match rule |
| **RPKI (Resource PKI)** | Cryptographic framework that allows IP prefix holders to authorize specific ASNs to originate their routes via Route Origin Authorizations (ROAs) |
| **Route Origin Authorization (ROA)** | Digitally signed object that authorizes an AS to originate a specific IP prefix, enabling RPKI-based route validation |
| **AS Path Prepending** | BGP technique of adding duplicate AS numbers to the AS path to make a route less preferred, also used defensively against hijacking |
| **Route Leak** | Propagation of BGP routing announcements beyond their intended scope, such as a customer re-advertising transit provider routes to other providers |

## Tools & Systems

- **Containerlab**: Network lab orchestration tool for deploying virtual router topologies using Docker containers
- **FRRouting (FRR)**: Open-source routing suite supporting BGP, OSPF, IS-IS with RPKI validation capabilities
- **BGPalerter**: Real-time BGP monitoring tool that detects prefix hijacking, route leaks, and RPKI status changes
- **Routinator**: RPKI Relying Party software that validates ROAs and provides validated prefix-origin data to routers
- **pybgpstream**: Python library for analyzing historical and real-time BGP data from RouteViews and RIPE RIS collectors

## Common Scenarios

### Scenario: Assessing an Organization's BGP Hijacking Resilience

**Context**: A cloud hosting company (AS12345) announces 203.0.113.0/24 for their customer-facing services. They need to assess their resilience to BGP hijacking attacks and verify their RPKI deployment is effective. The assessment includes lab simulation and real-world monitoring validation.

**Approach**:
1. Build a Containerlab topology replicating the organization's BGP peering with two upstream ISPs
2. Verify that ROA records are correctly published for all the organization's prefixes using RIPEstat
3. Simulate a more-specific prefix hijack (/25) from a rogue AS and verify that upstream ISPs with RPKI validation drop the invalid routes
4. Simulate an exact-match origin hijack and verify that RPKI ROV marks the route as invalid
5. Test route leak scenarios where a customer AS re-announces the provider's prefix
6. Deploy BGPalerter in production to continuously monitor for unauthorized announcements
7. Verify that the organization's ISPs have proper prefix filtering (IRR-based and RPKI) configured

**Pitfalls**:
- Testing BGP hijacking on real internet infrastructure instead of isolated lab environments
- Assuming RPKI alone prevents all hijacking -- many networks still do not validate RPKI
- Not testing more-specific prefix announcements, which bypass origin validation if no max-length is set in ROAs
- Overlooking route leak scenarios where authorized peers inadvertently redistribute routes

## Output Format

```
## BGP Security Assessment Report

**Organization**: Cloud Hosting Co. (AS12345)
**Prefixes Assessed**: 203.0.113.0/24, 198.51.100.0/24
**Assessment Date**: 2024-03-15

### RPKI Status

| Prefix | ROA Exists | Max Length | Origin AS | Status |
|--------|-----------|------------|-----------|--------|
| 203.0.113.0/24 | Yes | /24 | AS12345 | Valid |
| 198.51.100.0/24 | No | N/A | AS12345 | Not Found |

### Lab Simulation Results

| Attack Type | RPKI Validation | Result |
|-------------|-----------------|--------|
| More-specific /25 hijack | Enabled | BLOCKED (Invalid origin) |
| More-specific /25 hijack | Disabled | SUCCESSFUL (traffic diverted) |
| Exact-match origin hijack | Enabled | BLOCKED (Invalid origin) |
| Route leak via customer | Enabled | NOT BLOCKED (valid origin, wrong path) |

### Recommendations
1. Create ROA for 198.51.100.0/24 (currently unprotected)
2. Set max-length to /24 in ROAs to prevent more-specific hijacks
3. Request upstream ISPs enable RPKI Route Origin Validation
4. Deploy BGPalerter for continuous prefix monitoring
5. Register with IRR databases and request prefix filtering from peers
```