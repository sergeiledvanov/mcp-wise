FROM python:3.12-slim

WORKDIR /app

# Copy project files
COPY pyproject.toml .
COPY README.md .
COPY src ./src

# Install dependencies
RUN pip install --no-cache-dir .

# Environment variables with defaults
# API token should be provided at runtime
# docker run --env WISE_API_TOKEN=your_token your_image
ENV WISE_IS_SANDBOX="true"
ENV MODE="stdio"

# Set entrypoint
ENTRYPOINT ["python", "-m", "wise_mcp.main"]