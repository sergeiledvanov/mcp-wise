# Wise API: Recipient Creation Implementation Guide

This document provides comprehensive information about implementing Wise's recipient creation API in a Python server.

## 1. Endpoints for Recipient Creation

The Wise API uses different versions for recipient operations:

| Operation | HTTP Method | Endpoint | Description |
|-----------|------------|----------|-------------|
| Create recipient | POST | `/v1/accounts` | Create a standard recipient account |
| Create refund recipient | POST | `/v1/accounts?refund=true` | Create a recipient for refunds |
| List recipients | GET | `/v2/accounts` | Get all recipients |
| Get recipient by ID | GET | `/v2/accounts/{accountId}` | Get a specific recipient |
| Deactivate recipient | DELETE | `/v2/accounts/{accountId}` | Deactivate a recipient |
| Get requirements | GET | `/v1/quotes/{quoteId}/account-requirements` | Get dynamic recipient requirements |

## 2. Authentication

Wise API uses token-based authentication:

```python
headers = {
    'Authorization': 'Bearer YOUR_API_TOKEN',
    'Content-Type': 'application/json'
}
```

The API token can be obtained through:
1. The Wise Developer Portal
2. OAuth 2.0 flow for production integrations
3. API key for certain partner integrations

## 3. Creating Recipients

### 3.1 Request Format

The request format varies based on currency and recipient country. Here's a general structure:

```python
import requests
import json

def create_recipient(token, profile_id, currency, account_holder_name, country, account_details):
    url = "https://api.wise.com/v1/accounts"
    
    payload = {
        "currency": currency,           # e.g., "USD", "EUR", "GBP"
        "type": account_type,           # Determined by currency/country combination
        "profile": profile_id,          # Your Wise profile ID
        "accountHolderName": account_holder_name,
        "country": country,             # Two-letter country code
        "details": account_details      # Varies by country/currency (see below)
    }
    
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    
    response = requests.post(url, headers=headers, data=json.dumps(payload))
    return response.json()
```

### 3.2 Account Details by Country/Currency

The `details` object varies based on recipient country and currency:

#### EUR (SEPA countries)
```python
details = {
    "legalType": "PRIVATE",  # or "BUSINESS"
    "IBAN": "DE89370400440532013000"
}
```

#### GBP (United Kingdom)
```python
details = {
    "legalType": "PRIVATE",  # or "BUSINESS"
    "sortCode": "231470",
    "accountNumber": "28821822"
}
```

#### USD (United States)
```python
details = {
    "legalType": "PRIVATE",  # or "BUSINESS"
    "accountType": "CHECKING",  # or "SAVINGS"
    "accountNumber": "12345678",
    "routingNumber": "111000000",
    "abartn": "111000000"  # Sometimes required instead of routingNumber
}
```

#### AUD (Australia)
```python
details = {
    "legalType": "PRIVATE",  # or "BUSINESS"
    "bsbCode": "062-001",
    "accountNumber": "12345678"
}
```

#### Other Countries
For other countries, you need to first check the dynamic recipient requirements using the account-requirements endpoint.

### 3.3 Email Recipients

For email recipients (where the recipient will be notified to provide their bank details):

```python
payload = {
    "currency": currency,
    "type": "email",
    "profile": profile_id,
    "accountHolderName": account_holder_name,
    "details": {
        "email": "recipient@example.com"
    }
}
```

## 4. Response Format

### 4.1 Successful Response

```json
{
  "id": 12345678,
  "profile": 9876543,
  "accountHolderName": "John Smith",
  "currency": "USD",
  "country": "US",
  "type": "aba",
  "details": {
    "legalType": "PRIVATE",
    "accountType": "CHECKING",
    "accountNumber": "12345678",
    "routingNumber": "111000000"
  },
  "user": 45678923
}
```

### 4.2 Error Responses

Wise API uses HTTP status codes to indicate success or failure:

