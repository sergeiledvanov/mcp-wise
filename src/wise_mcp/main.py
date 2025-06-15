"""
Entry point for the Wise MCP server.
"""

from wise_mcp.app import mcp

def main():
    mcp.run(transport="streamable-http",
            host="127.0.0.1",
            port=14101)

if __name__ == "__main__":
    main()
