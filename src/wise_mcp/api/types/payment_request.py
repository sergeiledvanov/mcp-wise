"""
Payment request type definitions.
"""

from dataclasses import dataclass
from typing import Optional, List, Dict, Any, Literal


@dataclass
class Money:
    """Represents a monetary amount."""
    value: float
    currency: str

@dataclass
class PayerAddress:
    """Represents an address for a payer."""
    countryIso3Code: str
    firstLine: Optional[str] = None


@dataclass
class PayerV2:
    """Represents a payer in a payment request."""
    name: str
    email: Optional[str] = None
    address: Optional[PayerAddress] = None
    locale: Optional[str] = 'en'


@dataclass
class LineItemTax:
    """Represents tax information for a line item."""
    name: str
    percentage: float
    behaviour: Literal["INCLUDED", "EXCLUDED"]


@dataclass
class LineItem:
    """Represents a line item in an invoice."""
    name: str
    unit_price: Money
    quantity: int
    tax: Optional[LineItemTax] = None


@dataclass
class PaymentRequestInvoiceCommand:
    """Command for creating an invoice payment request."""
    request_type: Literal["INVOICE"] = "INVOICE"
    selected_payment_methods: List[str] = None
    balance_id: int = None
    due_at: str = None
    invoice_number: Optional[str] = None
    payer: Optional[PayerV2] = None
    line_items: List[LineItem] = None
    issue_date: str = None
    message: Optional[str] = None

    def __post_init__(self):
        if self.selected_payment_methods is None:
            self.selected_payment_methods = ["ACCOUNT_DETAILS"]
        if self.line_items is None:
            self.line_items = []


@dataclass
class PaymentRequestV2:
    """Represents a payment request response."""
    id: str
    amount: Money
    profile_id: int
    balance_id: int
    creator: Dict[str, Any]
    status: str
    link: Optional[str] = None
    created_at: Optional[str] = None
    published_at: Optional[str] = None
    due_at: Optional[str] = None
    message: Optional[str] = None
    description: Optional[str] = None
    reference: Optional[str] = None
    request_type: Optional[str] = None
    invoice: Optional[Dict[str, Any]] = None
