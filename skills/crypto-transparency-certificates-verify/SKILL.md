---
name: crypto-transparency-certificates-verify
description: Certificate Transparency (CT) is an Internet security standard that creates a public, append-only log of all issued SSL/TLS certificates. Monitoring CT logs enables early detection of phishing domains that register certificates mimicking legitimate brands, unauthorized certificate issuance for owned domains, and certificate-based attack infrastruct
domain: cybersecurity
---
---------|--------|-------|-------------|
"""
    for cert in suspicious_certs[:20]:
        flags = "; ".join(cert.get("flags", []))
        report += (f"| {cert['common_name']} | {cert['issuer'][:30]} "
                   f"| {flags} | [View]({cert['crt_sh_url']}) |\n")

    report += f"""
## Real-Time Certstream Alerts
| Domain | Issuer | Reason | Detected |
|--------|--------|--------|----------|
"""
    for alert in certstream_alerts[:20]:
        report += (f"| {alert['domain']} | {alert['issuer']} "
                   f"| {alert['reason']} | {alert['detected_at'][:19]} |\n")

    report += """
## Recommendations
1. Add flagged domains to DNS sinkhole / web proxy blocklist
2. Submit takedown requests for confirmed phishing domains
3. Monitor CT logs continuously for new certificate registrations
4. Implement CAA DNS records to restrict certificate issuance for your domains
5. Deploy DMARC to prevent email spoofing from lookalike domains
"""
    with open(f"ct_report_{domain.replace('.','_')}.md", "w") as f:
        f.write(report)
    print(f"[+] CT report saved")
    return report

generate_ct_report(suspicious, alerts if 'alerts' in dir() else [], "mycompany.com")
```

## Validation Criteria

- crt.sh queries return certificate data for target domains
- Suspicious certificates identified based on lookalike patterns
- Certstream real-time monitoring detects new phishing certificates
- Subdomain enumeration produces comprehensive list from CT logs
- Alerts generated with reason classification
- CT intelligence report created with actionable recommendations

## References

- [crt.sh Certificate Search](https://crt.sh/)
- [Certstream Real-Time CT Monitor](https://certstream.calidog.io/)
- [River Security: CT Logs for Attack Surface Discovery](https://riversecurity.eu/finding-attack-surface-and-fraudulent-domains-via-certificate-transparency-logs/)
- [Let's Encrypt: Certificate Transparency Logs](https://letsencrypt.org/docs/ct-logs/)
- [SSLMate Cert Spotter](https://sslmate.com/certspotter/)
- [CyberSierra: CT Logs as Early Warning System](https://cybersierra.co/blog/ssl-certificate-transparency-logs/)