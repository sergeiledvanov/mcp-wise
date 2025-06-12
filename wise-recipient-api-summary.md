# Wise API Documentation: Recipient Creation

Based on the available information, here's a comprehensive summary of Wise's Recipient API:

## 1. Endpoints for Recipient Creation

The Wise API uses different versions for recipient operations:

- **Create a recipient account**: `POST /v1/accounts`
- **Create a refund recipient account**: `POST /v1/accounts?refund=true`
- **Create an email recipient account**: Not explicitly shown, but appears to be available
- **List recipient accounts**: `GET /v2/accounts`
- **Get account by ID**: `GET /v2/accounts/{{accountId}}`
- **Deactivate a recipient account**: `DELETE /v2/accounts/{{accountId}}`
- **Retrieve recipient account requirements dynamically**: `GET /v1/quotes/{{quoteId}}/account-requirements`

## 2. Required Parameters and Formats

Since we couldn't directly access the full API documentation, I'll provide a general structure based on common banking APIs:

For creating a recipient (`POST /v1/accounts`), the request likely requires:

```json
{
  "currency": "TARGET_CURRENCY_CODE",
  "type": "ACCOUNT_TYPE", // e.g., "iban", "sort_code", etc.
  "profile": "PROFILE_ID",
  "accountHolderName": "RECIPIENT_NAME",
  "details": {
    // Varies depending on currency and country
    // For IBAN accounts:
    "legalType": "PRIVATE or BUSINESS",
    "iban": "IBAN_NUMBER",
    // For US accounts:
    "accountNumber": "ACCOUNT_NUMBER",
    "routingNumber": "ROUTING_NUMBER",
    "accountType": "CHECKING or SAVINGS",
    // Additional fields may be required depending on the country and currency
  }
}
```

The response structure likely includes:
```json
{
  "id": "RECIPIENT_ID",
  "profile": "PROFILE_ID",
  "accountHolderName": "RECIPIENT_NAME",
  "currency": "CURRENCY_CODE",
  "country": "COUNTRY_CODE",
  "type": "ACCOUNT_TYPE",
  "details": {
    // Account details reflecting what was submitted
  },
  "user": "USER_ID"
}
```

## 3. Authentication Methods

Wise API typically uses the following authentication methods:

- **Bearer Token Authentication**: Using OAuth 2.0 tokens in the Authorization header
  ```
  Authorization: Bearer {your_token}
  ```

- **API Key Authentication**: Some endpoints may accept API keys
  ```
  Authorization: {your_api_key}
  ```

## 4. Request and Response Formats

- **Content Type**: All requests and responses use JSON format (`application/json`)
- **HTTP Methods**:
  - `POST`: For creating resources
  - `GET`: For retrieving resources
  - `DELETE`: For deactivating resources

- **Versioning**: The API uses URL versioning (v1, v2)

## 5. Error Handling Considerations

Common error responses include:

- **400 Bad Request**: Invalid input, missing required fields
- **401 Unauthorized**: Authentication issues
- **403 Forbidden**: Permissions issues
- **404 Not Found**: Resource not found
- **500 Server Error**: Internal Wise server error

Error responses likely follow this structure:
```json
{
  "errors": [
    {
      "code": "ERROR_CODE",
      "message": "Human readable error message",
      "path": "Field causing the error (if applicable)"
    }
  ]
}
```

## Additional Notes

- The recipient account's hash can be used to track changes in recipient details
- The v2 resource provides features like `accountSummary` and `longAccountSummary` fields for UI representation
- To get dynamic recipient account requirements, use the `/v1/quotes/{{quoteId}}/account-requirements` endpoint
- All recipient IDs are cross-compatible between v1 and v2 APIs