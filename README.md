# Wise MCP Server

A MCP (Machine Communication Protocol) server that serves as a gateway for the Wise API, providing simplified access to Wise's recipient functionality.

## Features

- List all recipients from your Wise account via a simple MCP resource
- Automatically handles authentication and profile selection
- Uses the Wise Sandbox API for development and testing

## Requirements

- Python 3.9 or higher
- `uv` package manager
- Wise API token (from the Wise Sandbox environment)

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

## Usage

### Starting the Server

```bash
cd src
python main.py
```

### Available MCP Resources

The server provides the following MCP resources:

#### `list_recipients`

Returns a list of all recipients from your Wise account.

**Parameters**: None

**Example Usage**:
```python
from mcp.client import Client

# Connect to the MCP server
client = Client("wise-mcp")

# List all recipients
recipients = client.list_recipients()

# Process the recipients
for recipient in recipients:
    print(f"Recipient: {recipient['accountHolderName']}, {recipient['currency']}")
```

## Configuration

Configuration is done via environment variables, which can be set in the `.env` file:

- `WISE_API_TOKEN`: Your Wise API token (required)
- `ENVIRONMENT`: The environment to run in (development, testing, production)

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