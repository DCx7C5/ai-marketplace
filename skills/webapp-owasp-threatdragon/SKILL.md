---
name: webapp-owasp-threatdragon
description: "Webapp Owasp Threatdragon."
domain: cybersecurity
---

Integrate into SDLC

- Conduct threat modeling during the design phase of new features
- Update threat models when architecture changes occur
- Review threat models during security design reviews
- Store threat model files in version control alongside code
- Reference threat model findings in security acceptance criteria

## Threat Model File Format

Threat Dragon uses JSON format for threat models, enabling version control and programmatic manipulation:

```json
{
  "version": "2.2.0",
  "summary": {
    "title": "E-Commerce Application",
    "owner": "Security Team",
    "description": "Threat model for the checkout flow"
  },
  "detail": {
    "contributors": [
      {"name": "Security Architect"}
    ],
    "diagrams": [
      {
        "id": 0,
        "title": "Checkout Flow",
        "diagramType": "STRIDE",
        "cells": []
      }
    ]
  }
}
```

## CycloneDX TMBOM Integration

Threat Dragon participates in the CycloneDX Threat Model Bill of Materials (TMBOM) effort, enabling export to a common format that can be consumed by other threat modeling tools and GRC platforms, preventing vendor lock-in.

## Best Practices

1. **Start simple**: Begin with high-level DFDs (Level 0) before decomposing into detailed diagrams
2. **Involve developers**: Include development team members in threat modeling sessions for realistic threat assessment
3. **Time-box sessions**: Limit initial sessions to 90 minutes; iterate in follow-up sessions
4. **Prioritize by risk**: Use severity ratings (Critical, High, Medium, Low) to prioritize mitigations
5. **Living documents**: Treat threat models as living documents that evolve with the system
6. **Automate where possible**: Use the rule engine for initial threat generation, then refine manually

## References

- [OWASP Threat Dragon](https://owasp.org/www-project-threat-dragon/)
- [Threat Dragon GitHub Repository](https://github.com/OWASP/threat-dragon)
- [OWASP Threat Modeling Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Threat_Modeling_Cheat_Sheet.html)
- [STRIDE Threat Model](https://learn.microsoft.com/en-us/azure/security/develop/threat-modeling-tool-threats)
- [LINDDUN Privacy Threat Modeling](https://www.linddun.org/)
