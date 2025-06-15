# Wise MCP Server

A MCP (Machine Communication Protocol) server that serves as a gateway for the Wise API, providing simplified access to Wise's recipient functionality.

## Features

- List all recipients from your Wise account via a simple MCP resource
- Automatically handles authentication and profile selection
- Uses the Wise Sandbox API for development and testing

## Requirements

- Python 3.12 or higher
- `uv` package manager
- Wise API token

## Get an API token

https://wise.com/your-account/integrations-and-tools/api-tokens

Create a new token here.

## Installation

1. Clone this repository:
   ```bash
   git clone <repository-url>
   cd wise-mcp
   ```

2. Set up the environment:
   ```bash
   cp .env.example .env
   # Edit .env to add your Wise API token
   ```

3. Install dependencies with `uv`:
   ```bash
   uv venv
   uv pip install -e .
   ```

### Adding to claude.json

1. Add the Wise MCP server to your `~/.claude.json` file in your home directory:

```json
  "mcpServers": {
      "mcp-wise": {
        "command": "/path/to/mcp-wise/.venv/bin/python",
        "args": [
          "-m",
          "wise_mcp.main"
        ],
      }
  }
```

or as a streamable-http

```json
  "mcpServers": {
      "mcp-wise": {
         "type": "streamable-http",
         "url": "http://localhost:14101/mcp",
         "note": "For Streamable HTTP connections, add this URL directly in your MCP Client"
      }
  }
```

## Available MCP Resources

The server provides the following MCP resources:

### `list_recipients`

Returns a list of all recipients from your Wise account.

**Parameters**:
- `profile_type`: The type of profile to list recipients for. One of [personal, business]. Default: "personal"
- `currency`: Optional. Filter recipients by currency code (e.g., 'EUR', 'USD')

### `send_money`

Sends money to a recipient using the Wise API.

**Parameters**:
- `profile_type`: The type of profile to use (personal or business)
- `source_currency`: Source currency code (e.g., 'USD') 
- `source_amount`: Amount in source currency to send
- `recipient_id`: The ID of the recipient to send money to
- `payment_reference`: Optional. Reference message for the transfer (defaults to "money")
- `source_of_funds`: Optional. Source of the funds (e.g., "salary", "savings")

## Configuration

Configuration is done via environment variables, which can be set in the `.env` file:

- `WISE_API_TOKEN`: Your Wise API token (required)

## Development

### Project Structure

```
wise-mcp/
├── .env                # Environment variables (not in git)
├── .env.example        # Example environment variables
├── pyproject.toml      # Project dependencies and configuration
├── README.md           # This file
└── src/                # Source code
    ├── main.py         # Entry point
    └── wise_mcp/       # Main package
        ├── api/        # API clients
        │   └── wise_client.py # Wise API client
        ├── resources/  # MCP resources
        │   └── recipients.py  # Recipients resource
        └── app.py      # MCP application setup
```

### Adding New Features

To add new features:

1. Add new API client methods in `src/wise_mcp/api/wise_client.py`
2. Create new resources in `src/wise_mcp/resources/`
3. Import and register the new resources in `src/wise_mcp/app.py`

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

MIT