---
name: cloud-kubernetes-net-kubernetes
description: Calico is an open-source CNI plugin that provides fine-grained network policy enforcement for Kubernetes clusters. It implements the full Kubernetes NetworkPolicy API and extends it with Calico-specific GlobalNetworkPolicy, supporting policy ordering, deny rules, and service-account-based selectors.
domain: cybersecurity
---
# deny-all-egress.yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
name: cloud-kubernetes-net-kubernetes
  namespace: production
spec:
  podSelector: {}
  policyTypes:
    - Egress
```

### Allow Specific Pod-to-Pod Communication

```yaml
# allow-frontend-to-backend.yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
name: cloud-kubernetes-net-kubernetes
  namespace: production
spec:
  podSelector:
    matchLabels:
      app: backend
  policyTypes:
    - Ingress
  ingress:
    - from:
        - podSelector:
            matchLabels:
              app: frontend
      ports:
        - protocol: TCP
          port: 8080
```

### Allow DNS Egress

```yaml
# allow-dns-egress.yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
name: cloud-kubernetes-net-kubernetes
  namespace: production
spec:
  podSelector: {}
  policyTypes:
    - Egress
  egress:
    - to:
        - namespaceSelector: {}
      ports:
        - protocol: UDP
          port: 53
        - protocol: TCP
          port: 53
```

### Namespace Isolation

```yaml
# allow-same-namespace.yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
name: cloud-kubernetes-net-kubernetes
  namespace: production
spec:
  podSelector: {}
  policyTypes:
    - Ingress
  ingress:
    - from:
        - podSelector: {}
```

## Calico-Specific Policies

### GlobalNetworkPolicy (Cluster-Wide)

```yaml
# global-deny-external.yaml
apiVersion: projectcalico.org/v3
kind: GlobalNetworkPolicy
metadata:
name: cloud-kubernetes-net-kubernetes
spec:
  order: 100
  selector: "projectcalico.org/namespace != 'ingress-nginx'"
  types:
    - Ingress
  ingress:
    - action: Deny
      source:
        nets:
          - 0.0.0.0/0
      destination: {}
```

### Calico NetworkPolicy with Deny Rules

```yaml
# calico-deny-policy.yaml
apiVersion: projectcalico.org/v3
kind: NetworkPolicy
metadata:
name: cloud-kubernetes-net-kubernetes
  namespace: production
spec:
  order: 10
  selector: app == 'database'
  types:
    - Ingress
  ingress:
    - action: Deny
      source:
        selector: app == 'frontend'
    - action: Allow
      source:
        selector: app == 'backend'
      destination:
        ports:
          - 5432
```

### Service Account Based Policy

```yaml
# sa-based-policy.yaml
apiVersion: projectcalico.org/v3
kind: NetworkPolicy
metadata:
name: cloud-kubernetes-net-kubernetes
  namespace: production
spec:
  selector: app == 'api'
  ingress:
    - action: Allow
      source:
        serviceAccounts:
          names:
            - frontend-sa
            - monitoring-sa
  egress:
    - action: Allow
      destination:
        serviceAccounts:
          names:
            - database-sa
```

### Host Endpoint Protection

```yaml
# host-endpoint-policy.yaml
apiVersion: projectcalico.org/v3
kind: GlobalNetworkPolicy
metadata:
name: cloud-kubernetes-net-kubernetes
spec:
  order: 10
  selector: "has(kubernetes.io/hostname)"
  applyOnForward: false
  types:
    - Ingress
  ingress:
    - action: Allow
      protocol: TCP
      source:
        nets:
          - 10.0.0.0/8
      destination:
        ports:
          - 22
    - action: Deny
      protocol: TCP
      destination:
        ports:
          - 22
```

## Calico Policy Tiers

```yaml
# security-tier.yaml
apiVersion: projectcalico.org/v3
kind: Tier
metadata:
name: cloud-kubernetes-net-kubernetes
spec:
  order: 100

---
# platform-tier.yaml
apiVersion: projectcalico.org/v3
kind: Tier
metadata:
  name: platform
spec:
  order: 200
```

## Monitoring and Troubleshooting

```bash
# List all network policies
kubectl get networkpolicy --all-namespaces

# List Calico-specific policies
kubectl exec -n calico-system calicoctl -- calicoctl get networkpolicy --all-namespaces -o wide
kubectl exec -n calico-system calicoctl -- calicoctl get globalnetworkpolicy -o wide

# Check policy evaluation for a specific endpoint
kubectl exec -n calico-system calicoctl -- calicoctl get workloadendpoint -n production -o yaml

# View Calico logs
kubectl logs -n calico-system -l k8s-app=calico-node --tail=100

# Test connectivity
kubectl exec -n production frontend-pod -- wget -qO- --timeout=2 http://backend-svc:8080/health
```

## Best Practices

1. **Start with default deny** - Apply deny-all policies to every namespace, then allow specific traffic
2. **Use labels consistently** - Define a labeling standard for app, tier, environment
3. **Order policies** - Use Calico policy ordering (`order` field) to control evaluation precedence
4. **Allow DNS first** - Always create DNS egress rules before applying egress deny policies
5. **Use GlobalNetworkPolicy** for cluster-wide security baselines
6. **Test policies in staging** - Validate network connectivity after applying policies
7. **Monitor denied traffic** - Enable Calico flow logs for visibility into blocked connections
8. **Use tiers** - Organize policies into security, platform, and application tiers