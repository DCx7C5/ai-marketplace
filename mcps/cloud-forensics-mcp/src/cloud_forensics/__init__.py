"""
cloud-forensics MCP Package
"""

from cloud_forensics.tools import aws_auditor, azure_analyzer, gcp_scanner, bucket_enumerator, log_collector, vm_inspector, snapshot_analyzer, credential_finder

__version__ = "1.0.0"
__author__ = "CyberSecSuite Contributors"
__license__ = "MIT"

__all__ = [
    "__version__",
    "__author__",
    "__license__",
    "aws_auditor", "azure_analyzer", "gcp_scanner", "bucket_enumerator", "log_collector", "vm_inspector", "snapshot_analyzer", "credential_finder"
]
