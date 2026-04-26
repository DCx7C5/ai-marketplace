"""
email-analysis MCP Package
"""

from email_analysis.tools import eml_parser, header_analyzer, attachment_extractor, phishing_detector, sender_verifier, link_analyzer, mime_decoder, reputation_checker

__version__ = "1.0.0"
__author__ = "CyberSecSuite Contributors"
__license__ = "MIT"

__all__ = [
    "__version__",
    "__author__",
    "__license__",
    "eml_parser", "header_analyzer", "attachment_extractor", "phishing_detector", "sender_verifier", "link_analyzer", "mime_decoder", "reputation_checker"
]