- 400: Bad Request (invalid parameters)
- 401: Unauthorized (authentication issues)
- 403: Forbidden (permission issues)
- 404: Not Found (resource doesn't exist)
- 500: Server error

Error response body:

```json
{
  "errors": [
    {
      "code": "NOT_VALID",
      "message": "Account number is invalid",
      "path": "details.accountNumber"
    }
  ]
}
```

## 5. Getting Dynamic Recipient Requirements

Before creating a recipient, you can get the specific requirements for that currency/country combination:

```python
def get_recipient_requirements(token, quote_id):
    url = f"https://api.wise.com/v1/quotes/{quote_id}/account-requirements"
    
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    
    response = requests.get(url, headers=headers)
    return response.json()
```

This returns structured data about required fields and their formats for the specific recipient country/currency combination.

## 6. Implementation Example

Complete Python implementation for creating a recipient:

```python
import requests
import json

class WiseRecipientAPI:
    def __init__(self, api_token, is_sandbox=False):
        self.api_token = api_token
        self.base_url = "https://api.sandbox.transferwise.tech" if is_sandbox else "https://api.wise.com"
        self.headers = {
            "Authorization": f"Bearer {self.api_token}",
            "Content-Type": "application/json"
        }
    
    def create_recipient(self, profile_id, currency, account_holder_name, country, account_details):
        """Create a new recipient account"""
        url = f"{self.base_url}/v1/accounts"
        
        # Determine account type based on currency and country
        account_type = self._determine_account_type(currency, country)
        
        payload = {
            "currency": currency,
            "type": account_type,
            "profile": profile_id,
            "accountHolderName": account_holder_name,
            "country": country,
            "details": account_details
        }
        
        response = requests.post(url, headers=self.headers, data=json.dumps(payload))
        
        if response.status_code >= 400:
            self._handle_error(response)
        
        return response.json()
    
    def get_recipient_requirements(self, quote_id):
        """Get dynamic recipient requirements based on quote"""
        url = f"{self.base_url}/v1/quotes/{quote_id}/account-requirements"
        response = requests.get(url, headers=self.headers)
        
        if response.status_code >= 400:
            self._handle_error(response)
            
        return response.json()
    
    def list_recipients(self, profile_id, currency=None):
        """List all recipients for a profile"""
        url = f"{self.base_url}/v2/accounts"
        params = {"profile": profile_id}
        
        if currency:
            params["currency"] = currency
            
        response = requests.get(url, headers=self.headers, params=params)
        
        if response.status_code >= 400:
            self._handle_error(response)
            
        return response.json()
    
    def get_recipient(self, recipient_id):
        """Get a specific recipient by ID"""
        url = f"{self.base_url}/v2/accounts/{recipient_id}"
        response = requests.get(url, headers=self.headers)
        
        if response.status_code >= 400:
            self._handle_error(response)
            
        return response.json()
    
    def deactivate_recipient(self, recipient_id):
        """Deactivate a recipient"""
        url = f"{self.base_url}/v2/accounts/{recipient_id}"
        response = requests.delete(url, headers=self.headers)
        
        if response.status_code >= 400:
            self._handle_error(response)
            
        return True
    
    def _determine_account_type(self, currency, country):
        """Helper method to determine account type based on currency and country"""
        if currency == "EUR":
            return "iban"
        elif currency == "GBP" and country == "GB":
            return "sort_code"
        elif currency == "USD" and country == "US":
            return "aba"
        # Add more mappings as needed
        else:
            # Default to a general type
            return "bank_account"
    
    def _handle_error(self, response):
        """Handle API errors"""
        try:
            error_data = response.json()
            error_msg = error_data.get('errors', [{}])[0].get('message', 'Unknown error')
        except:
            error_msg = f"Error: HTTP {response.status_code}"
            
        raise Exception(f"Wise API Error: {error_msg}")
```

## 7. Usage Example

```python
# Initialize the API client
wise_api = WiseRecipientAPI(api_token="YOUR_API_TOKEN", is_sandbox=True)

# Create a USD recipient in the United States
recipient = wise_api.create_recipient(
    profile_id="12345",
    currency="USD",
    account_holder_name="John Smith",
    country="US",
    account_details={
        "legalType": "PRIVATE",
        "accountType": "CHECKING",
        "accountNumber": "12345678",
        "routingNumber": "111000000"
    }
)

print(f"Created recipient: {recipient['id']}")

# List all recipients
recipients = wise_api.list_recipients(profile_id="12345")
print(f"Found {len(recipients)} recipients")
```

## 8. Error Handling Best Practices

1. Always validate input data before sending to the API
2. Implement proper error handling with specific error messages
3. Implement retries for transient network issues
4. Log all API requests and responses for troubleshooting
5. Implement rate limiting to avoid hitting API limits

## 9. Security Considerations

1. Never store API tokens in code repositories
2. Use environment variables or secure vaults for tokens
3. Implement proper access controls for the server
4. Validate and sanitize all input data
5. Implement proper logging while ensuring sensitive data is not logged

This implementation guide should provide you with all the necessary information to create a robust Python server that can create recipients using the Wise API.