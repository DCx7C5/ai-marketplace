---
name: soc-hunting-data
description: - When hunting for data theft in compromised environments - After detecting unusual outbound data volumes or patterns - When investigating potential insider threat data theft - During incident response to determine what data was stolen - When threat intel indicates data exfiltration campaigns targeting your sector
domain: cybersecurity
---
------|-------------|
| T1041 | Exfiltration Over C2 Channel |
| T1048 | Exfiltration Over Alternative Protocol |
| T1048.001 | Exfiltration Over Symmetric Encrypted Non-C2 |
| T1048.002 | Exfiltration Over Asymmetric Encrypted Non-C2 |
| T1048.003 | Exfiltration Over Unencrypted/Obfuscated Non-C2 |
| T1567 | Exfiltration Over Web Service |
| T1567.002 | Exfiltration to Cloud Storage |
| T1052 | Exfiltration Over Physical Medium |
| T1029 | Scheduled Transfer |
| T1030 | Data Transfer Size Limits (staging) |
| T1537 | Transfer Data to Cloud Account |
| T1020 | Automated Exfiltration |

## Tools & Systems

| Tool | Purpose |
|------|---------|
| Splunk | SIEM for data volume analysis and SPL queries |
| Zeek | Network metadata for data flow analysis |
| Microsoft Defender for Cloud Apps | CASB for cloud exfiltration |
| Netskope | Cloud DLP and exfiltration detection |
| Suricata | Network IDS for protocol anomaly detection |
| RITA | DNS exfiltration and beacon detection |
| ExtraHop | Network traffic analysis for data flow |

## Common Scenarios

1. **Cloud Storage Exfiltration**: User uploads sensitive documents to personal Google Drive or Dropbox via browser.
2. **DNS Tunneling**: Malware exfiltrates data encoded in DNS subdomain queries to attacker-controlled nameserver.
3. **HTTPS Upload**: Compromised system POSTs large data blobs to C2 server over encrypted HTTPS.
4. **Email Attachment Exfiltration**: Insider forwards sensitive documents to personal email accounts.
5. **Staging and Compression**: Adversary stages data in compressed archives before slow exfiltration to avoid detection.

## Output Format

```
Hunt ID: TH-EXFIL-[DATE]-[SEQ]
Exfiltration Channel: [HTTP/DNS/Email/Cloud/USB]
Source: [Host/User]
Destination: [Domain/IP/Service]
Data Volume: [Bytes/MB/GB]
Time Period: [Start - End]
Protocol: [HTTPS/DNS/SMTP/SMB]
Files Involved: [Count/Types]
Risk Level: [Critical/High/Medium/Low]
Confidence: [High/Medium/Low]
```