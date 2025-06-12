"""
FastMCP server initialization.
"""

import os
from mcp.server.fastmcp import FastMCP

def create_app():
    """Create and configure the MCP application."""
    return FastMCP(__name__)

mcp = create_app()

from wise_mcp.resources import recipients