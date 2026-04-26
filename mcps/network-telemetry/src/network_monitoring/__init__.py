"""
network-monitoring MCP Package
"""

from network_monitoring.tools import interface_monitor, bandwidth_profiler, connection_tracker, packet_inspector, latency_meter, throughput_analyzer

__version__ = "1.0.0"
__author__ = "CyberSecSuite Contributors"
__license__ = "MIT"

__all__ = [
    "__version__",
    "__author__",
    "__license__",
    "interface_monitor", "bandwidth_profiler", "connection_tracker", "packet_inspector", "latency_meter", "throughput_analyzer"
]
