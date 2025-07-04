# Wise MCP Server

A MCP (Machine Communication Protocol) server that serves as a gateway for the Wise API, providing simplified access to Wise's recipient functionality.

## Features

- List all recipients from your Wise account via a simple MCP resource
- Automatically handles authentication and profile selection
- Uses the Wise Sandbox API for development and testing
- Available as a Docker image for easy integration

## Requirements

- Python 3.12 or higher (only if installing directly)
- `uv` package manager (only if installing directly)
- Wise API token
- Docker (if using Docker image)

## Get an API token

https://wise.com/your-account/integrations-and-tools/api-tokens

Create a new token here.

## Installation

### Option 1: Direct Installation

1. Clone this repository:
   ```bash
   git clone https://github.com/sergeiledvanov/mcp-wise
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

### Option 2: Using Docker

You can build a Docker image:

```bash
docker build -t mcp-wise .
```

And add to Claude Code by adding it to your `.mcp.json`

```json
{
  "mcpServers": {
    "mcp-wise": {
      "command": "docker",
      "args": [
        "run",
        "-i",
        "--rm",
        "--init",
        "-e", "WISE_API_TOKEN=your_api_token_here",
        "-e", "WISE_IS_SANDBOX=true",
        "mcp-wise:latest"
      ]
    }
  }
}
```

Make sure to replace `your_api_token_here` with your actual Wise API token.

Make sure to also update your .mcp.json file to match your selected mode. We provide template files that you can use:

1. For stdio mode (default):
   ```bash
   cp .mcp.json.stdio .mcp.json
   ```

2. For HTTP mode:
   ```bash
   cp .mcp.json.http .mcp.json
   ```

These template files contain the appropriate configuration for each mode.

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
- `WISE_IS_SANDBOX`: Set to true to use the Wise Sandbox API (default: false)
- `MODE`: MCP Server transport mode, either "http" or "stdio" (default: stdio)

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