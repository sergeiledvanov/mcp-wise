"""
Type definitions for Wise Fund Response.
"""

from dataclasses import dataclass
from typing import Optional


@dataclass
class WiseFundResponse:
    type: str
    status: str
    error_code: Optional[str] = None