---
name: cloud-devsecops-aqua
description: Aqua Security provides Trivy, the world's most popular open-source universal security scanner, designed to find vulnerabilities, misconfigurations, secrets, SBOM data, and license issues in containers, Kubernetes, code repositories, and cloud environments. Trivy covers OS packages (Alpine, Debian, Ubuntu, RHEL, etc.) and language-specific dependenc
domain: cybersecurity
---
-----|-------------|--------|
| Images scanned per day | Total images passing through scanning pipeline | All production images |
| Critical CVE count | Open critical vulnerabilities across all images | 0 in production |
| Mean time to patch | Average days from CVE publication to patched image | < 7 days |
| SBOM coverage | Percentage of production images with generated SBOMs | 100% |
| Scan duration | Average time per image scan | < 2 minutes |

## References

- [Trivy Documentation](https://aquasecurity.github.io/trivy/)
- [Trivy GitHub Repository](https://github.com/aquasecurity/trivy)
- [Trivy Operator for Kubernetes](https://aquasecurity.github.io/trivy-operator/)
- [Aqua Security Platform](https://www.aquasec.com/products/)
- [CycloneDX SBOM Specification](https://cyclonedx.org/specification/overview/)