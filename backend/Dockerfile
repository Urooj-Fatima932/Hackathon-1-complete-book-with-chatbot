FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# HF Spaces provides PORT environment variable
ENV PORT=8000
EXPOSE 8000

# Run the app using HF-provided port
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]

