"""
Helper functions for working with the Wise API client.
"""

from dataclasses import dataclass
from typing import Dict, Any, List

from .wise_client import WiseApiClient
from .types import WiseProfile


@dataclass
class WiseClientContext:
    """
    Context class that contains the Wise API client and the matched profile.
    """
    wise_api_client: WiseApiClient
    profile: WiseProfile


def init_wise_client(profile_type: str = "personal") -> WiseClientContext:
    api_client = WiseApiClient()

    profiles = api_client.list_profiles()
    
    if not profiles:
        raise Exception("No profiles found. Please create a profile in Wise first.")
    
    # Find the first profile with the specified type that is not "HIDDEN"
    matching_profile = None
    for profile in profiles:
        if str(profile.get("type")).lower() == str(profile_type).lower() and profile.get("currentState") != "HIDDEN":
            matching_profile = profile
            break
    
    if not matching_profile:
        raise Exception(f"No profile found with type '{profile_type}'. Available types: {', '.join(set(p.get('type', 'unknown') for p in profiles))}")
    
    wise_profile = WiseProfile(profile_id=str(matching_profile["id"]))
    
    return WiseClientContext(api_client, wise_profile)