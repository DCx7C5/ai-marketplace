"""
osint-recon MCP Package
"""

from osint_recon.tools import domain_scanner, dns_enumerator, subdomain_finder, whois_lookup, ssl_analyzer, web_scraper, metadata_extractor, reverse_lookup

__version__ = "1.0.0"
__author__ = "CyberSecSuite Contributors"
__license__ = "MIT"

__all__ = [
    "__version__",
    "__author__",
    "__license__",
    "domain_scanner", "dns_enumerator", "subdomain_finder", "whois_lookup", "ssl_analyzer", "web_scraper", "metadata_extractor", "reverse_lookup"
]
