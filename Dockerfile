# Use Python 3.9 slim image
FROM python:3.9-slim

# Set working directory
WORKDIR /app

# Copy requirements file
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Expose port (MCP typically uses stdio, but we'll expose a port for potential HTTP wrapper)
EXPOSE 8000

# Run the application
CMD ["python", "mcp_server.py"]