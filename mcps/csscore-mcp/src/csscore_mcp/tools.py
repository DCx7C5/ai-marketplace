"""Tools extracted from csmcp for csscore-mcp."""

from typing import Any, Dict

# === From cache.py ===
"""Exact-match context caching tools — SDK in-process MCP server module."""
from __future__ import annotations

import hashlib
import json
from datetime import datetime
from typing import Any

from csmcp._sdk_compat import tool
from csmcp.cybersec.helpers import JsonDict, sdk_result

_CACHE: dict[str, dict[str, Any]] = {}


def _cache_key(tool_name: str, params: dict[str, Any]) -> str:
    payload = json.dumps({"tool": tool_name, "params": params}, sort_keys=True, default=str)
    return hashlib.sha256(payload.encode()).hexdigest()


@tool(
    "cache_lookup",
    "Deterministic exact-match cache lookup. Returns cached result if TTL is valid.",
    {
        "tool_name": "string",
        "params": "object",
        "ttl_seconds": {"type": "integer", "default": 3600},
    },
)
async def cache_lookup(args: dict[str, Any]) -> JsonDict:
    key = _cache_key(args["tool_name"], args.get("params", {}))
    entry = _CACHE.get(key)
    if entry is None:
        return sdk_result({"status": "miss", "key": key})

    import time
    ttl = args.get("ttl_seconds", 3600)
    age = time.time() - entry["stored_at"]
    if age > ttl:
        del _CACHE[key]
        return sdk_result({"status": "expired", "key": key, "age_seconds": int(age)})

    return sdk_result({"status": "hit", "key": key, "result": entry["result"], "age_seconds": int(age)})


@tool(
    "cache_store",
    "Store a tool call result in the exact-match cache.",
    {
        "tool_name": "string",
        "params": "object",
        "result": "object",
        "tags": {"type": "array", "items": {"type": "string"}, "default": []},
    },
)
async def cache_store(args: dict[str, Any]) -> JsonDict:
    import time
    key = _cache_key(args["tool_name"], args.get("params", {}))
    _CACHE[key] = {
        "tool_name": args["tool_name"],
        "params": args.get("params", {}),
        "result": args["result"],
        "tags": args.get("tags", []),
        "stored_at": time.time(),
        "stored_iso": datetime.now().isoformat(),
    }
    return sdk_result({"status": "stored", "key": key, "cache_size": len(_CACHE)})


@tool(
    "cache_analytics",
    "Return cache hit/miss statistics and entry listing.",
    {"limit": {"type": "integer", "default": 20}},
)
async def cache_analytics(args: dict[str, Any]) -> JsonDict:
    import time
    limit = min(int(args.get("limit", 20)), 200)
    now = time.time()
    entries = [
        {
            "key": k[:16] + "...",
            "tool_name": v["tool_name"],
            "stored_iso": v.get("stored_iso"),
            "age_seconds": int(now - v["stored_at"]),
            "tags": v.get("tags", []),
        }
        for k, v in list(_CACHE.items())[:limit]
    ]
    return sdk_result({"status": "success", "total_entries": len(_CACHE), "entries": entries})


@tool(
    "cache_invalidate",
    "Invalidate cache entries by key prefix, tag, or tool name.",
    {
        "tool_name": {"type": "string", "nullable": True},
        "tag": {"type": "string", "nullable": True},
        "key_prefix": {"type": "string", "nullable": True},
    },
)
async def cache_invalidate(args: dict[str, Any]) -> JsonDict:
    tool_name = args.get("tool_name")
    tag = args.get("tag")
    key_prefix = args.get("key_prefix")
    removed = 0

    keys_to_remove = []
    for k, v in _CACHE.items():
        if tool_name and v["tool_name"] == tool_name:
            keys_to_remove.append(k)
        elif tag and tag in v.get("tags", []):
            keys_to_remove.append(k)
        elif key_prefix and k.startswith(key_prefix):
            keys_to_remove.append(k)

    for k in keys_to_remove:
        del _CACHE[k]
        removed += 1

    return sdk_result({"status": "success", "removed": removed, "remaining": len(_CACHE)})


ALL_TOOLS = [cache_lookup, cache_store, cache_analytics, cache_invalidate]


# === From health.py ===
"""Health and metrics tools — SDK in-process MCP server module."""
from __future__ import annotations

import os
import time
from typing import Any

from csmcp._sdk_compat import tool
from csmcp.cybersec.helpers import JsonDict, sdk_result, sdk_error

_START_TIME = time.time()


@tool("get_health", "Health check: uptime, circuit breakers, provider status, rate limits, cache.", {})
async def get_health(args: dict[str, Any]) -> JsonDict:
    try:
        from ai_proxy.providers.registry import get_all_providers
        from ai_proxy.routing.combo import get_circuit_breaker_status
        from ai_proxy.services.rate_limiter import rate_limiter
        from ai_proxy.services.usage_tracker import usage_tracker
    except ImportError:
        return sdk_error("ai_proxy not available")

    providers = get_all_providers()
    cb_status = get_circuit_breaker_status()
    open_cbs = [cb for cb in cb_status if cb["state"] == "open"]
    summary = usage_tracker.get_summary()

    services: dict[str, str] = {"ai_proxy": "healthy", "rate_limiter": "healthy"}
    try:
        from db.main import is_initialized
        services["database"] = "healthy" if is_initialized() else "degraded"
    except Exception:
        services["database"] = "unknown"

    return sdk_result({
        "status": "healthy" if not open_cbs else "degraded",
        "uptime_seconds": round(time.time() - _START_TIME),
        "version": os.environ.get("APP_VERSION", "0.1.0"),
        "providers_total": len(providers),
        "providers_available": sum(1 for p in providers.values() if p.is_available),
        "circuit_breakers": {
            "total": len(cb_status),
            "open": len(open_cbs),
            "closed": len(cb_status) - len(open_cbs),
            "open_targets": [cb["target"] for cb in open_cbs],
        },
        "usage": {
            "total_requests": summary["total_requests"],
            "total_errors": summary["total_errors"],
            "total_cost_usd": summary["total_cost_usd"],
        },
        "rate_limits": {
            p_id: rate_limiter.get_status(p_id) for p_id in providers
        },
        "services": services,
    })


