---
name: net-assessment-ciscoise
description: "Net Assessment Ciscoise."
domain: cybersecurity
---

--|
| Employees (5) | Servers (10) | Permit_HTTP_HTTPS |
| Employees (5) | PCI_Zone (15) | Deny_All |
| IT-Admins (3) | Servers (10) | Permit_All |
| Guest (7) | Internet (99) | Permit_HTTP_HTTPS |
| Guest (7) | Servers (10) | Deny_All |

## Troubleshooting

```bash
# On switch - verify authentication status
show authentication sessions
show authentication sessions interface Gi1/0/1 details
show dot1x all

# Check RADIUS connectivity
test aaa server radius ISE-PRIMARY username testuser password testpass

# On ISE - check live logs
# Navigate to Operations > RADIUS > Live Logs
# Filter by MAC address or username
# Review Authentication Details for failure reason

# Common failure reasons:
# 12514 - EAP-TLS handshake failed (certificate issue)
# 22056 - Subject not found in identity store
# 24408 - User not found in Active Directory
# 24454 - User password expired
```

## Best Practices

- **Monitor Mode First** - Deploy in monitor mode (open authentication) before closed mode enforcement
- **Low-Impact Mode** - Use `authentication open` with pre-auth dACLs for gradual rollout
- **MAB Database** - Pre-populate endpoint database with known MAC addresses for printers, phones
- **Profiling** - Enable ISE profiling to automatically classify endpoints by type
- **CoA Support** - Ensure Change of Authorization is configured for dynamic policy updates
- **High Availability** - Deploy ISE in a Primary/Secondary node pair with PAN failover
- **Certificate Infrastructure** - Use machine certificates for EAP-TLS for strongest authentication

## References

- [Cisco ISE Admin Guide 3.1](https://www.cisco.com/c/en/us/td/docs/security/ise/3-1/admin_guide/b_ise_admin_3_1.html)
- [Cisco 802.1X Design Guide](https://www.cisco.com/c/en/us/support/docs/lan-switching/8021x/214843-guide-ieee-802-1x-deployment-with-cisco.html)
- [CiscoLive ISE Deployment Guide 2025](https://www.ciscolive.com/c/dam/r/ciscolive/emea/docs/2025/pdf/BRKSEC-2660.pdf)
- [Cisco ISE Wired 802.1X Configuration](https://www.networkcomputing.com/network-security/cisco-ise-wired-802-1x-configuration)
