"""
filesystem-forensics MCP Package
"""

from filesystem_forensics.tools import file_hasher, carving_engine, metadata_extractor, timeline_generator, access_tracker, signature_validator, deletion_recovery, archive_analyzer

__version__ = "1.0.0"
__author__ = "CyberSecSuite Contributors"
__license__ = "MIT"

__all__ = [
    "__version__",
    "__author__",
    "__license__",
    "file_hasher", "carving_engine", "metadata_extractor", "timeline_generator", "access_tracker", "signature_validator", "deletion_recovery", "archive_analyzer"
]
