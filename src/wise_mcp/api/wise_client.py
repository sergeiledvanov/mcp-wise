"""
Wise API client for interacting with the Wise API.
"""

import os
import uuid
import requests
from typing import Dict, List, Optional, Any

from dotenv import load_dotenv
from .types import WiseRecipient, WiseFundResponse, WiseScaResponse, WiseFundWithScaResponse, PaymentRequestInvoiceCommand, PaymentRequestV2, Money

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
        url = f"{self.base_url}/v2/profiles"
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
        url = f"{self.base_url}/v2/profiles/{profile_id}"
        response = requests.get(url, headers=self.headers)
        
        if response.status_code >= 400:
            self._handle_error(response)
            
        return response.json()
    
    def list_recipients(self,
                        profile_id: str,
                        currency: Optional[str] = None) -> List[WiseRecipient]:
        """
        List all recipients for a profile.
        
        Args:
            profile_id: The ID of the profile to list recipients for.
            currency: Optional. Filter recipients by currency.
            
        Returns:
            List of WiseRecipient objects.
            
        Raises:
            Exception: If the API request fails.
        """
        url = f"{self.base_url}/v2/accounts"
        params = {"profile": profile_id}
        
        # Add currency filter if provided
        if currency:
            params["currency"] = currency
        
        response = requests.get(url, headers=self.headers, params=params)
        
        if response.status_code >= 400:
            self._handle_error(response)
            
        response_data = response.json()
        
        # Convert the raw recipient data to WiseRecipient objects
        recipients = []
        for recipient in response_data.get("content", []):
            recipients.append(WiseRecipient(
                id=str(recipient.get("id", "")),
                profile_id=str(recipient.get("profile", "")),
                full_name=recipient.get("name", {}).get("fullName", "Unknown"),
                currency=recipient.get("currency", ""),
                country=recipient.get("country", ""),
                account_summary=recipient.get("accountSummary", ""),
            ))
            
        return recipients
    
    def create_quote(
        self, 
        profile_id: str, 
        source_currency: str, 
        target_currency: str, 
        source_amount: float,
        recipient_id: str
    ) -> Dict[str, Any]:
        """
        Create a quote for a currency exchange.
        
        Args:
            profile_id: The ID of the profile to create the quote for
            source_currency: The source currency code (e.g., 'USD')
            target_currency: The target currency code (e.g., 'EUR')
            source_amount: The amount in the source currency to exchange
            recipient_id: The recipient account ID
            
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
        
        payload["targetAccount"] = recipient_id
        
        response = requests.post(url, headers=self.headers, json=payload)
        
        if response.status_code >= 400:
            self._handle_error(response)
            
        return response.json()
    
    def create_transfer(
        self,
        recipient_id: str,
        quote_uuid: str,
        reference: str,
        customer_transaction_id: str,
        source_of_funds: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Create a transfer using a previously generated quote.
        
        Args:
            recipient_id: The ID of the recipient account to send money to (required)
            quote_uuid: The UUID of the quote to use for this transfer (required)
            reference: The reference message for the transfer (e.g., "Invoice payment")
            customer_transaction_id: A unique ID for the transaction
            source_of_funds: Source of the funds (e.g., "salary", "savings") (optional)

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
            "targetAccount": recipient_id,
            "quoteUuid": quote_uuid,
            "details": details,
            "customerTransactionId": customer_transaction_id,
        }
        
        response = requests.post(url, headers=self.headers, json=payload)
        
        if response.status_code >= 400:
            self._handle_error(response)
            
        return response.json()

    def fund_transfer(
        self,
        profile_id: str,
        transfer_id: str,
        type: str
    ) -> WiseFundWithScaResponse:
        """
        Fund a transfer that has been created. This may trigger a Strong Customer Authentication (SCA) flow.
        
        Args:
            profile_id: The ID of the profile that owns the transfer
            transfer_id: The ID of the transfer to fund
            type: The payment method type (required). Only
                  'BALANCE' is supported for now. If another value is provided, raise an error.
            
        Returns:
            WiseFundWithScaResponse object which may include:
            - fund_response: The standard payment response if no SCA is required
            - sca_response: SCA challenge details if SCA is required

        Raises:
            Exception: If the API request fails
        """

        if type != "BALANCE":
            raise ValueError("Only 'BALANCE' payment type is supported for funding transfers.")

        url = f"{self.base_url}/v3/profiles/{profile_id}/transfers/{transfer_id}/payments"
        
        # Build the payment payload
        payload = {"type": type}
        
        response = requests.post(url, headers=self.headers, json=payload)
        result = WiseFundWithScaResponse()

        print(f"Funding transfer {transfer_id} response headers: {response.headers}")
        
        if response.status_code == 403:
            if response.headers.get("x-2fa-approval-result") == "REJECTED":
                result.sca_response = WiseScaResponse(
                    one_time_token=response.headers.get("x-2fa-approval"),
                )
                return result

        elif response.status_code >= 400:
            self._handle_error(response)
            
        response_data = response.json()
        
        result.fund_response = WiseFundResponse(
            type=response_data.get("type", ""),
            status=response_data.get("status", ""),
            error_code=response_data.get("errorCode")
        )
        return result

    def create_empty_invoice(
        self,
        profile_id: str,
        balance_id: int,
        due_at: str,
        issue_date: str
    ) -> PaymentRequestV2:
        """
        Create an empty invoice to get auto-generated fields like invoice number.
        
        Args:
            profile_id: The ID of the profile to create the invoice for
            balance_id: The ID of the balance to use for the invoice
            due_at: Due date in YYYY-MM-DDTHH:MM:SS.SSSZ format
            issue_date: Issue date in YYYY-MM-DDTHH:MM:SS.SSSZ format

        Returns:
            PaymentRequestV2 object containing the created empty invoice
            
        Raises:
            Exception: If the API request fails
        """
        url = f"{self.base_url}/v2/profiles/{profile_id}/acquiring/payment-requests"
        
        payload = {
            "requestType": "INVOICE",
            "selectedPaymentMethods": [],  
            "balanceId": balance_id,
            "dueAt": due_at,
            "issueDate": issue_date,
            "lineItems": []
        }

        response = requests.post(url, headers=self.headers, json=payload)
        
        if response.status_code >= 400:
            self._handle_error(response)
            
        response_data = response.json()
        
        return PaymentRequestV2(
            id=response_data["id"],
            amount=Money(
                value=response_data["amount"]["value"],
                currency=response_data["amount"]["currency"]
            ),
            profile_id=response_data["profileId"],
            balance_id=response_data["balanceId"],
            creator=response_data["creator"],
            status=response_data["status"],
            link=response_data.get("link"),
            created_at=response_data.get("createdAt"),
            published_at=response_data.get("publishedAt"),
            due_at=response_data.get("dueAt"),
            message=response_data.get("message"),
            description=response_data.get("description"),
            reference=response_data.get("reference"),
            request_type=response_data.get("requestType"),
            invoice=response_data.get("invoice")
        )

    def update_payment_request_v2(
        self,
        profile_id: str,
        payment_request_id: str,
        payment_request: PaymentRequestInvoiceCommand
    ) -> PaymentRequestV2:
        """
        Update an existing payment request with full invoice data.
        
        Args:
            profile_id: The ID of the profile
            payment_request_id: The ID of the payment request to update
            payment_request: The payment request command object with full data
            
        Returns:
            PaymentRequestV2 object containing the updated payment request
            
        Raises:
            Exception: If the API request fails
        """
        url = f"{self.base_url}/v2/profiles/{profile_id}/acquiring/payment-requests/{payment_request_id}"
        
        payload = {
            "requestType": payment_request.request_type,
            "selectedPaymentMethods": payment_request.selected_payment_methods,
            "balanceId": payment_request.balance_id,
            "dueAt": payment_request.due_at,
            "issueDate": payment_request.issue_date,
            "lineItems": []
        }
        
        # Add optional fields if they exist
        if payment_request.invoice_number:
            payload["invoiceNumber"] = payment_request.invoice_number
            
        if payment_request.message:
            payload["message"] = payment_request.message
            
        if payment_request.payer:
            payer_data = {}
            if payment_request.payer.name:
                payer_data["name"] = payment_request.payer.name
            if payment_request.payer.email:
                payer_data["email"] = payment_request.payer.email
            if payment_request.payer.address and payment_request.payer.address.countryIso3Code:
                payer_data["address"] = {
                    "firstLine": payment_request.payer.address.firstLine,
                    "countryIso3Code": payment_request.payer.address.countryIso3Code
                }
            if payment_request.payer.locale:
                payer_data["locale"] = payment_request.payer.locale
            payload["payer"] = payer_data
        
        # Convert line items
        for item in payment_request.line_items:
            line_item = {
                "name": item.name,
                "unitPrice": {
                    "value": item.unit_price.value,
                    "currency": item.unit_price.currency
                },
                "quantity": item.quantity
            }
            
            if item.tax:
                line_item["tax"] = {
                    "name": item.tax.name,
                    "percentage": item.tax.percentage,
                    "behaviour": item.tax.behaviour
                }
            
            payload["lineItems"].append(line_item)
        
                # log the payload for debugging
        print(f"Creating payment request with payload: {payload}")

        response = requests.put(url, headers=self.headers, json=payload)
        
        if response.status_code >= 400:
            self._handle_error(response)
            
        response_data = response.json()
        
        return PaymentRequestV2(
            id=response_data["id"],
            amount=Money(
                value=response_data["amount"]["value"],
                currency=response_data["amount"]["currency"]
            ),
            profile_id=response_data["profileId"],
            balance_id=response_data["balanceId"],
            creator=response_data["creator"],
            status=response_data["status"],
            link=response_data.get("link"),
            created_at=response_data.get("createdAt"),
            published_at=response_data.get("publishedAt"),
            due_at=response_data.get("dueAt"),
            message=response_data.get("message"),
            description=response_data.get("description"),
            reference=response_data.get("reference"),
            request_type=response_data.get("requestType"),
            invoice=response_data.get("invoice")
        )

    def publish_payment_request(
        self,
        profile_id: str,
        payment_request_id: str
    ) -> PaymentRequestV2:
        """
        Publish a payment request to make it active and available for payment.
        
        Args:
            profile_id: The ID of the profile
            payment_request_id: The ID of the payment request to publish
            
        Returns:
            PaymentRequestV2 object containing the published payment request
            
        Raises:
            Exception: If the API request fails
        """
        url = f"{self.base_url}/v2/profiles/{profile_id}/acquiring/payment-requests/{payment_request_id}/status"
        
        payload = {"status": "PUBLISHED"}
        
        response = requests.put(url, headers=self.headers, json=payload)
        
        if response.status_code >= 400:
            self._handle_error(response)
            
        response_data = response.json()
        
        return PaymentRequestV2(
            id=response_data["id"],
            amount=Money(
                value=response_data["amount"]["value"],
                currency=response_data["amount"]["currency"]
            ),
            profile_id=response_data["profileId"],
            balance_id=response_data["balanceId"],
            creator=response_data["creator"],
            status=response_data["status"],
            link=response_data.get("link"),
            created_at=response_data.get("createdAt"),
            published_at=response_data.get("publishedAt"),
            due_at=response_data.get("dueAt"),
            message=response_data.get("message"),
            description=response_data.get("description"),
            reference=response_data.get("reference"),
            request_type=response_data.get("requestType"),
            invoice=response_data.get("invoice")
        )

    def get_balance_currencies(self, profile_id: str) -> List[Dict[str, Any]]:
        """
        Get available currencies and balances for a profile.
        
        Args:
            profile_id: The ID of the profile to get balances for
            
        Returns:
            List of balance objects with currency and balance ID information
            
        Raises:
            Exception: If the API request fails
        """
        url = f"{self.base_url}/v1/profiles/{profile_id}/acquiring/requesting-configuration/currency-options"
        response = requests.get(url, headers=self.headers)
        
        if response.status_code >= 400:
            self._handle_error(response)
            
        return response.json()

    def get_ott_token_status(self, ott: str) -> Dict[str, Any]:
        """
        Get the status of a one-time token.
        
        Args:
            ott: One-time token to check status for
            
        Returns:
            Dict containing the token status information as returned by the Wise API
            
        Raises:
            Exception: If the API request fails
        """
        url = f"{self.base_url}/v1/one-time-token/status"
        
        # Create custom headers with the one-time token
        headers = self.headers.copy()
        headers["One-Time-Token"] = ott
        
        response = requests.get(url, headers=headers)
        
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
            
        raise Exception(f"Wise API Error: {error_data}")