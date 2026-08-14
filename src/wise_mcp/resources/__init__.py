"""
Resource module initialization.
"""

from wise_mcp.resources.recipients import list_recipients
from wise_mcp.resources.transactions import list_transactions, get_balance_statement

__all__ = ["list_recipients", "list_transactions", "get_balance_statement"]
