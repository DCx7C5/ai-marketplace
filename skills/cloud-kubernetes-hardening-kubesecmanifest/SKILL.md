---
name: cloud-kubernetes-hardening-kubesecmanifest
description: Kubesec is an open-source security risk analysis tool developed by ControlPlane that inspects Kubernetes resource manifests for common exploitable risks such as privilege escalation, writable host mounts, and excessive capabilities. It assigns a numerical security score to each resource and provides actionable recommendations for hardening. Kubesec
domain: cybersecurity
---
----|----------|------|
| Privileged | `securityContext.privileged == true` | Full host access |
| HostPID | `spec.hostPID == true` | Process namespace escape |
| HostNetwork | `spec.hostNetwork == true` | Network namespace escape |
| SYS_ADMIN | `capabilities.add contains SYS_ADMIN` | Near-root capability |

### Best Practice Checks (Positive Score)

| Check | Points | Description |
|-------|--------|-------------|
| ReadOnlyRootFilesystem | +1 | Prevents filesystem writes |
| RunAsNonRoot | +1 | Non-root process execution |
| RunAsUser > 10000 | +1 | High UID reduces collision risk |
| LimitsCPU | +1 | Prevents CPU resource exhaustion |
| LimitsMemory | +1 | Prevents memory resource exhaustion |
| RequestsCPU | +1 | Ensures scheduler resource awareness |
| ServiceAccountName | +3 | Explicit service account |
| AppArmor annotation | +3 | Kernel-level MAC enforcement |
| Seccomp profile | +4 | Syscall filtering |

## References

- [Kubesec GitHub Repository](https://github.com/controlplaneio/kubesec)
- [Kubesec Online Scanner](https://kubesec.io/)
- [ControlPlane Security Tools](https://controlplane.io/)
- [CIS Kubernetes Benchmark](https://www.cisecurity.org/benchmark/kubernetes)
- [Kubernetes Pod Security Standards](https://kubernetes.io/docs/concepts/security/pod-security-standards/)