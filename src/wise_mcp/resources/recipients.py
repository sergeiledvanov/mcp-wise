"""
Wise API resources for the FastMCP server.
"""

from typing import Dict, List, Any, Optional

from wise_mcp.app import mcp

from ..api.wise_client_helper import init_wise_client
from ..api.types import WiseRecipient
from ..utils.string_utils import find_best_match_by_name

@mcp.tool()
def list_recipients(profile_type: str = "personal", currency: Optional[str] = None) -> List[str]:
    """
    Returns all recipients from the Wise API for the given profile type of current user. If a
    user has multiple profiles of that type, it will return recipients from the first profile.

    Args:
        profile_type: The type of profile to list recipients for. one of [personal, business]
        currency: Optional. Filter recipients by currency code (e.g., 'EUR', 'USD')

    Returns:
        List of formatted strings with recipient information
    
    Raises:
        Exception: If the API request fails or profile ID is not available.
    """

    ctx = init_wise_client(profile_type)
    
    return ctx.wise_api_client.list_recipients(ctx.profile.profile_id, currency)
