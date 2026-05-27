---
name: webapp-tls-lifecycle-monitor
description: "-| | DV (Domain Validation) | Domain ownership | Websites, APIs | | OV (Organization Validation) | Domain + org identity | Business sites | | EV (Extended Validation) | Full legal verification | E-commerce, banking | | Wildcard | *."
domain: cybersecurity
---

-|
| DV (Domain Validation) | Domain ownership | Websites, APIs |
| OV (Organization Validation) | Domain + org identity | Business sites |
| EV (Extended Validation) | Full legal verification | E-commerce, banking |
| Wildcard | *.domain.com | Multi-subdomain |
| SAN/UCC | Multiple domains | Multi-domain hosting |

## Security Considerations

- Set up automated monitoring for all certificates
- Use ECDSA (P-256) certificates for better performance over RSA
- Enable OCSP stapling on all servers
- Implement Certificate Transparency log monitoring
- Maintain inventory of all certificates and their locations
- Plan for CA compromise scenarios (key pinning, backup CAs)

## Validation Criteria

- [ ] CSR generation produces valid PKCS#10 request
- [ ] Certificate parsing extracts all relevant fields
- [ ] Expiration monitoring detects certificates within threshold
- [ ] Certificate chain validation verifies trust path
- [ ] OCSP checking detects revoked certificates
- [ ] Certificate inventory tracks all deployed certificates