@tool(
    "get_provider_metrics",
    "Per-provider latency (p50/p95/p99), success rate, usage, and circuit breaker state.",
    {"provider": {"type": "string", "nullable": True}},
)
async def get_provider_metrics(args: dict[str, Any]) -> JsonDict:
    try:
        from ai_proxy.providers.registry import get_all_providers
        from ai_proxy.routing.combo import get_circuit_breaker_status, get_usage_counts
        from ai_proxy.services.usage_tracker import usage_tracker
        from ai_proxy.services.rate_limiter import rate_limiter
    except ImportError:
        return sdk_error("ai_proxy not available")

    filter_provider = args.get("provider")
    providers = get_all_providers()
    if filter_provider and filter_provider not in providers:
        return sdk_error(f"Provider '{filter_provider}' not found")

    cb_status = get_circuit_breaker_status()
    cb_open_targets = {cb["target"] for cb in cb_status if cb["state"] == "open"}
    usage_counts = get_usage_counts()
    summary = usage_tracker.get_summary()
    by_provider = summary["by_provider"]

    metrics: dict[str, Any] = {}
    for p_id, p in providers.items():
        if filter_provider and p_id != filter_provider:
            continue
        p_usage = by_provider.get(p_id, {"tokens": 0, "cost_usd": 0.0, "requests": 0, "errors": 0})
        req_count = p_usage["requests"]
        err_count = p_usage["errors"]
        metrics[p_id] = {
            "available": p.is_available,
            "is_free": p.is_free,
            "requests_total": req_count,
            "errors_total": err_count,
            "success_rate": round((req_count - err_count) / req_count, 4) if req_count else None,
            "tokens_total": p_usage["tokens"],
            "cost_total_usd": p_usage["cost_usd"],
            "usage_count": usage_counts.get(p_id, 0),
            "circuit_breaker_open_targets": [t for t in cb_open_targets if t.startswith(f"{p_id}:")],
            "rate_limit_status": rate_limiter.get_status(p_id),
        }

    if filter_provider:
        return sdk_result({"status": "success", "provider": filter_provider, "metrics": metrics[filter_provider]})
    return sdk_result({"status": "success", "providers": metrics})


@tool("get_session_snapshot", "Full session snapshot: cost, tokens, recent requests, budget, circuit breakers.", {})
async def get_session_snapshot(args: dict[str, Any]) -> JsonDict:
    try:
        from ai_proxy.services.usage_tracker import usage_tracker
        from ai_proxy.routing.combo import get_circuit_breaker_status, budget_guard
    except ImportError:
        return sdk_error("ai_proxy not available")

    summary = usage_tracker.get_summary()
    recent = usage_tracker.get_recent(limit=10)
    cb_status = get_circuit_breaker_status()
    open_cbs = [cb for cb in cb_status if cb["state"] == "open"]

    return sdk_result({
        "status": "success",
        "uptime_seconds": round(time.time() - _START_TIME),
        "usage": summary,
        "recent_requests": recent,
        "circuit_breakers": {
            "open": len(open_cbs),
            "total": len(cb_status),
            "open_targets": [cb["target"] for cb in open_cbs],
        },
        "budgets": budget_guard.get_all(),
    })


ALL_TOOLS = [get_health, get_provider_metrics, get_session_snapshot]


# === From db.py ===
"""Database health and bootstrap tools — SDK in-process MCP server module."""
from __future__ import annotations

from typing import Any

from csmcp._sdk_compat import tool
from csmcp.cybersec.helpers import JsonDict, sdk_result, sdk_error


@tool(
    "db_healthcheck",
    "Check PostgreSQL/Tortoise health and optional table/intelligence counts.",
    {
        "check_connection": {"type": "boolean", "default": True},
        "create_db": {"type": "boolean", "default": False},
        "bootstrap_intel": {"type": "boolean", "default": False},
        "include_counts": {"type": "boolean", "default": True},
    },
)
async def db_healthcheck(args: dict[str, Any]) -> JsonDict:
    try:
        from db.bootstrap import get_database_health_async
    except ImportError:
        return sdk_error("db.bootstrap not available — ensure src/ is in PYTHONPATH")

    health = await get_database_health_async(
        create_db=args.get("create_db", False),
        bootstrap_intel=args.get("bootstrap_intel", False),
        include_counts=args.get("include_counts", True),
        check_connection=args.get("check_connection", True),
    )
    return sdk_result(health)


@tool(
    "bootstrap_intelligence",
    "Bootstrap NVD/CVE, CWE, CAPEC, MITRE families and shared feeds into PostgreSQL.",
    {
        "force": {"type": "boolean", "default": False},
        "include_feeds": {"type": "boolean", "default": True},
        "create_db": {"type": "boolean", "default": True},
    },
)
async def bootstrap_intelligence(args: dict[str, Any]) -> JsonDict:
    try:
        from db.bootstrap import (
            init_tortoise_async,
            get_database_health_async,
            bootstrap_intelligence_async,
        )
    except ImportError:
        return sdk_error("db.bootstrap not available — ensure src/ is in PYTHONPATH")

    await init_tortoise_async(create_db=args.get("create_db", True), bootstrap_intel=False)
    summary = await bootstrap_intelligence_async(
        force=args.get("force", False),
        include_feeds=args.get("include_feeds", True),
    )
    health = await get_database_health_async(
        create_db=False, bootstrap_intel=False, include_counts=True, check_connection=True,
    )
    return sdk_result({"status": "success", "bootstrap": summary, "health": health})


ALL_TOOLS = [db_healthcheck, bootstrap_intelligence]


