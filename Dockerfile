# Use Python 3.10 slim image (required by MCP library)
FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Install Git first (needed to install MCP from GitHub)
RUN apt-get update && apt-get install -y git && rm -rf /var/lib/apt/lists/*

# Copy requirements file
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Expose port
EXPOSE 8000

# Run the web application
CMD ["python", "web_mcp_server.py"]