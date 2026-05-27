---
name: net-dns-typosquatting
description: - Auditing project dependencies to identify packages whose names are suspiciously similar to popular libraries - Proactively scanning package registries for newly published packages that may be typosquats of your organization's packages - Investigating a suspected supply chain compromise where a developer installed a misspelled package name - Build
domain: cybersecurity
---
---|------------|
| **Typosquatting** | Registering a package name that closely resembles a popular package, exploiting common typos to trick developers into installing malicious code |
| **Levenshtein Distance** | The minimum number of single-character edits (insertions, deletions, substitutions) required to transform one string into another; the primary metric for measuring name similarity |
| **Dependency Confusion** | A broader supply chain attack where attackers publish malicious packages to public registries with names matching private internal packages, exploiting package manager resolution order |
| **PEP 503 Normalization** | The Python packaging specification that treats hyphens, underscores, and periods as equivalent in package names, meaning `my-package`, `my_package`, and `my.package` resolve to the same package |
| **QWERTY Distance** | A keyboard-layout-aware distance metric measuring how far apart two keys are on a standard keyboard, used to detect substitutions from adjacent key mistyping |
| **Combosquatting** | A variant of typosquatting where attackers prepend or append common words to a package name (e.g., `requests-security`, `python-requests`) |
| **StarJacking** | An attack where a typosquat package links its repository URL to the legitimate package's GitHub repository to inflate apparent credibility |

## Tools & Systems

- **PyPI JSON API**: REST API at `https://pypi.org/pypi/<package>/json` returning package metadata including name, author, versions, upload timestamps, and project URLs
- **npm Registry API**: REST API at `https://registry.npmjs.org/<package>` returning package metadata including maintainers, version history, creation timestamps, and distribution info
- **python-Levenshtein / rapidfuzz**: Python libraries for fast string distance computation, supporting Levenshtein, Damerau-Levenshtein, Jaro-Winkler, and other similarity metrics
- **pypistats.org API**: Provides download statistics for PyPI packages, enabling download count comparison between suspected typosquats and their targets
- **npm download counts API**: Endpoint at `https://api.npmjs.org/downloads/point/<period>/<package>` providing download statistics for npm packages

## Common Scenarios

### Scenario: Auditing a Python Project for Typosquatted Dependencies

**Context**: A security team discovers that a developer's workstation was compromised after installing a Python package. The incident response team needs to audit all project dependencies for potential typosquats and establish ongoing monitoring.

**Approach**:
1. Parse `requirements.txt` and `Pipfile.lock` to extract all 87 direct and transitive dependencies
2. Generate typosquat candidates for each dependency using character omission, transposition, substitution, and separator manipulation, producing approximately 2,400 candidate names
3. Query the PyPI JSON API for each candidate, finding 34 that actually exist as published packages
4. Score each existing candidate: 3 packages score above 70 (HIGH risk) with Levenshtein distance 1, created within the last 60 days, single version, and fewer than 100 downloads
5. Manual review confirms 2 of the 3 are malicious typosquats containing obfuscated code that exfiltrates environment variables during installation
6. Block the malicious packages in the organization's artifact proxy, report to PyPI for takedown via `security@pypi.org`, and add all 87 dependencies to the ongoing monitoring watchlist
7. Implement the detection agent as a scheduled CI job that runs weekly and alerts on new HIGH-risk findings

**Pitfalls**:
- Not normalizing PyPI package names per PEP 503 before comparison, causing missed matches between hyphenated and underscored variants
- Setting the Levenshtein distance threshold too low (only 1) and missing typosquats at distance 2 that use double substitutions
- Relying solely on name similarity without checking metadata signals, leading to high false positive rates on legitimately similar package names
- Not accounting for npm scoped packages (`@scope/name`) which have different naming rules than unscoped packages
- Querying the registries too aggressively and getting rate-limited or IP-blocked

## Output Format

```
## Typosquatting Detection Report

**Scan Date**: 2026-03-19
**Registry**: PyPI
**Packages Monitored**: 87
**Candidates Generated**: 2,412
**Candidates Found in Registry**: 34
**Flagged as Suspicious**: 5

### HIGH Risk (Score >= 70)

| Suspect Package | Target Package | Levenshtein | Created | Downloads | Score |
|----------------|---------------|-------------|---------|-----------|-------|
| reqeusts       | requests      | 1           | 2026-02-28 | 43     | 92    |
| requsets       | requests      | 1           | 2026-03-01 | 12     | 88    |
| numpyy         | numpy         | 1           | 2026-01-15 | 67     | 78    |

### Recommendation
- BLOCK: reqeusts, requsets, numpyy (add to artifact proxy deny-list)
- REPORT: Submit malware reports to security@pypi.org with package names and evidence
- MONITOR: Continue weekly scans for the full dependency watchlist
```