---
name: New Skill
about: Submit a new CyberSecSuite skill
title: "[Skill] domain/subdomain/action"
labels: ["skill", "new-content"]
assignees: []
---

## Skill Path

<!-- e.g., `skills/mobile/android/frida/hook/SKILL.md` -->

## Name

<!-- Derived from path: skip top-level domain, join rest with `-` -->
<!-- e.g., `android-frida-hook` -->

## Description

<!-- What this skill does and when to invoke it -->

## MITRE ATT&CK Techniques

<!-- e.g., T1059, T1059.001 -->

## NIST CSF Controls

<!-- e.g., DE.CM-01, RS.MA-01 -->

## Checklist

- [ ] File placed at correct hierarchical path under `skills/`
- [ ] YAML frontmatter complete (`name`, `description`, `domain`, `model`, `maxTurns`, `mitre_attack`, `nist_csf`)
- [ ] `name` follows path-derivation convention
- [ ] Skill body has meaningful content (not a placeholder)
- [ ] `scripts/validate.sh` passes locally

