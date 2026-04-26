"""
dystopian-crypto MCP Package
"""

from dystopian_crypto.tools import aes_cipher, rsa_encryptor, hash_generator, signature_verifier, key_derivator, random_generator, certificate_parser, key_rotator, entropy_analyzer, algorithm_detector, padding_validator, key_escrow_manager

__version__ = "1.0.0"
__author__ = "CyberSecSuite Contributors"
__license__ = "MIT"

__all__ = [
    "__version__",
    "__author__",
    "__license__",
    "aes_cipher", "rsa_encryptor", "hash_generator", "signature_verifier", "key_derivator", "random_generator", "certificate_parser", "key_rotator", "entropy_analyzer", "algorithm_detector", "padding_validator", "key_escrow_manager"
]
