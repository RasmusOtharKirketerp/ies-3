# Description: Dockerfile for building a Docker image for the application
# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    libxml2-dev \
    libxslt-dev \
    python3-dev \
    curl \
    supervisor \
    && rm -rf /var/lib/apt/lists/*

# Install NLTK data (required for newspaper3k)
RUN python -m pip install --no-cache-dir nltk && \
    python -c "import nltk; nltk.download('punkt')"

# Copy requirements first for better caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Create data directory for database
RUN mkdir -p /app/data

# Copy the application code
COPY src/ ./src/
COPY start_app.bat ./

# Copy supervisord configuration
COPY supervisord.conf /etc/supervisor/conf.d/supervisord.conf

# Set environment variables
ENV FLASK_APP=src/app.py \
    FLASK_ENV=production \
    PORT=1910 \
    HOST=0.0.0.0 \
    DB_PATH=/app/data/articles.db \
    USER_ID=default \
    PYTHONUNBUFFERED=1 \
    LANG=C.UTF-8 \
    LC_ALL=C.UTF-8

# Create volume mount point
VOLUME ["/app/data"]

# Expose the port the app runs on
EXPOSE ${PORT}

# Health check
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:${PORT}/status || exit 1

# Run supervisord
CMD ["/usr/bin/supervisord", "-c", "/etc/supervisor/conf.d/supervisord.conf"]




