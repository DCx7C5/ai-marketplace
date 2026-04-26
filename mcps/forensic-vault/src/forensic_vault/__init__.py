"""
forensic-vault MCP Package
"""

from forensic_vault.tools import (
    artifact_vault,
    case_management,
    chain_of_custody,
    entropy_analyzer,
    evidence_handler,
    evidence_validator,
    hash_analyzer,
    ioc_extractor,
    log_parser,
    malware_analyzer,
    memory_forensics,
    signature_matcher,
    timeline_builder,
    yara_scanner,
)

__version__ = "1.0.0"
__author__ = "CyberSecSuite Contributors"
__license__ = "MIT"

__all__ = [
    "__author__",
    "__license__",
    "__version__",
    "artifact_vault",
    "case_management",
    "chain_of_custody",
    "entropy_analyzer",
    "evidence_handler",
    "evidence_validator",
    "hash_analyzer",
    "ioc_extractor",
    "log_parser",
    "malware_analyzer",
    "memory_forensics",
    "signature_matcher",
    "timeline_builder",
    "yara_scanner",
]