# === From cases.py ===
"""Investigation case tools — SDK in-process MCP server module."""
from __future__ import annotations

from typing import Any

from csmcp._sdk_compat import tool
from csmcp.cybersec.helpers import JsonDict, _get_current_scope, sdk_result, sdk_error


@tool(
    "case_open",
    "Open a new investigation case (Phase 0). Creates a CaseIntake record and sets session phase.",
    {
        "title": "string",
        "problem_statement": "string",
        "attack_hypothesis": {"type": "string", "default": ""},
        "known_facts": {"type": "array", "items": {"type": "string"}, "default": []},
        "suspected_iocs": {"type": "array", "items": {"type": "string"}, "default": []},
        "affected_assets": {"type": "array", "items": {"type": "string"}, "default": []},
        "timeline_hints": {"type": "array", "items": {"type": "string"}, "default": []},
        "scope_in": {"type": "array", "items": {"type": "string"}, "default": []},
        "scope_out": {"type": "array", "items": {"type": "string"}, "default": []},
        "priority": {"type": "string", "enum": ["low", "medium", "high", "critical"], "default": "medium"},
        "mode": {"type": "string", "enum": ["blue", "red", "purple"], "default": "blue"},
        "mitre_hypotheses": {"type": "array", "items": {"type": "string"}, "default": []},
        "data_sources": {"type": "array", "items": {"type": "string"}, "default": []},
        "tags": {"type": "array", "items": {"type": "string"}, "default": []},
        "analyst_notes": {"type": "string", "default": ""},
    },
)
async def case_open(args: dict[str, Any]) -> JsonDict:
    try:
        from db.bootstrap import init_tortoise_async
        await init_tortoise_async()
        from db.models.case_intake import CaseIntake
        from db.models.scope import Session, Project
        from db.models.layers import SessionLayer
    except ImportError as exc:
        return sdk_error(f"db models not available: {exc}")

    scope = _get_current_scope()
    title = args["title"]
    problem_statement = args["problem_statement"]
    attack_hypothesis = args.get("attack_hypothesis", "")
    known_facts = args.get("known_facts", [])
    suspected_iocs = args.get("suspected_iocs", [])
    affected_assets = args.get("affected_assets", [])
    timeline_hints = args.get("timeline_hints", [])
    scope_in = args.get("scope_in", [])
    scope_out = args.get("scope_out", [])
    priority = args.get("priority", "medium")
    mode = args.get("mode", "blue")
    mitre_hypotheses = args.get("mitre_hypotheses", [])
    data_sources = args.get("data_sources", [])
    tags = args.get("tags", [])
    analyst_notes = args.get("analyst_notes", "")

    try:
        proj = None
        if scope.get("project"):
            proj, _ = await Project.get_or_create(name=scope["project"])
        sess = None
        if scope.get("session"):
            sess = await Session.get_or_none(session_id=scope["session"])
            if sess:
                sess.phase = "case_opening"
                sess.mode = mode
                await sess.save()

        intake = await CaseIntake.create(
            project=proj, session=sess,
            title=title, problem_statement=problem_statement, attack_hypothesis=attack_hypothesis,
            known_facts=known_facts, suspected_iocs=suspected_iocs, affected_assets=affected_assets,
            timeline_hints=timeline_hints, scope_in=scope_in, scope_out=scope_out,
            priority=priority, mode=mode, mitre_hypotheses=mitre_hypotheses,
            data_sources=data_sources, tags=tags, analyst_notes=analyst_notes,
        )

        if sess:
            layer, _ = await SessionLayer.get_or_create(
                session=sess, defaults={"name": f"phase0-{sess.session_id}"},
            )
            layer.active_phase = "case_opening"
            layer.current_hypotheses = mitre_hypotheses
            layer.investigation_focus = affected_assets
            layer.analysis_notes = (
                f"Case: {title}\nHypothesis: {attack_hypothesis}\n"
                f"Facts: {'; '.join(known_facts)}"
            )
            await layer.save()

        return sdk_result({
            "status": "success", "case_id": intake.id, "title": title,
            "priority": priority, "mode": mode, "phase": "case_opening",
            "facts_count": len(known_facts), "iocs_count": len(suspected_iocs),
            "assets_count": len(affected_assets), "mitre_count": len(mitre_hypotheses),
            "message": f"Case '{title}' opened. Ready for Phase 1 (Recon).",
        })
    except Exception as exc:
        return sdk_error(str(exc))


@tool(
    "case_status",
    "Get the status of the current or a specific case intake by ID.",
    {"case_id": {"type": "integer", "nullable": True}},
)
async def case_status(args: dict[str, Any]) -> JsonDict:
    try:
        from db.bootstrap import init_tortoise_async
        await init_tortoise_async()
        from db.models.case_intake import CaseIntake
    except ImportError as exc:
        return sdk_error(f"db models not available: {exc}")

    try:
        case_id = args.get("case_id")
        if case_id:
            intake = await CaseIntake.get_or_none(id=case_id)
        else:
            intake = await CaseIntake.all().order_by("-created_at").first()

        if not intake:
            return sdk_error("No case found")

        return sdk_result({
            "status": "success",
            "case": {
                "id": intake.id, "title": intake.title,
                "problem": intake.problem_statement,
                "hypothesis": intake.attack_hypothesis,
                "priority": intake.priority.value if hasattr(intake.priority, "value") else intake.priority,
                "mode": intake.mode.value if hasattr(intake.mode, "value") else intake.mode,
                "known_facts": intake.known_facts, "suspected_iocs": intake.suspected_iocs,
                "affected_assets": intake.affected_assets, "timeline_hints": intake.timeline_hints,
                "scope_in": intake.scope_in, "scope_out": intake.scope_out,
                "mitre_hypotheses": intake.mitre_hypotheses, "data_sources": intake.data_sources,
                "tags": intake.tags, "opened_by": intake.opened_by,
                "created_at": intake.created_at.isoformat() if intake.created_at else None,
                "closed_at": intake.closed_at.isoformat() if intake.closed_at else None,
            },
        })
    except Exception as exc:
        return sdk_error(str(exc))


