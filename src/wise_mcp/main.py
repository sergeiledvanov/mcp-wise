"""
Entry point for the Wise MCP server.
"""

import os
from dotenv import load_dotenv
from wise_mcp.app import mcp

def main():
    load_dotenv()
    mode = os.getenv("MODE", "stdio").lower()
    
    if mode == "http":
        mcp.run(transport="streamable-http",
                host="127.0.0.1",
                port=14101)
    else:
        # Default stdio transport
        mcp.run()

if __name__ == "__main__":
    main()
