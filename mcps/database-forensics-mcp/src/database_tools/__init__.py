"""
database-tools MCP Package
"""

from database_tools.tools import (
    artifact_extractor,
    backup_validator,
    data_profiler,
    deadlock_detector,
    dump_parser,
    encryption_validator,
    index_analyzer,
    partitioning_advisor,
    performance_profiler,
    permission_auditor,
    query_optimizer,
    replica_checker,
    schema_analyzer,
    slowlog_analyzer,
    transaction_analyzer,
)

__version__ = "1.0.0"
__author__ = "CyberSecSuite Contributors"
__license__ = "MIT"

__all__ = [
    "__author__",
    "__license__",
    "__version__",
    "artifact_extractor",
    "backup_validator",
    "data_profiler",
    "deadlock_detector",
    "dump_parser",
    "encryption_validator",
    "index_analyzer",
    "partitioning_advisor",
    "performance_profiler",
    "permission_auditor",
    "query_optimizer",
    "replica_checker",
    "schema_analyzer",
    "slowlog_analyzer",
    "transaction_analyzer",
]