ALL_TOOLS = [case_open, case_status]


# === From findings.py ===
"""Findings and IOC tools — SDK in-process MCP server module."""
from __future__ import annotations

from datetime import datetime
from typing import Any

from csmcp._sdk_compat import tool
from csmcp.cybersec.helpers import (
    JsonDict, _get_current_scope, _coerce_limit, get_project_dir, get_session_dir,
    sdk_result, sdk_error,
)


@tool(
    "add_finding",
    "Add a new security finding to the scoped store (file + DB).",
    {
        "title": "string",
        "description": {"type": "string", "default": ""},
        "severity": {"type": "string", "enum": ["low", "medium", "high", "critical"], "default": "medium"},
        "location": {"type": "string", "default": ""},
        "status": {"type": "string", "enum": ["open", "investigating", "confirmed", "false_positive", "resolved", "accepted_risk"], "default": "open"},
        "confidence": {"type": "string", "enum": ["low", "medium", "high", "confirmed"], "default": "medium"},
        "tags": {"type": "array", "items": {"type": "string"}, "default": []},
    },
)
async def add_finding(args: dict[str, Any]) -> JsonDict:
    try:
        from hooks.database import write_scoped_entry_async
    except ImportError:
        write_scoped_entry_async = None

    title = args["title"]
    description = args.get("description", "")
    severity = args.get("severity", "medium")
    location = args.get("location", "")
    status = args.get("status", "open")
    confidence = args.get("confidence", "medium")
    tags = args.get("tags", [])

    scope = _get_current_scope()
    timestamp = datetime.now().isoformat()
    entry = (
        f"### {timestamp} — {title}\n"
        f"**Severity:** {severity.upper()}\n"
        f"**Status:** {status}\n"
        f"**Location:** {location or 'N/A'}\n\n"
        f"{description}\n\n---\n\n"
    )

    project_dir = get_project_dir(scope)
    session_dir = get_session_dir(scope)

    project_dir.mkdir(parents=True, exist_ok=True)
    if session_dir:
        session_dir.mkdir(parents=True, exist_ok=True)
        with (session_dir / f"{severity}.md").open("a", encoding="utf-8") as f:
            f.write(entry)

    with (project_dir / "findings.md").open("a", encoding="utf-8") as f:
        f.write(entry)

    data: JsonDict = {
        "title": title, "description": description, "severity": severity,
        "location": location, "status": status, "confidence": confidence,
        "tags": tags, "timestamp": timestamp,
    }
    if write_scoped_entry_async:
        await write_scoped_entry_async(
            project_name=scope["project"],
            session_id=scope["session"], value_type="finding", data=data,
        )

    return sdk_result({
        "status": "success",
        "message": f"Added {severity} finding: {title}",
        "scope": scope,
    })


@tool(
    "add_ioc",
    "Add or merge an IOC (indicator of compromise) into scoped memory and DB.",
    {
        "value": "string",
        "ioc_type": {"type": "string", "default": "unknown"},
        "confidence": {"type": "string", "enum": ["low", "medium", "high", "confirmed"], "default": "low"},
        "status": {"type": "string", "enum": ["active", "cleared", "watchlist", "expired"], "default": "active"},
        "source": {"type": "string", "default": ""},
        "context": {"type": "object", "default": {}},
        "tags": {"type": "array", "items": {"type": "string"}, "default": []},
    },
)
async def add_ioc(args: dict[str, Any]) -> JsonDict:
    value = args.get("value", "")
    if not value.strip():
        return sdk_error("IOC value is required")

    try:
        from hooks.database import write_scoped_entry_async
    except ImportError:
        write_scoped_entry_async = None

    scope = _get_current_scope()
    ioc_data: JsonDict = {
        "ioc_type": args.get("ioc_type", "unknown"),
        "value": value.strip(),
        "confidence": args.get("confidence", "low"),
        "status": args.get("status", "active"),
        "source": args.get("source", ""),
        "context": args.get("context", {}),
        "tags": args.get("tags", []),
        "timestamp": datetime.now().isoformat(),
    }
    if write_scoped_entry_async:
        await write_scoped_entry_async(
            project_name=scope["project"],
            session_id=scope["session"], value_type="ioc", data=ioc_data,
        )

    return sdk_result({"status": "success", "ioc": ioc_data, "scope": scope})


@tool(
    "query_findings",
    "Query security findings from the scoped store with optional severity/status filters.",
    {
        "severity": {"type": "string", "enum": ["low", "medium", "high", "critical"], "nullable": True},
        "status": {"type": "string", "enum": ["open", "investigating", "confirmed", "false_positive", "resolved", "accepted_risk"], "nullable": True},
        "limit": {"type": "integer", "default": 10},
    },
)
async def query_findings(args: dict[str, Any]) -> JsonDict:
    try:
        from hooks.database import query_findings_db_async, ScopeContext
    except ImportError:
        return sdk_error("hooks.database not available")

    scope = _get_current_scope()
    sc = ScopeContext(
        project_name=scope["project"],
        session_id=scope["session"],
    )
    findings = await query_findings_db_async(
        scope=sc,
        severity=args.get("severity"),
        status=args.get("status"),
        limit=_coerce_limit(args.get("limit", 10), 10),
    )
    return sdk_result({"status": "success", "findings": findings, "count": len(findings)})


