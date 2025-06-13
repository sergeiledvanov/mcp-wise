"""
Wise API resources for the FastMCP server.
"""

from typing import Dict, List, Any, Optional

from wise_mcp.app import mcp

from ..api.wise_client_helper import init_wise_client
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
    
    recipients_data = ctx.wise_api_client.list_recipients(ctx.profile.profile_id, currency)

    # Format the recipients as strings
    formatted_recipients = []
    for recipient in recipients_data.get("content", []):
        full_name = recipient.get("name", {}).get("fullName", "Unknown")
        account_summary = recipient.get("accountSummary", "")
        currency = recipient.get("currency", "")
        country = recipient.get("country", "")
        
        formatted_string = f"{full_name}, {account_summary} - {currency} ({country})"
        formatted_recipients.append(formatted_string)
        
    return formatted_recipients

@mcp.tool()
def find_recipient(name: str, profile_type: str = "personal", currency: Optional[str] = None) -> Dict[str, Any]:
    """
    Finds the best matching recipient by name from the Wise API.

    Args:
        name: Name of the recipient to find (fuzzy matching will be applied)
        profile_type: The type of profile to list recipients for. one of [personal, business]
        currency: Optional. Filter recipients by currency code (e.g., 'EUR', 'USD')

    Returns:
        Dictionary containing the best matching recipient's information

    Raises:
        Exception: If the API request fails or if no recipients are found
    """

    ctx = init_wise_client(profile_type)
    recipients_data = ctx.wise_api_client.list_recipients(ctx.profile.profile_id, currency)
    recipients = recipients_data.get("content", [])

    if not recipients:
        raise Exception(f"No recipients found for profile type '{profile_type}'" +
                        (f" and currency '{currency}'" if currency else ""))

    return find_best_match_by_name(recipients, name)


