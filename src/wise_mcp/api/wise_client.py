"""
Wise API client for interacting with the Wise API.
"""

import os
import uuid
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
    
    def create_quote(
        self, 
        profile_id: str, 
        source_currency: str, 
        target_currency: str, 
        source_amount: float,
        target_account_id: str
    ) -> Dict[str, Any]:
        """
        Create a quote for a currency exchange.
        
        Args:
            profile_id: The ID of the profile to create the quote for
            source_currency: The source currency code (e.g., 'USD')
            target_currency: The target currency code (e.g., 'EUR')
            source_amount: The amount in the source currency to exchange
            target_account_id: The recipient account ID
            
        Returns:
            Quote object from the Wise API containing exchange rate details
            
        Raises:
            Exception: If the API request fails
        """
        url = f"{self.base_url}/v3/profiles/{profile_id}/quotes"
        payload = {
            "sourceCurrency": source_currency,
            "targetCurrency": target_currency,
            "sourceAmount": source_amount
        }
        
        payload["targetAccount"] = target_account_id
        
        response = requests.post(url, headers=self.headers, json=payload)
        
        if response.status_code >= 400:
            self._handle_error(response)
            
        return response.json()
    
    def create_transfer(
        self,
        target_account_id: str,
        quote_uuid: str,
        reference: str,
        source_of_funds: Optional[str] = None,
        customer_transaction_id: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Create a transfer using a previously generated quote.
        
        Args:
            target_account_id: The ID of the recipient account to send money to (required)
            quote_uuid: The UUID of the quote to use for this transfer (required)
            reference: The reference message for the transfer (e.g., "Invoice payment")
            source_of_funds: Source of the funds (e.g., "salary", "savings") (optional)
            customer_transaction_id: A unique ID for the transaction (optional, will be generated if not provided)
            
        Returns:
            Transfer object from the Wise API containing transfer details
            
        Raises:
            Exception: If the API request fails
        """
        url = f"{self.base_url}/v1/transfers"
        
        # Create the details object with required reference
        details = {"reference": reference}
        
        # Add sourceOfFunds if provided
        if source_of_funds:
            details["sourceOfFunds"] = source_of_funds
        
        # Build the payload
        payload = {
            "targetAccount": target_account_id,
            "quoteUuid": quote_uuid,
            "details": details
        }
        
        # Add customer transaction ID if provided, otherwise it will be generated by Wise
        if customer_transaction_id:
            payload["customerTransactionId"] = customer_transaction_id or str(uuid.uuid4())
        
        response = requests.post(url, headers=self.headers, json=payload)
        
        if response.status_code >= 400:
            self._handle_error(response)
            
        return response.json()

    def fund_transfer(
        self,
        profile_id: str,
        transfer_id: str,
        type: str
    ) -> Dict[str, Any]:
        """
        Fund a transfer that has been created.
        
        Args:
            profile_id: The ID of the profile that owns the transfer
            transfer_id: The ID of the transfer to fund
            type: The payment method type (required). Only
                  'BALANCE' is supported for now. If another value is provided, raise an error.
            
        Returns:
            Payment object from the Wise API containing payment details
            
        Raises:
            Exception: If the API request fails
        """

        if type != "BALANCE":
            raise ValueError("Only 'BALANCE' payment type is supported for funding transfers.")

        url = f"{self.base_url}/v3/profiles/{profile_id}/transfers/{transfer_id}/payments"
        
        # Build the payment payload
        payload = {"type": type}
        
        response = requests.post(url, headers=self.headers, json=payload)
        
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