@tool(
    "update_risk_register",
    "Update a risk register entry with impact, likelihood, and mitigation details.",
    {
        "risk_id": "string",
        "impact": {"type": "string", "nullable": True},
        "likelihood": {"type": "string", "nullable": True},
        "mitigation": {"type": "string", "nullable": True},
    },
)
async def update_risk_register(args: dict[str, Any]) -> JsonDict:
    try:
        from hooks.database import write_scoped_entry_async
    except ImportError:
        write_scoped_entry_async = None

    scope = _get_current_scope()
    risk_data: JsonDict = {"risk_id": args["risk_id"]}
    for field in ("impact", "likelihood", "mitigation"):
        if args.get(field) is not None:
            risk_data[field] = args[field]

    if write_scoped_entry_async:
        await write_scoped_entry_async(
            project_name=scope["project"],
            session_id=scope["session"], value_type="risk", data=risk_data,
        )

    return sdk_result({"status": "success", "message": f"Updated risk {args['risk_id']}", "data": risk_data})


ALL_TOOLS = [add_finding, add_ioc, query_findings, update_risk_register]


# === From poc.py ===
"""PoC (Proof of Concept) MCP tools."""
from __future__ import annotations

from typing import Any

from csmcp._sdk_compat import tool
from csmcp.cybersec.helpers import JsonDict, sdk_result, sdk_error


@tool(
    "query_pocs",
    "Query PoC exploit records, optionally filtered by CVE ID, status, or weaponized flag.",
    {
        "cve_id": {"type": "string", "description": "Filter by CVE ID (e.g. CVE-2021-44228). Optional."},
        "status": {"type": "string", "description": "Filter by status: unverified|verified|weaponized|patched|disputed. Optional."},
        "weaponized_only": {"type": "boolean", "description": "If true, return only weaponized PoCs. Optional."},
        "limit": {"type": "integer", "description": "Max results (default 20, max 100)."},
    },
)
async def query_pocs(args: dict[str, Any]) -> JsonDict:
    try:
        from db.models.poc import ProofOfConcept
    except ImportError:
        return sdk_error("db.models.poc not available — ensure src/ is in PYTHONPATH")

    cve_id = args.get("cve_id", "").strip()
    status = args.get("status", "").strip()
    weaponized = args.get("weaponized_only", False)
    limit = min(int(args.get("limit", 20)), 100)

    qs = ProofOfConcept.all().prefetch_related("cve")
    if cve_id:
        qs = qs.filter(cve__cve_id=cve_id)
    if status:
        qs = qs.filter(status=status)
    if weaponized:
        qs = qs.filter(is_weaponized=True)

    pocs = await qs.limit(limit)
    return sdk_result({
        "count": len(pocs),
        "pocs": [
            {
                "id": p.id,
                "title": p.title,
                "cve_id": p.cve.cve_id if p.cve_id and p.cve else None,
                "status": p.status,
                "severity": p.severity,
                "poc_url": p.poc_url,
                "source": p.source,
                "language": p.language,
                "is_weaponized": p.is_weaponized,
                "reliability_score": p.reliability_score,
                "requires_auth": p.requires_auth,
                "tags": p.tags,
            }
            for p in pocs
        ],
    })


@tool(
    "add_poc",
    "Add a new PoC exploit record linked to a CVE.",
    {
        "cve_id": {"type": "string", "description": "CVE ID to link (e.g. CVE-2021-44228)."},
        "title": {"type": "string", "description": "PoC title."},
        "poc_url": {"type": "string", "description": "URL to the PoC/exploit."},
        "source": {"type": "string", "description": "Source (GitHub, ExploitDB, PacketStorm, …)."},
        "language": {"type": "string", "description": "Primary programming language."},
        "status": {"type": "string", "description": "unverified|verified|weaponized|patched|disputed."},
        "is_weaponized": {"type": "boolean", "description": "True if actively weaponized."},
        "description": {"type": "string", "description": "Detailed description."},
        "tags": {"type": "array", "items": {"type": "string"}, "description": "Tags."},
    },
)
async def add_poc(args: dict[str, Any]) -> JsonDict:
    try:
        from db.models.poc import ProofOfConcept
        from db.models.cve import CVEIntel
        from db.models.enums import PocStatus
    except ImportError:
        return sdk_error("db.models.poc not available — ensure src/ is in PYTHONPATH")

    cve_id = args.get("cve_id", "").strip()
    cve = await CVEIntel.filter(cve_id=cve_id).first() if cve_id else None

    poc = await ProofOfConcept.create(
        cve=cve,
        title=args.get("title", ""),
        poc_url=args.get("poc_url", ""),
        source=args.get("source", ""),
        language=args.get("language", ""),
        status=PocStatus(args.get("status", "unverified")),
        is_weaponized=bool(args.get("is_weaponized", False)),
        description=args.get("description", ""),
        tags=args.get("tags", []),
    )
    return sdk_result({"id": poc.id, "title": poc.title, "status": poc.status})


ALL_TOOLS = [query_pocs, add_poc]


# === From intelligence.py ===
"""MITRE suggestion and project memory tools — SDK in-process MCP server module."""
from __future__ import annotations

from typing import Any

from csmcp._sdk_compat import tool
from csmcp.cybersec.helpers import (
    JsonDict, _get_current_scope, get_project_dir,
    get_session_dir, sdk_result, sdk_error,
)


_KEYWORDS_TO_MITRE: dict[str, list[str]] = {
    "screenshot": ["T1113 - Screen Capture"],
    "keylog": ["T1056.001 - Keylogging"],
    "browser": ["T1555.003 - Web Browsers", "T1539 - Steal Web Session Cookie"],
    "cookie": ["T1539 - Steal Web Session Cookie"],
    "arp": ["T1557.002 - ARP Cache Poisoning"],
    "network": ["T1040 - Network Sniffing", "T1557 - Man-in-the-Middle"],
    "persistence": ["T1547 - Boot or Logon Autostart Execution"],
    "log": ["T1070.002 - Clear Windows Event Logs", "T1562.002 - Disable Windows Event Logging"],
    "injection": ["T1055 - Process Injection"],
    "c2": ["T1071 - Application Layer Protocol", "T1573 - Encrypted Channel"],
    "scheduled task": ["T1053.005 - Scheduled Task", "T1053 - Scheduled Task/Job"],
    "download": ["T1105 - Ingress Tool Transfer", "T1071.001 - Web Protocols"],
    "payload": ["T1105 - Ingress Tool Transfer", "T1204 - User Execution"],
    "task": ["T1053.005 - Scheduled Task", "T1053 - Scheduled Task/Job"],
    "cron": ["T1053.003 - Cron", "T1053 - Scheduled Task/Job"],
}


