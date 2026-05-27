---
name: cloud-containers-docker
description: Hardening Docker containers for production involves applying security best practices aligned with CIS Docker Benchmark v1.8.0 to minimize attack surface, prevent privilege escalation, and enforce least-privilege principles across Docker daemon, images, containers, and runtime configurations.
domain: cybersecurity
---
------|---------------|-------------|
| Non-root user | USER instruction in Dockerfile | 4.1 |
| Read-only rootfs | --read-only flag | 5.12 |
| Drop capabilities | --cap-drop ALL | 5.3 |
| Resource limits | --memory, --cpus, --pids-limit | 5.10 |
| No new privileges | --security-opt no-new-privileges | 5.25 |
| Content trust | DOCKER_CONTENT_TRUST=1 | 4.5 |
| TLS for daemon | daemon.json TLS config | 2.6 |
| Audit logging | auditd rules | 1.1 |

## References

- [CIS Docker Benchmark](https://www.cisecurity.org/benchmark/docker)
- [Docker Security Best Practices](https://docs.docker.com/engine/security/)
- [Docker Bench Security Tool](https://github.com/docker/docker-bench-security)
- [Hadolint - Dockerfile Linter](https://github.com/hadolint/hadolint)