---
name: net-capture-zeek-dnstunnel
description: "-| | T1071.004 | Application Layer Protocol: DNS | | T1048."
domain: cybersecurity
---

-|
| T1071.004 | Application Layer Protocol: DNS |
| T1048.003 | Exfiltration Over Alternative Protocol: DNS |
| T1572 | Protocol Tunneling |
| Shannon Entropy | Measure of randomness in subdomain strings |
| Zeek dns.log | DNS query/response metadata |
| RITA | Automated DNS tunneling detection from Zeek logs |
| iodine | IPv4-over-DNS tunneling tool |
| dnscat2 | DNS-based command-and-control tool |
| DNSExfiltrator | Data exfiltration tool using DNS requests |

## Detection Queries

### Zeek Script -- DNS Tunnel Detection
```zeek
@load base/protocols/dns
module DNSTunnel;

export {
    redef enum Notice::Type += { DNSTunnel::Long_DNS_Query };
    const query_length_threshold = 50 &redef;
    const query_count_threshold = 100 &redef;
}

event dns_request(c: connection, msg: dns_msg, query: string, qtype: count, qclass: count) {
    if ( |query| > query_length_threshold ) {
        NOTICE([$note=DNSTunnel::Long_DNS_Query,
                $msg=fmt("Long DNS query detected: %s (%d chars)", query, |query|),
                $conn=c]);
    }
}
```

### Splunk -- DNS Tunneling Indicators from Zeek
```spl
index=zeek sourcetype=bro_dns
| rex field=query "(?<subdomain>[^.]+)\.(?<basedomain>[^.]+\.[^.]+)$"
| stats count dc(subdomain) as unique_subs avg(len(query)) as avg_len max(len(query)) as max_len by src basedomain
| where count > 100 AND (unique_subs > 50 OR avg_len > 40)
| sort -unique_subs
```

### Splunk -- High Entropy Subdomain Detection
```spl
index=zeek sourcetype=bro_dns
| rex field=query "^(?<subdomain>[^.]+)"
| where len(subdomain) > 20
| eval char_count=len(subdomain)
| stats count dc(query) as unique_queries avg(char_count) as avg_sub_len by src query_type_name basedomain
| where unique_queries > 30 AND avg_sub_len > 25
| sort -unique_queries
```

### RITA Analysis
```bash
rita import /path/to/zeek/logs dataset_name
rita show-dns-fqdn-ips-long dataset_name
rita show-exploded-dns dataset_name
rita show-dns-tunneling dataset_name --csv > dns_tunnel_results.csv
```

## Common Scenarios

1. **dnscat2 C2**: Encodes command-and-control traffic in DNS CNAME/TXT queries with Base64-encoded subdomain labels. Produces high query volumes with long, high-entropy subdomains.
2. **iodine IPv4 Tunnel**: Creates a virtual network interface tunneling all IP traffic through DNS. Generates massive DNS query volumes with NULL record types.
3. **Data Exfiltration via DNS**: Sensitive data encoded in subdomain labels (e.g., `aGVsbG8gd29ybGQ.exfil.attacker.com`), sent as A or TXT queries. Each query carries ~63 bytes of data.
4. **DNS-over-HTTPS Tunneling**: Bypasses traditional DNS monitoring by sending DNS queries over HTTPS to public resolvers (8.8.8.8, 1.1.1.1), requiring TLS inspection for detection.
5. **Cobalt Strike DNS Beacon**: Uses DNS A/TXT records for C2 communication with configurable subdomain encoding schemes.

## Output Format

```
Hunt ID: TH-DNSTUNNEL-[DATE]-[SEQ]
Source IP: [Internal IP]
Source Host: [Hostname]
Target Domain: [Base domain]
Query Count: [Total queries in window]
Unique Subdomains: [Count]
Avg Query Length: [Characters]
Max Query Length: [Characters]
Subdomain Entropy: [Bits per character]
Primary Record Type: [A/TXT/CNAME/NULL]
Data Volume Estimate: [Bytes exfiltrated]
Risk Level: [Critical/High/Medium/Low]
```