@tool(
    "suggest_mitre",
    "Suggest MITRE ATT&CK techniques based on a description of observed behaviour.",
    {
        "description": "string",
        "category": {"type": "string", "default": ""},
    },
)
def suggest_mitre(args: dict[str, Any]) -> JsonDict:
    description = args.get("description", "")
    category = args.get("category", "")
    suggestions: list[str] = []
    matched: list[str] = []
    seen: set[str] = set()
    desc_lower = description.lower()

    for keyword, techniques in _KEYWORDS_TO_MITRE.items():
        if keyword in desc_lower:
            matched.append(keyword)
            for t in techniques:
                if t not in seen:
                    seen.add(t)
                    suggestions.append(t)

    return sdk_result({
        "status": "success",
        "description": description,
        "suggested_techniques": suggestions,
        "matched_keywords": matched,
        "category": category,
    })


@tool(
    "get_project_memory",
    "Return project memory: findings, recent entries and IOCs from the current scope.",
    {"query": {"type": "string", "default": ""}},
)
async def get_project_memory(args: dict[str, Any]) -> JsonDict:
    try:
        from hooks.database import get_recent_entries_async, get_scoped_entries_async, ScopeContext
    except ImportError:
        return sdk_error("hooks.database not available")

    scope = _get_current_scope()
    session_dir = get_session_dir(scope)
    findings_file = get_project_dir(scope) / "findings.md"

    memory_data: JsonDict = {
        "findings": findings_file.read_text(encoding="utf-8") if findings_file.exists() else "",
        "scope": scope,
        "project_dir": str(get_project_dir(scope)),
        "session_dir": str(session_dir) if session_dir else None,
    }

    sc = ScopeContext(
        project_name=scope["project"],
        session_id=scope["session"],
    )
    memory_data["recent_entries"] = await get_recent_entries_async(sc, limit=20)
    memory_data["recent_iocs"] = await get_scoped_entries_async(
        project_name=scope["project"],
        session_id=scope["session"], value_type="ioc", limit=10,
    )

    return sdk_result({"status": "success", "memory": memory_data, "query": args.get("query", "")})


ALL_TOOLS = [suggest_mitre, get_project_memory]


# === From layers.py ===
"""Scope layer share/read tools — SDK in-process MCP server module."""
from __future__ import annotations

from typing import Any

from csmcp._sdk_compat import tool
from csmcp.cybersec.helpers import (
    JsonDict, _get_current_scope, _normalize_target_scopes, _normalize_scope_level,
    _coerce_limit, sdk_result, sdk_error,
)


@tool(
    "share_to_layers",
    "Share a value to one or more scopes (project / session).",
    {
        "value_type": "string",
        "data": "object",
        "target_scopes": {"type": "array", "items": {"type": "string"}, "nullable": True},
    },
)
async def share_to_layers(args: dict[str, Any]) -> JsonDict:
    try:
        from hooks.database import write_scoped_entry_async
    except ImportError:
        return sdk_error("hooks.database not available")

    scope = _get_current_scope()
    value_type = args["value_type"]
    data = args["data"]
    scopes = _normalize_target_scopes(args.get("target_scopes"))
    results: dict[str, JsonDict] = {}

    if "project" in scopes:
        if scope["project"]:
            try:
                results["project"] = await write_scoped_entry_async(
                    project_name=scope["project"],
                    session_id=None, value_type=value_type, data=data,
                )
            except Exception as e:
                results["project"] = {"status": "error", "message": str(e)}
        else:
            results["project"] = {"status": "skipped", "message": "Project scope not available"}

    if "session" in scopes:
        if scope["session"]:
            try:
                results["session"] = await write_scoped_entry_async(
                    project_name=scope["project"],
                    session_id=scope["session"], value_type=value_type, data=data,
                )
            except Exception as e:
                results["session"] = {"status": "error", "message": str(e)}
        else:
            results["session"] = {"status": "skipped", "message": "Session scope not available"}

    success_count = sum(1 for r in results.values() if r.get("status") == "success")
    return sdk_result({
        "status": "success",
        "message": f"Shared {value_type} to {success_count} scopes",
        "details": results,
        "scope": scope,
    })


@tool(
    "get_layer_value",
    "Read values from a scope layer (project / session).",
    {
        "value_type": "string",
        "scope": {"type": "string", "enum": ["project", "session"], "default": "project"},
        "limit": {"type": "integer", "default": 100},
    },
)
async def get_layer_value(args: dict[str, Any]) -> JsonDict:
    try:
        from hooks.database import get_scoped_entries_async, ScopeContext
    except ImportError:
        return sdk_error("hooks.database not available")

    current_scope = _get_current_scope()
    scope_level = _normalize_scope_level(args.get("scope", "project"), "project")

    sc = ScopeContext(
        project_name=current_scope["project"] if scope_level in ("project", "session") else None,
        session_id=current_scope["session"] if scope_level == "session" else None,
    )
    data = await get_scoped_entries_async(
        project_name=sc.project_name,
        session_id=sc.session_id, value_type=args["value_type"],
        limit=_coerce_limit(args.get("limit", 100), 100),
    )
    return sdk_result({
        "status": "success", "scope_level": scope_level, "scope": current_scope,
        "data": data, "count": len(data),
    })


ALL_TOOLS = [share_to_layers, get_layer_value]


# === From vault_tool.py ===
"""
Vault MCP tools — scaffold, ingest, query, lint, status.

These tools expose the VaultManager via the CyberSecSuite MCP server.
The vault path defaults to CYBERSEC_VAULT_PATH env var, or ./data/vault.
"""
from __future__ import annotations

