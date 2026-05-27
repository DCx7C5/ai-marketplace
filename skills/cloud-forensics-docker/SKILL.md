---
name: cloud-forensics-docker
description: - When investigating a compromised Docker container or container host - For analyzing malicious Docker images pulled from registries - During incident response involving containerized application breaches - When examining container escape attempts or privilege escalation - For auditing container configurations and identifying misconfigurations
domain: cybersecurity
---
------|-------------|
| Image layers | Read-only filesystem layers stacked to form the container image |
| overlay2 | Default Docker storage driver using union filesystem for layers |
| Container diff | Comparison of runtime filesystem changes against the original image |
| Privileged mode | Container with full host capabilities (bypasses most isolation) |
| Docker socket | Unix socket (/var/run/docker.sock) controlling the Docker daemon |
| Container escape | Technique for breaking out of container isolation to the host |
| Volume mounts | Host filesystem paths made accessible inside the container |
| Image history | Record of Dockerfile instructions used to build each layer |

## Tools & Systems

| Tool | Purpose |
|------|---------|
| docker inspect | Detailed container configuration and state information |
| docker diff | Show filesystem changes made in a running/stopped container |
| dive | Interactive Docker image layer analysis tool |
| container-diff | Google tool for comparing container image contents |
| Trivy | Vulnerability scanner for container images and filesystems |
| docker-explorer | Forensic tool for offline Docker artifact analysis |
| Sysdig | Container runtime security monitoring and forensics |
| Falco | Runtime threat detection for containers and Kubernetes |

## Common Scenarios

**Scenario 1: Web Application Container Compromise**
Export the container filesystem, identify webshells in web root, analyze access logs for exploitation attempts, check for added files and modified configurations, examine network connections for C2 communication, review container capabilities for escalation paths.

**Scenario 2: Supply Chain Attack via Malicious Image**
Analyze image layers with dive to identify which layer added malicious content, compare with the official base image using container-diff, check image history for suspicious RUN commands, scan for embedded backdoors and cryptocurrency miners, trace the image pull from registry logs.

**Scenario 3: Container Escape Investigation**
Check if container ran privileged or with dangerous capabilities, examine host filesystem mount points for unauthorized access, review Docker socket mount enabling Docker-in-Docker abuse, analyze host system logs for container escape indicators, check for kernel exploit artifacts.

**Scenario 4: Cryptojacking in Container Environment**
Identify high-CPU containers, export and analyze the container image for mining binaries, check for unauthorized images in the registry, review container creation events for rogue deployments, examine network connections for mining pool communications.

## Output Format

```
Docker Container Forensics Summary:
  Container: abc123def456 (nginx-app)
  Image: company/web-app:v2.1
  Status: Running (started 2024-01-10 09:00 UTC)
  Host: docker-host-01.corp.local

  Security Configuration:
    Privileged: No
    Capabilities Added: NET_ADMIN (WARNING)
    Volume Mounts: /var/log -> /host-logs (RW)
    Network Mode: bridge
    User: root (WARNING)

  Filesystem Changes:
    Added: 23 files (5 suspicious)
    Changed: 12 files (2 suspicious)
    Deleted: 0 files

  Suspicious Findings:
    /tmp/reverse.sh - Reverse shell script (Added)
    /var/www/html/.hidden/shell.php - PHP webshell (Added)
    /etc/crontab - Modified (persistence cron entry added)
    /root/.ssh/authorized_keys - Modified (unauthorized key added)

  Vulnerability Scan:
    Critical: 3 (CVE-2024-xxxx in base image)
    High: 12
    Medium: 34

  Evidence: /cases/case-2024-001/docker/
```