"""
code-analysis MCP Package
"""

from code_analysis.tools import ast_parser, vulnerability_scanner, complexity_analyzer, dependency_auditor, secret_detector, pattern_finder, metric_calculator, report_generator

__version__ = "1.0.0"
__author__ = "CyberSecSuite Contributors"
__license__ = "MIT"

__all__ = [
    "__version__",
    "__author__",
    "__license__",
    "ast_parser", "vulnerability_scanner", "complexity_analyzer", "dependency_auditor", "secret_detector", "pattern_finder", "metric_calculator", "report_generator"
]