import os
from typing import Any

from csmcp._sdk_compat import tool
from csmcp.cybersec.helpers import JsonDict, sdk_result, sdk_error

_VAULT_PATH = os.getenv("CYBERSEC_VAULT_PATH", "./data/vault")


def _get_vault():
    from memory.vault.manager import VaultManager
    return VaultManager(_VAULT_PATH)


@tool(
    "vault_scaffold",
    "Scaffold a new CyberSecSuite forensic Obsidian vault. Creates wiki/, .raw/, memories/ directories and seed files. Idempotent.",
    {
        "vault_name": {"type": "string", "description": "Display name for the vault, e.g. 'APT29 Investigation'"},
        "purpose": {"type": "string", "description": "One-line description of the investigation or purpose"},
    },
)
async def vault_scaffold(args: dict[str, Any]) -> JsonDict:
    vault_name = args.get("vault_name", "CyberSecSuite Vault")
    purpose = args.get("purpose", "Forensic investigation workspace")
    try:
        vm = _get_vault()
        result = vm.scaffold(vault_name, purpose)
        return sdk_result(result)
    except Exception as e:
        return sdk_error(str(e))


@tool(
    "vault_status",
    "Return vault health summary: page count, canvas count, sources ingested, hot cache age.",
    {},
)
async def vault_status(args: dict[str, Any]) -> JsonDict:
    try:
        vm = _get_vault()
        return sdk_result(vm.status())
    except Exception as e:
        return sdk_error(str(e))


@tool(
    "vault_ingest",
    "Ingest a file or URL into the forensic vault. Delta-tracked — unchanged sources are skipped unless force=true.",
    {
        "source": {"type": "string", "description": "File path or URL to ingest into .raw/"},
        "category": {
            "type": "string",
            "enum": ["articles", "intel", "malware", "logs", "pcaps"],
            "description": "Where to place the raw source. Defaults to 'articles' for URLs.",
            "default": "articles",
        },
        "force": {"type": "boolean", "default": False, "description": "Re-ingest even if hash unchanged"},
        "tags": {"type": "array", "items": {"type": "string"}, "description": "Tags to apply to extracted wiki pages"},
    },
)
async def vault_ingest(args: dict[str, Any]) -> JsonDict:
    source = args.get("source", "")
    _category = args.get("category", "articles")
    force = args.get("force", False)
    tags = args.get("tags", [])

    if not source:
        return sdk_error("'source' is required")

    try:
        from pathlib import Path
        import time

        vm = _get_vault()

        # URL handling — save to .raw/articles/<slug>-<date>.md
        if source.startswith("http://") or source.startswith("https://"):
            from urllib.parse import urlparse
            parsed = urlparse(source)
            slug = (parsed.path.rstrip("/").split("/")[-1] or parsed.netloc).lower().replace(" ", "-")[:50]
            date = time.strftime("%Y-%m-%d")
            raw_path = Path(_VAULT_PATH) / ".raw" / "articles" / f"{slug}-{date}.md"
            raw_path.parent.mkdir(parents=True, exist_ok=True)
            if not raw_path.exists():
                raw_path.write_text(f"---\nsource_url: {source}\ningested_at: {date}\ntags: {tags}\n---\n\n# {slug}\n\nFetch content manually via web_search or web_fetch.\n", encoding="utf-8")
            source = str(raw_path)

        src_path = Path(source)
        if not src_path.exists():
            return sdk_error(f"Source not found: {source}")

        # Delta check
        already_done, file_hash = vm.check_already_ingested(src_path)
        if already_done and not force:
            return sdk_result({"skipped": True, "reason": "Already ingested (unchanged). Use force=true to re-ingest.", "source": source})

        # Record ingest — actual content extraction is done by the agent
        # The MCP tool records tracking metadata; Claude handles wiki page creation
        vm.record_ingest(src_path, file_hash, pages_created=[], pages_updated=["wiki/log.md", "wiki/hot.md"])

        return sdk_result({
            "ingested": True,
            "source": source,
            "hash": file_hash,
            "vault_path": str(vm.vault_path),
            "instructions": (
                "Source recorded. Now: (1) read the source file, "
                "(2) extract entities/IOCs/TTPs/findings, "
                "(3) create wiki pages in wiki/<domain>/<name>.md, "
                "(4) update wiki/index.md and wiki/log.md, "
                "(5) update wiki/hot.md with key facts."
            ),
        })
    except Exception as e:
        return sdk_error(str(e))


@tool(
    "vault_query",
    "Query the forensic vault for information. Reads hot cache first, then index, then relevant pages.",
    {
        "question": {"type": "string", "description": "What to look up in the vault"},
        "domain": {
            "type": "string",
            "enum": ["entities", "iocs", "ttps", "cases", "findings", "concepts", "all"],
            "default": "all",
            "description": "Which wiki domain to search",
        },
        "limit": {"type": "integer", "default": 10, "description": "Max pages to include in result"},
    },
)
async def vault_query(args: dict[str, Any]) -> JsonDict:
    question = args.get("question", "")
    domain = args.get("domain", "all")
    limit = min(args.get("limit", 10), 50)

    if not question:
        return sdk_error("'question' is required")

    try:
        from pathlib import Path

        vault = Path(_VAULT_PATH)
        wiki = vault / "wiki"

        if not wiki.exists():
            return sdk_error("Vault not found. Run vault_scaffold first.")

        # Read hot cache
        hot_content = ""
        hot_path = wiki / "hot.md"
        if hot_path.exists():
            hot_content = hot_path.read_text(encoding="utf-8")

        # Find relevant pages by keyword matching
        search_terms = question.lower().split()
        domains = [domain] if domain != "all" else ["entities", "iocs", "ttps", "cases", "findings", "concepts"]
        matches: list[dict[str, Any]] = []
        for d in domains:
            d_path = wiki / d
            if not d_path.exists():
                continue
            for md_file in sorted(d_path.glob("*.md")):
                if md_file.name.startswith("_"):
                    continue
                content = md_file.read_text(encoding="utf-8")
                score = sum(term in content.lower() for term in search_terms)
                if score > 0:
                    matches.append({"path": str(md_file.relative_to(vault)), "score": score, "content": content[:1000]})

        matches.sort(key=lambda m: m["score"], reverse=True)
        matches = matches[:limit]

        return sdk_result({
            "question": question,
            "hot_cache": hot_content[:2000],
            "matches": matches,
            "match_count": len(matches),
        })
    except Exception as e:
        return sdk_error(str(e))


