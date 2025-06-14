"""
Type definitions for Wise Fund Response and SCA handling.
"""

from dataclasses import dataclass
from typing import Optional, List, Dict, Any


@dataclass
class WiseFundResponse:
    type: str
    status: str
    error_code: Optional[str] = None


@dataclass
class WiseScaResponse:
    one_time_token: str


@dataclass
class WiseFundWithScaResponse:
    """Combined response for fund transfer with SCA challenge."""
    fund_response: Optional[WiseFundResponse] = None
    sca_response: Optional[WiseScaResponse] = None
