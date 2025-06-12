"""
Entry point for the Wise MCP server.
"""

from wise_mcp.app import mcp

def main():
    mcp.run()

if __name__ == "__main__":
    main()
