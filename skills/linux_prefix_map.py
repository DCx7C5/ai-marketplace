#!/usr/bin/env python3
"""
Linux Component Subprefix Map

This file is the single source of truth for how linux/ skills are renamed
during the flat migration.

The goal (per project conventions):
- Use short, conventional, memorable prefixes.
- Pattern: linux-{component}-{topic}-{action}
- Examples:
    linux-fs-permissions-analyze
    linux-kernel-syscall-abuse-detect
    linux-proc-maps-analyze

This map was generated from actual inventory of the current tree (227 skills).
"""

from __future__ import annotations
from pathlib import Path
from typing import Dict

# =============================================================================
# CANONICAL LINUX COMPONENT MAP
# =============================================================================
#
# Key   = current first or second level directory name under linux/
# Value = the short prefix we will use in the final flat name
#
# Rules followed:
# - Short and conventional (fs, net, proc, mem, etc.)
# - Avoid collision with top-level categories (harden, forensic, etc.)
# - "linux-" is always the outer prefix for linux skills.
# - Only meaningful skill-oriented actions become skills (no "read", "list", etc.)

LINUX_COMPONENT_MAP: Dict[str, str] = {
    # Filesystem related
    "filesystem": "fs",
    "ntfs": "fs-ntfs",
    "xfs": "fs-xfs",
    "tmpfs": "fs-tmp",
    "vfs": "fs-vfs",

    # Kernel
    "kernel": "kernel",
    "syscall": "kernel-syscall",
    "ebpf": "kernel-ebpf",
    "network-stack": "kernel-net",
    "boot": "kernel-boot",

    # Processes & execution
    "processes": "proc",
    "proc-fs": "proc",
    "ptrace": "proc-ptrace",
    "ipc": "proc-ipc",

    # Memory
    "memory": "mem",
    "rop": "mem-rop",

    # Networking & services
    "network-services": "net",
    "smb": "net-smb",
    "nfs": "net-nfs",
    "tftp": "net-tftp",
    "rsync": "net-rsync",
    "webdav": "net-webdav",

    # Hardware / firmware
    "hardware": "hw",
    "firmware": "hw-firmware",
    "uefi": "hw-uefi",

    # Identity & privileges
    "identity": "id",
    "capabilities": "id-cap",
    "suid": "id-suid",
    "sudo": "id-sudo",

    # Services & D-Bus
    "services": "svc",
    "dbus": "svc-dbus",

    # Logging & audit
    "logging": "log",
    "auditd": "log-auditd",
    "logs": "log",
    "lastlog": "log-lastlog",

    # Forensics (linux-specific artifacts)
    "forensics": "linux-forensic",   # to distinguish from top-level forensics/
    "disk": "linux-forensic-disk",
    "artifact": "linux-forensic-artifact",
    "timeline": "linux-forensic-timeline",

    # Hardening (linux-specific)
    "hardening": "linux-harden",
    "apparmor": "linux-harden-apparmor",
    "aslr-nx": "linux-harden-aslr",
    "grsecurity": "linux-harden-grsec",

    # Containers
    "containers": "container",
    "namespace": "container-ns",
    "seccomp": "container-seccomp",

    # Supply chain / persistence
    "supply-chain": "supply",
    "shared-library": "supply-lib",

    # Shell / environment
    "shell": "shell",
    "profile": "shell-profile",

    # Other
    "software": "sw",
    "browser": "sw-browser",
}

# Common action normalizations (only the ones we care about for linux)
LINUX_ACTION_MAP = {
    "analyze": "analyze",
    "audit": "audit",
    "detect": "detect",
    "exploit": "exploit",
    "forensic": "forensic",
    "verify": "verify",
    "configure": "configure",
    "monitor": "monitor",
    "deploy": "deploy",
    "assess": "assess",
    "create": "create",
    # We deliberately do NOT create skills for generic "read", "list", "get", etc.
}

# =============================================================================
# Helper functions
# =============================================================================

def normalize_linux_path(old_rel_path: str) -> str:
    """
    Convert a relative path under linux/ into the final flat skill name
    following the project convention:

        linux-{component}-{rest-of-path}

    Only the first (or first+second as a compound) segment(s) are looked up
    in the map to decide the canonical short prefix.
    The remaining path segments are slugified with minimal further mapping
    to avoid the duplication we saw earlier.
    """
    parts = [p for p in Path(old_rel_path).parts if p]

    # Drop generic uninteresting actions early (user: "read is not worth a skill")
    generic_noise = {"read", "list", "get", "show", "dump", "cat", "ls"}
    parts = [p for p in parts if p.lower() not in generic_noise]

    if not parts:
        return ""

    first = parts[0]
    rest = parts[1:]

    # Compound key lookup (e.g. kernel/network-stack)
    compound = "/".join(parts[:2]) if len(parts) >= 2 else ""
    if compound in LINUX_COMPONENT_MAP:
        prefix = LINUX_COMPONENT_MAP[compound]
        rest = parts[2:]
    else:
        prefix = LINUX_COMPONENT_MAP.get(first, first)

    # For the remaining parts, do only light cleaning.
    # We do NOT re-apply the full map here to avoid duplication.
    cleaned = []
    for p in rest:
        # Only apply very obvious short mappings if they exist
        if p in LINUX_COMPONENT_MAP and len(LINUX_COMPONENT_MAP[p]) <= 8:
            cleaned.append(LINUX_COMPONENT_MAP[p])
        else:
            cleaned.append(p)

    slug = "-".join([prefix] + cleaned)

    if not slug.startswith("linux-"):
        slug = "linux-" + slug

    slug = slug.replace("--", "-")
    return slug


def get_component_for_path(old_rel_path: str) -> str:
    """Return the primary component key for a given linux path."""
    parts = [p for p in Path(old_rel_path).parts if p]
    if not parts:
        return "unknown"
    first = parts[0]
    return LINUX_COMPONENT_MAP.get(first, first)


# =============================================================================
# Self-test / usage example
# =============================================================================

if __name__ == "__main__":
    test_paths = [
        "filesystem/permissions/analyze",
        "filesystem/tmpfs/artifact/collect",
        "kernel/network-stack/raw-socket/abuse/detect",
        "kernel/syscall/audit/monitor",
        "processes/proc-fs/maps/analyze",
        "network-services/smb/share/enum",
        "hardware/firmware/uefi/detect",
        "identity/capabilities/audit",
        "logging/auditd/rule/configure",
        "forensics/disk/timeline/plaso/forensic",
        "hardening/apparmor/profile/create/configure",
        "containers/namespace/user/privesc/detect",
    ]

    print("Linux Prefix Mapping — Examples\n")
    for p in test_paths:
        new = normalize_linux_path(p)
        print(f"  {p:55} → {new}")

    print("\nMap contains", len(LINUX_COMPONENT_MAP), "entries.")
    print("Edit this file to refine the canonical subprefixes.")
