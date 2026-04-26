"""
api-security MCP Package
"""

from api_security.tools import endpoint_scanner, payload_fuzzer, auth_tester, rate_limiter_checker, header_analyzer, response_validator, injection_detector, schema_validator

__version__ = "1.0.0"
__author__ = "CyberSecSuite Contributors"
__license__ = "MIT"

__all__ = [
    "__version__",
    "__author__",
    "__license__",
    "endpoint_scanner", "payload_fuzzer", "auth_tester", "rate_limiter_checker", "header_analyzer", "response_validator", "injection_detector", "schema_validator"
]
