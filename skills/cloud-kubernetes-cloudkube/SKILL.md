---
name: cloud-kubernetes-cloudkube
description: "Cloud Kubernetes Cloudkube."
domain: cybersecurity
---

|
| Pod Security Standards | Three profiles (Privileged, Baseline, Restricted) enforced via Pod Security Admission that control pod security context capabilities |
| Workload Identity | Cloud-native mechanism binding Kubernetes service accounts to cloud IAM roles for credential-free cloud API access (IRSA, GKE WI, AKS MI) |
| Network Policy | Kubernetes resource defining allowed ingress and egress traffic flows between pods, enforced by the CNI plugin |
| Admission Controller | Kubernetes plugin that intercepts API requests before persistence to validate or mutate resources against security policies |
| RBAC | Role-Based Access Control in Kubernetes, defining what actions (verbs) identities can perform on which resources in which namespaces |
| Seccomp Profile | Linux kernel feature restricting the system calls a container process can make, reducing the kernel attack surface |
| Service Mesh | Infrastructure layer (Istio, Linkerd) providing mutual TLS, traffic policies, and observability for service-to-service communication |

## Tools & Systems

- **Falco**: Open-source runtime security engine detecting anomalous behavior in containers using kernel-level system call monitoring
- **Kyverno**: Kubernetes-native policy engine for admission control, mutation, and generation of resources based on security policies
- **kube-bench**: CIS Kubernetes Benchmark assessment tool checking cluster configuration against security best practices
- **Trivy**: Vulnerability scanner for container images, file systems, and Kubernetes resources with SBOM generation
- **Calico/Cilium**: CNI plugins providing network policy enforcement and advanced network security features including eBPF-based monitoring

## Common Scenarios

### Scenario: Cryptominer Deployed via Compromised Container Image

**Context**: GuardDuty Extended Threat Detection generates an AttackSequence:EKS/CompromisedCluster finding. A developer pulled a public Docker image containing an embedded XMRig cryptominer that executes at container startup.

**Approach**:
1. Isolate the affected pod by applying a deny-all network policy targeting its labels
2. Capture the container image digest and scan it with Trivy to identify the embedded binary
3. Review Kubernetes audit logs to identify who deployed the compromised image and when
4. Deploy Kyverno ClusterPolicy requiring images from approved private registries only
5. Enable image digest pinning to prevent tag mutation attacks
6. Deploy Falco with rules detecting crypto mining process signatures (/usr/bin/xmrig, stratum+tcp connections)

**Pitfalls**: Deleting the pod before capturing the image digest and audit logs destroys forensic evidence. Blocking only the specific image tag allows the attacker to re-push with a different tag.

## Output Format

```
Kubernetes Security Assessment Report
=======================================
Cluster: production-cluster (EKS 1.29)
Provider: AWS (us-east-1)
Assessment Date: 2025-02-23
Tool: kube-bench v0.8.0 + manual review

CIS KUBERNETES BENCHMARK RESULTS:
  Total Controls: 124
  Passed: 98 (79%)
  Failed: 18 (15%)
  Warnings: 8 (6%)

CRITICAL FINDINGS:
  [K8S-001] 3 namespaces lack Pod Security Standards enforcement
    Namespaces: monitoring, logging, default
    Remediation: Apply restricted PSA labels

  [K8S-002] Default service account tokens auto-mounted in 12 deployments
    Risk: Credential theft if container is compromised
    Remediation: Set automountServiceAccountToken: false

  [K8S-003] No network policies in production namespace
    Risk: Unrestricted lateral movement between all pods
    Remediation: Deploy default-deny policy with explicit allow rules

HIGH FINDINGS:
  [K8S-004] 5 pods running as root with privileged security context
  [K8S-005] Images deployed using mutable tags (:latest) in 8 deployments
  [K8S-006] RBAC ClusterRoleBinding grants cluster-admin to developers group
```
