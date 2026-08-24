# Utilities for Pydantic validators, if needed.
import re

def validate_phone_number(v: str) -> str:
    """Basic phone number validator (example)."""
    if not re.match(r'^\+?1?\d{9,15}$', v):
        raise ValueError('Invalid phone number format')
    return v
