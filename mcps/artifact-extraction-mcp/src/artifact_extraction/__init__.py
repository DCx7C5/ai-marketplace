"""
artifact-extraction MCP Package
"""

from artifact_extraction.tools import registry_extractor, event_log_parser, prefetch_analyzer, shortcuts_parser, mru_extractor, thumbnail_analyzer, recycle_bin_parser, temp_collector

__version__ = "1.0.0"
__author__ = "CyberSecSuite Contributors"
__license__ = "MIT"

__all__ = [
    "__version__",
    "__author__",
    "__license__",
    "registry_extractor", "event_log_parser", "prefetch_analyzer", "shortcuts_parser", "mru_extractor", "thumbnail_analyzer", "recycle_bin_parser", "temp_collector"
]
