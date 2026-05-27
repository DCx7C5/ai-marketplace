---
name: webapp-protocol-tls-verify
description: "--| | CPU overhead | 50-80% increase per session | Hardware SSL acceleration, dedicated decrypt appliance | | Throughput reduction | 40-60% typical | Size decryption hardware for peak encrypted traffic | | Latency increase | 1-5ms additional | Place inspection close to users | | TLS 1."
domain: cybersecurity
---

--|
| CPU overhead | 50-80% increase per session | Hardware SSL acceleration, dedicated decrypt appliance |
| Throughput reduction | 40-60% typical | Size decryption hardware for peak encrypted traffic |
| Latency increase | 1-5ms additional | Place inspection close to users |
| TLS 1.3 0-RTT | Cannot inspect 0-RTT data | Block 0-RTT or accept risk |
| Certificate pinning | Inspection fails | Add to exemption list |
| QUIC/HTTP3 | Bypasses traditional proxy | Block QUIC, force HTTP/2 |

## Compliance and Privacy

- **Employee Notice** - Notify users that network traffic is subject to inspection
- **Privacy Exemptions** - Exclude healthcare, financial, and legally privileged traffic
- **Data Handling** - Inspected cleartext must not be logged or stored unnecessarily
- **GDPR Compliance** - Document lawful basis for processing encrypted personal data
- **Certificate Pinning** - Maintain exemption list for applications using HPKP or built-in pins

## Best Practices

- **Start with Logging** - Deploy in detect-only mode first to identify certificate-pinned applications
- **Maintain Exemption List** - Keep a curated list of applications requiring decryption bypass
- **Block QUIC** - Block UDP/443 to force HTTP/2 through TLS inspection
- **Monitor Certificate Errors** - Track decryption errors in firewall logs
- **TLS 1.2 Minimum** - Enforce TLS 1.2 as minimum version; block SSLv3 and TLS 1.0/1.1
- **Key Protection** - Store inspection CA private key in HSM for production environments
- **Regular CA Rotation** - Plan for CA certificate rotation before expiration

## References

- [Palo Alto SSL Decryption](https://docs.paloaltonetworks.com/network-security/decryption)
- [Cisco SSL/TLS Proxy](https://www.cisco.com/c/en/us/td/docs/routers/sdwan/configuration/security/ios-xe-17/security-book-xe/m-ssl-proxy.html)
- [NIST SP 800-52 Rev 2 - TLS Configuration](https://csrc.nist.gov/publications/detail/sp/800-52/rev-2/final)
- [US-CERT Alert on HTTPS Inspection](https://www.cisa.gov/news-events/alerts/2017/03/13/https-interception-weakens-tls-security)
