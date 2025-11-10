# Dockerfile for LangGraph Multi-Agent Workflow
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy all application code
COPY . .

# Set Python path
ENV PYTHONPATH=/app

# Default command (can be overridden in job definition)
CMD ["python", "batch_job.py", "--agent", "all"]
