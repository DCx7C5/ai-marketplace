# csscore-mcp Tools

**Generated:** Auto-extracted from source code

## Available Tools (64)

### cache_lookup

Deterministic exact-match cache lookup. Returns cached result if TTL is valid.

**Function:** `cache_lookup`

---

### cache_store

Store a tool call result in the exact-match cache.

**Function:** `cache_store`

---

### cache_analytics

Return cache hit/miss statistics and entry listing.

**Function:** `cache_analytics`

---

### cache_invalidate

Invalidate cache entries by key prefix, tag, or tool name.

**Function:** `cache_invalidate`

---

### get_health

Health check: uptime, circuit breakers, provider status, rate limits, cache.

**Function:** `get_health`

---

### get_provider_metrics

Per-provider latency (p50/p95/p99), success rate, usage, and circuit breaker state.

**Function:** `get_provider_metrics`

---

### get_session_snapshot

Full session snapshot: cost, tokens, recent requests, budget, circuit breakers.

**Function:** `get_session_snapshot`

---

### db_healthcheck

Check PostgreSQL/Tortoise health and optional table/intelligence counts.

**Function:** `db_healthcheck`

---

### bootstrap_intelligence

Bootstrap NVD/CVE, CWE, CAPEC, MITRE families and shared feeds into PostgreSQL.

**Function:** `bootstrap_intelligence`

---

### case_open

Open a new investigation case (Phase 0). Creates a CaseIntake record and sets session phase.

**Function:** `case_open`

---

### case_status

Get the status of the current or a specific case intake by ID.

**Function:** `case_status`

---

### add_finding

Add a new security finding to the scoped store (file + DB).

**Function:** `add_finding`

---

### add_ioc

Add or merge an IOC (indicator of compromise) into scoped memory and DB.

**Function:** `add_ioc`

---

### query_findings

Query security findings from the scoped store with optional severity/status filters.

**Function:** `query_findings`

---

### update_risk_register

Update a risk register entry with impact, likelihood, and mitigation details.

**Function:** `update_risk_register`

---

### query_pocs

Query PoC exploit records, optionally filtered by CVE ID, status, or weaponized flag.

**Function:** `query_pocs`

---

### add_poc

Add a new PoC exploit record linked to a CVE.

**Function:** `add_poc`

---

### suggest_mitre

Suggest MITRE ATT&CK techniques based on a description of observed behaviour.

**Function:** `suggest_mitre`

---

### get_project_memory

Return project memory: findings, recent entries and IOCs from the current scope.

**Function:** `get_project_memory`

---

### share_to_layers

Share a value to one or more scopes (project / session).

**Function:** `share_to_layers`

---

### get_layer_value

Read values from a scope layer (project / session).

**Function:** `get_layer_value`

---

### vault_scaffold

Scaffold a new CyberSecSuite forensic Obsidian vault. Creates wiki/, .raw/, memories/ directories and seed files. Idempotent.

**Function:** `vault_scaffold`

---

### vault_status

Return vault health summary: page count, canvas count, sources ingested, hot cache age.

**Function:** `vault_status`

---

### vault_ingest

Ingest a file or URL into the forensic vault. Delta-tracked — unchanged sources are skipped unless force=true.

**Function:** `vault_ingest`

---

### vault_query

Query the forensic vault for information. Reads hot cache first, then index, then relevant pages.

**Function:** `vault_query`

---

### vault_lint

Check vault health: orphan pages, missing indexes, stale hot cache.

**Function:** `vault_lint`

---

### session_snapshot

Return a full session state snapshot including scope, usage, budget, and circuit breakers.

**Function:** `session_snapshot`

---

### agent_registry

List all registered A2A agents with skills and metadata.

**Function:** `agent_registry`

---

### best_provider

Find the best provider/model for a task based on cost, capability, and circuit breaker state.

**Function:** `best_provider`

---

### proxy_chat

Route a chat completion through the AI proxy with multi-provider fallback.

**Function:** `proxy_chat`

---

### proxy_providers

