# Wise MCP server

The goal of this document is to create an MCP server that will serve as a gateway for the Wise API.

## Requirements
- MCP server should be called `wise-mcp`.
- MCP server should only be able to: 
  - list all recipients
- Wise API should be used in sandbox (`https://api.sandbox.transferwise.tech`)

### List all recipients
- Listing all recipients should be implemented as an mcp resource
- MCP method for listing all recipients should not have any parameters
- In order to list all recipients, Wise API requires a profile ID. To obtain one, use list profiles API call described here https://docs.wise.com/api-docs/api-reference/profile#list-profiles

## Documentation
Analyze current directory for the existing documentation in md files.

## Implementation
1. Use current directory for the MCP server project.
2. Wise API token should be stored in the `.env` file.
3. use `uv` package manager, define dependencies in `pyproject.toml`
4. MCP server should be written in Python.
5. Use the most suitable and widespread frameworks that are suitable for the task.
6. MCP server should not have any REST endpoints
7. MCP server should only contain tools and resources:
   Use `@mcp.resource` for endpoint-like, RESTful operations.
   Use `@mcp.tool` for general-purpose, callable functions.
8. No data should be stored locally in the database, everything should be fetched from the Wise API in runtime by the MCP server.
9. Create a readme.md documentation for the MCP server, explaining how to run it, how to use it, and how to contribute.

## Steps to create the MCP server
- Analyze documentation stored in md files.
- Break down the task into smaller steps, analyze each step, and provide a detailed explanation of how to implement it.
- Verify the plan, make sure it is feasible, then implement it. Think harder.