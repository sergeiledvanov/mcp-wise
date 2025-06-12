"""
Wise API resources for the MCP server.
"""

import os
from typing import Dict, List, Any

from mcp import resource
from ..api.wise_client import WiseApiClient


@resource
def list_recipients() -> List[Dict[str, Any]]:
    """
    MCP resource to list all recipients from the Wise API.
    
    Returns:
        List of recipients from the Wise API.
    
    Raises:
        Exception: If the API request fails or profile ID is not available.
    """
    # Initialize the Wise API client
    api_client = WiseApiClient()
    
    # Get the profile ID from the first available profile
    # as per requirements, we need to obtain a profile ID
    profiles = api_client.list_profiles()
    
    if not profiles:
        raise Exception("No profiles found. Please create a profile in Wise first.")
    
    # Get the first profile ID
    profile_id = str(profiles[0]["id"])
    
    # List all recipients for the profile
    return api_client.list_recipients(profile_id)