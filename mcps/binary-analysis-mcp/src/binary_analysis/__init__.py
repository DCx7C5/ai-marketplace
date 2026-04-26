"""
binary-analysis MCP Package
"""

from binary_analysis.tools import disassembler, decompiler, function_analyzer, string_finder, import_resolver, xref_generator, control_flow_grapher, entropy_calculator

__version__ = "1.0.0"
__author__ = "CyberSecSuite Contributors"
__license__ = "MIT"

__all__ = [
    "__version__",
    "__author__",
    "__license__",
    "disassembler", "decompiler", "function_analyzer", "string_finder", "import_resolver", "xref_generator", "control_flow_grapher", "entropy_calculator"
]
