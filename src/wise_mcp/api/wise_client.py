"""
Wise API client for interacting with the Wise API.
"""

import os
import requests
from typing import Dict, List, Optional, Any

from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class WiseApiClient:
    """Client for interacting with the Wise API."""

    def __init__(self):
        """
        Initialize the Wise API client.
        
        Args:
            api_token: The API token to use for authentication.
        """

        is_sandbox = os.getenv("WISE_IS_SANDBOX", "true").lower() == "true"
        self.api_token = os.getenv("WISE_API_TOKEN", "")

        if not self.api_token:
            raise ValueError("WISE_API_TOKEN must be provided or set in the environment")
        
        if is_sandbox:
            self.base_url = "https://api.sandbox.transferwise.tech"
        else:
            self.base_url = "https://api.transferwise.com"

        self.headers = {
            "Authorization": f"Bearer {self.api_token}",
            "Content-Type": "application/json"
        }
    
    def list_profiles(self) -> List[Dict[str, Any]]:
        """
        List all profiles associated with the API token.
        
        Returns:
            List of profile objects from the Wise API.
        
        Raises:
            Exception: If the API request fails.
        """
        url = f"{self.base_url}/v1/profiles"
        response = requests.get(url, headers=self.headers)
        
        if response.status_code >= 400:
            self._handle_error(response)
            
        return response.json()
    
    def get_profile(self, profile_id: str) -> Dict[str, Any]:
        """
        Get a specific profile by ID.
        
        Args:
            profile_id: The ID of the profile to get.
            
        Returns:
            Profile object from the Wise API.
            
        Raises:
            Exception: If the API request fails.
        """
        url = f"{self.base_url}/v1/profiles/{profile_id}"
        response = requests.get(url, headers=self.headers)
        
        if response.status_code >= 400:
            self._handle_error(response)
            
        return response.json()
    
    def list_recipients(self, profile_id: str) -> List[Dict[str, Any]]:
        """
        List all recipients for a profile.
        
        Args:
            profile_id: The ID of the profile to list recipients for.
            
        Returns:
            List of recipient objects from the Wise API.
            
        Raises:
            Exception: If the API request fails.
        """
        url = f"{self.base_url}/v2/accounts"
        params = {"profile": profile_id}
        
        response = requests.get(url, headers=self.headers, params=params)
        
        if response.status_code >= 400:
            self._handle_error(response)
            
        return response.json()
    
    def _handle_error(self, response: requests.Response) -> None:
        """
        Handle API errors by raising an exception with details.
        
        Args:
            response: The response object from the API request.
            
        Raises:
            Exception: With details about the API error.
        """
        try:
            error_data = response.json()
            error_msg = error_data.get('errors', [{}])[0].get('message', 'Unknown error')
        except:
            error_msg = f"Error: HTTP {response.status_code}"
            
        raise Exception(f"Wise API Error: {error_msg}")