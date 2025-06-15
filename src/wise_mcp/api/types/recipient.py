"""
Type definitions for Wise Recipients.
"""

from dataclasses import dataclass
from typing import Optional


@dataclass
class WiseRecipient:
    id: str
    profile_id: str
    full_name: str
    currency: str
    country: str
    account_summary: Optional[str] = None