@tool(
    "vault_lint",
    "Check vault health: orphan pages, missing indexes, stale hot cache.",
    {},
)
async def vault_lint(args: dict[str, Any]) -> JsonDict:
    try:
        vm = _get_vault()
        return sdk_result(vm.lint())
    except Exception as e:
        return sdk_error(str(e))

ALL_TOOLS = [vault_scaffold, vault_status, vault_ingest, vault_query, vault_lint]


# === From session.py ===
"""Session snapshot, agent registry, and best provider tools — SDK in-process MCP server module."""
from __future__ import annotations

from typing import Any

from csmcp._sdk_compat import tool
from csmcp.cybersec.helpers import JsonDict, _get_current_scope, sdk_result, sdk_error


@tool("session_snapshot", "Return a full session state snapshot including scope, usage, budget, and circuit breakers.", {})
async def session_snapshot(args: dict[str, Any]) -> JsonDict:
    try:
        from ai_proxy.providers.registry import get_enabled_providers, get_free_providers
        from ai_proxy.routing.combo import get_circuit_breaker_status, get_usage_counts, budget_guard, Strategy
        from ai_proxy.services.usage_tracker import usage_tracker
    except ImportError:
        return sdk_error("ai_proxy not available")

    scope = _get_current_scope()
    cb_status = get_circuit_breaker_status()
    return sdk_result({
        "status": "success",
        "scope": scope,
        "providers": {"enabled": len(get_enabled_providers()), "free": len(get_free_providers())},
        "usage": usage_tracker.get_summary(),
        "usage_counts": get_usage_counts(),
        "budget": budget_guard.get_all(),
        "circuit_breakers": {
            "total": len(cb_status),
            "open": sum(1 for cb in cb_status if cb["state"] == "open"),
        },
        "strategies_available": [s.value for s in Strategy],
    })


@tool("agent_registry", "List all registered A2A agents with skills and metadata.", {})
async def agent_registry(args: dict[str, Any]) -> JsonDict:
    try:
        from a2a.registry import AgentRegistry
        from a2a.agent_loader import load_cybersecsuite_agents

        registry = AgentRegistry()
        load_cybersecsuite_agents(registry)
        agents = registry.summary()
        orchestrators = [a for a in agents if a.get("claude_metadata", {}).get("role") == "orchestrator"]

        # Append installed marketplace agents (T036).
        try:
            from marketplace.registry import get_registry as _get_mkt_registry
            for item in _get_mkt_registry().list_installed():
                if item.kind == "agent":
                    agents.append({
                        "name": item.id,
                        "description": item.description,
                        "source": "marketplace",
                        "provider": item.provider,
                        "tags": item.tags,
                    })
        except Exception:
            pass  # marketplace not available — skip silently

        return sdk_result({
            "status": "success",
            "total": len(agents),
            "orchestrators": len(orchestrators),
            "specialists": len(agents) - len(orchestrators),
            "agents": agents,
        })
    except Exception as exc:
        return sdk_error(str(exc))


@tool(
    "best_provider",
    "Find the best provider/model for a task based on cost, capability, and circuit breaker state.",
    {
        "task": "string",
        "prefer_free": {"type": "boolean", "default": False},
        "max_cost_per_1k": {"type": "number", "nullable": True},
        "require_tools": {"type": "boolean", "default": False},
        "require_vision": {"type": "boolean", "default": False},
        "min_context": {"type": "integer", "nullable": True},
    },
)
async def best_provider(args: dict[str, Any]) -> JsonDict:
    try:
        from ai_proxy.providers.registry import get_all_providers
        from ai_proxy.routing.combo import get_circuit_breaker_status
    except ImportError:
        return sdk_error("ai_proxy not available")

    prefer_free = args.get("prefer_free", False)
    max_cost_per_1k = args.get("max_cost_per_1k")
    require_tools = args.get("require_tools", False)
    require_vision = args.get("require_vision", False)
    min_context = args.get("min_context")

    open_targets = {cb["target"] for cb in get_circuit_breaker_status() if cb["state"] == "open"}
    candidates = []

    for p in get_all_providers().values():
        if not p.is_available:
            continue
        for m in p.models:
            if m.deprecated:
                continue
            if require_tools and not m.supports_tools:
                continue
            if require_vision and not m.supports_vision:
                continue
            if min_context and m.context_window < min_context:
                continue
            if max_cost_per_1k is not None and m.cost.input > max_cost_per_1k * 1000:
                continue
            if f"{p.id}:{m.id}" in open_targets:
                continue
            candidates.append({
                "provider": p.id, "model": m.id, "is_free": p.is_free,
                "cost_input": m.cost.input, "cost_output": m.cost.output,
                "context_window": m.context_window,
                "supports_tools": m.supports_tools, "supports_vision": m.supports_vision,
            })

    if prefer_free:
        candidates.sort(key=lambda c: (not c["is_free"], c["cost_input"]))
    else:
        candidates.sort(key=lambda c: c["cost_input"])

    return sdk_result({
        "status": "success",
        "task": args.get("task", ""),
        "best": candidates[0] if candidates else None,
        "candidates_count": len(candidates),
    })


ALL_TOOLS = [session_snapshot, agent_registry, best_provider]

