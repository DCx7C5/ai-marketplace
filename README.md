# 🛒 AI Marketplace

> A production-grade marketplace of **1,064 Claude skills** and **38 AI agents** — unified discovery, instant install, enterprise-ready.

[![Agents](https://img.shields.io/badge/agents-38-blue?style=flat-square)](agents/)
[![Skills](https://img.shields.io/badge/skills-1%2C064-green?style=flat-square)](skills/)
[![Status](https://img.shields.io/badge/status-production-success?style=flat-square)]()
[![License](https://img.shields.io/badge/license-MIT-purple?style=flat-square)](LICENSE)
[![CyberSecSuite](https://img.shields.io/badge/CyberSecSuite-v0.1-red?style=flat-square)](https://github.com/DCx7C5/cybersecsuite)

**Latest Release:** `marketplace-v1-ready` (2026-04-27)

---

## 📦 What's in here?

| Category | Count | Description |
|----------|-------|-------------|
| [**Agents**](agents/) | 38 | Claude Code sub-agents (31 templates + AgentFactory + 6 sub-agents) |
| [**Skills**](skills/) | 1,064 | AI skills organized by domain (security, cloud, forensics, etc.) |
| [**MCPs**](mcps/) | 6 | Model Context Protocol servers (csscore, canvas, memory, template, playwright, crypto) |
| [**Search Index**](search-index.json) | 1,064+ | Full-text searchable asset catalog |

---

## 🚀 Quick Install

### Clone the Production-Ready Marketplace

```bash
git clone https://github.com/DCx7C5/ai-marketplace.git
cd ai-marketplace
git checkout marketplace-v1-ready  # Production release
```

### Install an Agent

Copy a single agent file into your project's `.claude/agents/` directory:

```bash
# Example: install the cybersec-analyst agent
curl -sSL https://raw.githubusercontent.com/DCx7C5/ai-marketplace/main/agents/cybersec-analyst.md \
  -o .claude/agents/cybersec-analyst.md
```

Or symlink locally:

```bash
git clone https://github.com/DCx7C5/ai-marketplace.git ~/.ai-marketplace
mkdir -p .claude/agents
ln -s ~/.ai-marketplace/agents/* .claude/agents/
```

### Install Skills

```bash
# Example: install the deception/honeypot skill
mkdir -p .claude/skills/deception/honeypot
curl -sSL https://raw.githubusercontent.com/DCx7C5/ai-marketplace/main/skills/deception/honeypot/SKILL.md \
  -o .claude/skills/deception/honeypot/SKILL.md
```

### Install Everything (CyberSecSuite Full Bundle)

```bash
git clone https://github.com/DCx7C5/ai-marketplace.git ~/.ai-marketplace
cp -r ~/.ai-marketplace/agents/* .claude/agents/
cp -r ~/.ai-marketplace/skills/* .claude/skills/
```

### Search for Assets

Use the included search index for discovery:

```bash
# View available assets
cat search-index.json | jq '.[] | {name, type, category}' | head -20
```

---

## 🤖 Agents

Claude Code sub-agents are markdown files placed in `.claude/agents/`. Each agent has a focused domain and is invoked automatically by Claude Code when the task matches.

### Security & Forensics

| Agent | Description | Model |
|-------|-------------|-------|
| [`cybersec-analyst`](agents/cybersec-analyst.md) | CVE lookup, IOC analysis, MITRE ATT&CK mapping | sonnet |
| [`vuln-scanner`](agents/vuln-scanner.md) | Vulnerability scanning and assessment | sonnet |
| [`threat-modeler`](agents/threat-modeler.md) | STRIDE/PASTA threat modeling | sonnet |
| [`reverse-engineer`](agents/reverse-engineer.md) | Binary analysis, disassembly, decompilation | sonnet |
| [`firmware-analyst`](agents/firmware-analyst.md) | Firmware extraction and analysis | sonnet |
| [`kernel-analyst`](agents/kernel-analyst.md) | Kernel module and rootkit analysis | sonnet |
| [`memory-analyst`](agents/memory-analyst.md) | Memory forensics (Volatility) | sonnet |
| [`persistence-analyst`](agents/persistence-analyst.md) | Persistence mechanism detection | sonnet |
| [`certificate-analyst`](agents/certificate-analyst.md) | TLS/PKI certificate inspection | sonnet |
| [`steganography-analyst`](agents/steganography-analyst.md) | Steganography detection and extraction | sonnet |

### Network Specialists

| Agent | Description | Model |
|-------|-------------|-------|
| [`network-analyst`](agents/network-analyst.md) | Packet capture and network forensics | sonnet |
| [`layer2-specialist`](agents/layer2-specialist.md) | Layer 2 (Ethernet, ARP, STP) analysis | sonnet |
| [`layer3-specialist`](agents/layer3-specialist.md) | Layer 3 (IP, routing, ICMP) analysis | sonnet |
| [`layer4-specialist`](agents/layer4-specialist.md) | Layer 4 (TCP/UDP) analysis | sonnet |
| [`layer5-specialist`](agents/layer5-specialist.md) | Layer 5 (session) analysis | sonnet |
| [`layer6-specialist`](agents/layer6-specialist.md) | Layer 6 (presentation/encoding) analysis | sonnet |
| [`layer7-specialist`](agents/layer7-specialist.md) | Layer 7 (application protocol) analysis | sonnet |

### Development & Analysis

| Agent | Description | Model |
|-------|-------------|-------|
| [`python-developer`](agents/python-developer.md) | Python/FastAPI/Tortoise ORM/Pydantic v2 | sonnet |
| [`cpp-developer`](agents/cpp-developer.md) | C/C++ development and analysis | sonnet |
| [`code-reviewer`](agents/code-reviewer.md) | Security-focused code review | sonnet |
| [`command-verifier`](agents/command-verifier.md) | Shell command safety verification | sonnet |
| [`postgres-db-engineer`](agents/postgres-db-engineer.md) | PostgreSQL schema and query optimization | sonnet |
| [`logfile-analyst`](agents/logfile-analyst.md) | Log parsing and anomaly detection | sonnet |
| [`filesystem-analyst`](agents/filesystem-analyst.md) | Filesystem forensics and artifact recovery | sonnet |
| [`process-analyst`](agents/process-analyst.md) | Process tree and behavior analysis | sonnet |
| [`settings-analyst`](agents/settings-analyst.md) | Configuration file security review | sonnet |
| [`audiovideo-analyst`](agents/audiovideo-analyst.md) | Audio/video forensics and metadata | sonnet |

### UI/UX & Infrastructure

| Agent | Description | Model |
|-------|-------------|-------|
| [`frontend-design`](agents/frontend-design.md) | UI/UX design and component building | sonnet |
| [`senior-frontend`](agents/senior-frontend.md) | Senior-level frontend architecture | sonnet |
| [`token-optimizer`](agents/token-optimizer.md) | Token usage optimization | sonnet |
| [`watchdog`](agents/watchdog.md) | System monitoring and alerting | sonnet |

---

## 🧠 Skills

CyberSecSuite skills are modular capability modules placed in `.claude/skills/`. They follow a hierarchical taxonomy (`domain/subdomain/.../SKILL.md`).

### Available Skill Domains

| Domain | Skills | Description |
|--------|--------|-------------|
| [`deception/`](skills/deception/) | 4 | Honeypots, honeytokens, canary tokens, deception tech |
| [`mobile/`](skills/mobile/) | 12 | Android/iOS forensics, APK analysis, IPC, dynamic analysis |
| [`steganography/`](skills/steganography/) | 8 | LSB detection across PNG/JPG/BMP/GIF, audio steg, metadata |
| [`vulnerabilities/`](skills/vulnerabilities/) | 36+ | CVE analysis, exploit detection, patch management |

---

## 📁 Repository Structure

```
ai-marketplace/
├── agents/                    # Claude Code sub-agent definitions
│   ├── cybersec-analyst.md
│   ├── python-developer.md
│   └── ...
├── skills/                    # CyberSecSuite skill modules
│   ├── deception/
│   │   ├── SKILL.md
│   │   ├── honeypot/SKILL.md
│   │   ├── honeytoken/SKILL.md
│   │   └── canarytoken/SKILL.md
│   ├── mobile/
│   ├── steganography/
│   └── vulnerabilities/
├── docs/                      # Extended documentation
│   ├── AGENT_SCHEMA.md        # Agent YAML frontmatter spec
│   ├── SKILL_SCHEMA.md        # Skill YAML frontmatter spec
│   └── USAGE.md               # Detailed usage guide
├── scripts/                   # Helper scripts
│   └── install.sh             # One-liner installer
├── .github/
│   ├── workflows/
│   │   ├── validate.yml       # Validate agent/skill schemas
│   │   └── index.yml          # Auto-generate index.json
│   └── ISSUE_TEMPLATE/
│       ├── new-agent.md
│       └── new-skill.md
├── index.json                 # Machine-readable catalog
├── CONTRIBUTING.md
└── LICENSE
```

---

## 🤝 Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) to add your own agents or skills.

**TL;DR:**
1. Fork this repo
2. Add your agent to `agents/` or skill to `skills/`
3. Validate with `scripts/validate.sh`
4. Open a PR

---

## 📄 License

MIT — see [LICENSE](LICENSE)

---

## 🔗 Related Projects

- [CyberSecSuite](https://github.com/DCx7C5/cybersecsuite) — Full-stack forensics platform (v0.1)
- [Claude Code Docs](https://docs.anthropic.com/claude-code) — Anthropic Claude Code documentation

