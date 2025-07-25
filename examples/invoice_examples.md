# Invoice Creation Examples

This document provides examples of how to use the new invoice creation tools in the Wise MCP server.

**Important: Invoices are only available for business profiles. Personal profiles cannot create invoices.**

## Invoice Creation Process

The invoice creation follows a 3-step process:
1. **Create empty invoice** - Gets auto-generated fields like invoice number
2. **Update with full data** - Adds line items, payer information, etc.
3. **Publish invoice** - Makes the invoice active and available for payment

This process is handled automatically by the `create_invoice` tool.

## Example 1: Simple Business Invoice

```python
# First, get available balance currencies (business profile only)
get_balance_currencies(profile_type="business")

# Create a simple invoice with one line item
create_invoice(
    profile_type="business",  # Must be "business" - personal profiles cannot create invoices
    balance_id=12345,  # Use the balance ID from get_balance_currencies
    due_days=30,
    line_items=[
        {
            "name": "Consulting Services",
            "amount": 1000.00,
            "currency": "EUR",
            "quantity": 1
        }
    ],
    payer_name="John Doe",
    payer_address={
        "firstLine": "56 Shoreditch High Street, London E1 6JJ",
        "countryIso3Code": "gbr"
    },
    payer_email="john@example.com",
    message="Thank you for your business!"
)
```

## Example 2: Invoice with Multiple Line Items and Tax

```python
create_invoice(
    profile_type="business",  # Only business profiles can create invoices
    balance_id=67890,
    due_days=15,
    line_items=[
        {
            "name": "Web Development",
            "amount": 2500.00,
            "currency": "USD",
            "quantity": 1,
            "tax_name": "VAT",
            "tax_percentage": 20.0,
            "tax_behaviour": "EXCLUDED"
        },
        {
            "name": "Domain Registration",
            "amount": 15.00,
            "currency": "USD",
            "quantity": 2,
            "tax_name": "VAT",
            "tax_percentage": 20.0,
            "tax_behaviour": "EXCLUDED"
        }
    ],
    payer_name="Acme Corporation",
        payer_address={
        "firstLine": "56 Shoreditch High Street, London E1 6JJ",
        "countryIso3Code": "gbr"
    },
    payer_locale="es",
    payer_email="accounting@acme.com",
    message="Payment terms: Net 15 days",
    issue_date="2025-07-01T00:00:00.000Z"
)
```

## Getting Balance Information

Before creating an invoice, you need to know which balance to use. Use the `get_balance_currencies` tool:

```python
# This will return something like:
# Available balances for invoice creation (business profiles only):
# • Currency: EUR, Balance ID: 12345
# • Currency: USD, Balance ID: 67890
# • Currency: GBP, Balance ID: 11111

get_balance_currencies(profile_type="business")  # Must use business profile
```

## Formatting payer address

We want to follow the common address formatting practices for a given region/country.
The payer address also goes onto an invoice PDF and we usually want it go onto multiple lines there – to achieve this, you may place new line characters into the address ("\n").

For example, a given address "56 Shoreditch High Street, London, E1 6JJ" can be split onto multiple lines as "56 Shoreditch High Street\nLondon\nE1 6JJ".

## Important Notes

- **Business Profiles Only**: Personal profiles cannot create invoices. You must use `profile_type="business"`
- **Auto-generated Invoice Numbers**: If you don't provide an `invoice_number`, Wise will auto-generate one
- **Currency Matching**: The line item currency must match the balance currency
- **Automatic Publishing**: The invoice is automatically published and ready for payment after creation

## Tax Behaviors

When adding tax to line items, you can specify the tax behavior:

- `"INCLUDED"`: Tax is included in the unit price
- `"EXCLUDED"`: Tax is added on top of the unit price (default)

## Response Format

Successful invoice creation will return:
```
Invoice created and published successfully! ID: req_abc123, Invoice Number: INV-2025-001, Status: PUBLISHED, Link: https://wise.com/pay/req_abc123
```

The invoice will be created, updated with full data, and published in one operation.
