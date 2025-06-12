"""
MCP server initialization.
"""

import os
from mcp import MCP


def create_app():
    """Create and configure the MCP application."""
    app = MCP(__name__)
    
    # Import resources
    from wise_mcp.resources import recipients
    
    return app


app = create_app()