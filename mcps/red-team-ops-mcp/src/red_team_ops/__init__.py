"""
red-team-ops MCP Package
"""

from red_team_ops.tools import payload_generator, obfuscator, c2_simulator, persistence_planner, privilege_escalator, lateral_mover, defense_evader, exfil_planner

__version__ = "1.0.0"
__author__ = "CyberSecSuite Contributors"
__license__ = "MIT"

__all__ = [
    "__version__",
    "__author__",
    "__license__",
    "payload_generator", "obfuscator", "c2_simulator", "persistence_planner", "privilege_escalator", "lateral_mover", "defense_evader", "exfil_planner"
]