List all configured AI providers with status and rate limits.

**Function:** `proxy_providers`

---

### proxy_models

List all available models across providers, optionally filtered by provider.

**Function:** `proxy_models`

---

### proxy_usage

Return AI proxy usage summary: tokens, costs, requests by provider.

**Function:** `proxy_usage`

---

### proxy_cost

Return detailed cost breakdown by provider.

**Function:** `proxy_cost`

---

### simulate_route

Dry-run route simulation — shows which provider/model would be selected without executing.

**Function:** `simulate_route`

---

### set_budget_guard

Set a spending budget guard for a combo or tier key.

**Function:** `set_budget_guard`

---

### get_circuit_breakers

Return circuit breaker status for all routing targets.

**Function:** `get_circuit_breakers`

---

### explain_route

Explain step-by-step why a specific provider/model would be chosen for a request.

**Function:** `explain_route`

---

### routing_strategies

List all available routing strategies with descriptions.

**Function:** `routing_strategies`

---

### tool_toggle_get

Get the current toggle state for a specific tool across all scopes.

**Function:** `tool_toggle_get`

---

### tool_toggle_list

List all tools that have explicit toggle states, with their active scope and enabled status.

**Function:** `tool_toggle_list`

---

### tool_toggle_clear

Remove all toggle state for a tool across all scopes (resets to default: enabled).

**Function:** `tool_toggle_clear`

---

### web_search

Web search via Perplexity/Serper/Brave/Tavily — title, URL, snippet. Engine auto-selected from available API keys.

**Function:** `web_search`

---

### structured_extract

Extract structured forensic data from text using a typed schema. Returns a validated JSON object.

**Function:** `structured_extract`

---

### structured_extract_stream

Stream structured extraction with incremental parsed snapshots (for large documents).

**Function:** `structured_extract_stream`

---

### skill_list

List available skills from the registry

**Function:** `skill_list`

---

### skill_search

Search skills by keyword

**Function:** `skill_search`

---

### skill_load

Load a skill by name

**Function:** `skill_load`

---

### check_quota

Check rate limit and budget quota for a provider or all providers.

**Function:** `check_quota`

---

### cost_report

Cost and usage report broken down by provider. Optional limit on recent records.

**Function:** `cost_report`

---

### list_models_catalog

List all available models with context window, cost, and availability.

**Function:** `list_models_catalog`

---

### list_tool_categories

List all CyberSecSuite tool categories with tool counts and representative names.

**Function:** `list_tool_categories`

---

### describe_tool

Get the full description and parameter schema for a specific tool by name.

**Function:** `describe_tool`

---

### thinking_stream

Stream a thinking-enabled response, surfacing reasoning blocks as they arrive.

**Function:** `thinking_stream`

---

### agent_env_create

Create an Anthropic agent environment (isolated execution context).

**Function:** `agent_env_create`

---

### agent_vault_create

Create an Anthropic vault for storing MCP server credentials.

**Function:** `agent_vault_create`

---

### agent_vault_add_credential

Store an MCP server credential (static bearer token) in an existing vault.

**Function:** `agent_vault_add_credential`

---

### agent_skill_upload

Upload a SKILL.md file to Anthropic as a custom agent skill.

**Function:** `agent_skill_upload`

---

### agent_remote_create

Create a remote Anthropic agent with tools, MCP servers, and skills.

**Function:** `agent_remote_create`

---

### agent_remote_add_skills

Add custom or Anthropic built-in skills to an existing remote agent (bumps version).

**Function:** `agent_remote_add_skills`

---

### agent_versions_list

List all versions of a remote Anthropic agent.

**Function:** `agent_versions_list`

---

### agent_session_create

Create a session for a remote agent pinned to a specific version.

**Function:** `agent_session_create`

---

### agent_session_run

Send a prompt to a remote agent session and stream/collect the response.

**Function:** `agent_session_run`

---

### agent_file_upload

Upload a file to Anthropic beta Files API for use as a session resource.

**Function:** `agent_file_upload`

---

