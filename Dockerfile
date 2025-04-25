FROM python:3.13-alpine@sha256:18159b2be11db91f84b8f8f655cd860f805dbd9e49a583ddaac8ab39bf4fe1a7

WORKDIR /app

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY src/ ./src/
COPY config/ ./config/

# Create directories
RUN mkdir -p /var/log/6v_watcher

# Set environment variable to use built-in tomllib
ENV PYTHONPATH=/app
ENV PYTHONUNBUFFERED=1
ENV QBITTORRENTAPI_DO_NOT_VERIFY_WEBUI_CERTIFICATE=True

# Run the application
CMD ["python", "src/main.py"]
