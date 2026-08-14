"""Read-only Wise activity and balance-statement tools."""

from typing import Any, Dict, Optional

from wise_mcp.app import mcp
from ..api.wise_client_helper import init_wise_client


@mcp.tool()
def list_transactions(
    profile_type: str = "personal",
    since: Optional[str] = None,
    until: Optional[str] = None,
    status: Optional[str] = None,
    monetary_resource_type: Optional[str] = None,
    size: int = 100,
    next_cursor: Optional[str] = None,
) -> Dict[str, Any]:
    """List Wise profile activity, including transfers and balance transactions.

    Dates must be ISO-8601 UTC timestamps. If ``next_cursor`` is returned, pass it back
    to retrieve the next page.
    """
    ctx = init_wise_client(profile_type)
    return ctx.wise_api_client.list_activities(
        profile_id=ctx.profile.profile_id,
        since=since,
        until=until,
        status=status,
        monetary_resource_type=monetary_resource_type,
        size=size,
        next_cursor=next_cursor,
    )


@mcp.tool()
def get_balance_statement(
    balance_id: str,
    currency: str,
    interval_start: str,
    interval_end: str,
    profile_type: str = "personal",
    statement_type: str = "COMPACT",
    statement_locale: str = "en",
) -> Dict[str, Any]:
    """Retrieve detailed transactions for one currency balance and date interval."""
    ctx = init_wise_client(profile_type)
    return ctx.wise_api_client.get_balance_statement(
        profile_id=ctx.profile.profile_id,
        balance_id=balance_id,
        currency=currency,
        interval_start=interval_start,
        interval_end=interval_end,
        statement_type=statement_type,
        statement_locale=statement_locale,
    )
