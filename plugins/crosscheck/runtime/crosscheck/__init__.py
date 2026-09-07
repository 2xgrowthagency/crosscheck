"""Crosscheck deterministic contracts; collection and authority belong to adapters."""
from .gate import evaluate, validate_receipt, fingerprint

__version__ = "0.3.0-rc.1"
__all__ = ["evaluate", "validate_receipt", "fingerprint"]
