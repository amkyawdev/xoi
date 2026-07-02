FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    curl \
    git \
    wget \
    gnupg \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for caching
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Install Playwright browsers
RUN playwright install --with-deps chromium

# Expose port
EXPOSE 8000

# Default command
CMD ["uvicorn", "api.server:app", "--host", "0.0.0.0", "--port", "8000"]
