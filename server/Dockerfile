FROM python:3.12-slim

WORKDIR /app

# Install system deps
RUN apt-get update && apt-get install -y --no-install-recommends \
    ca-certificates && \
    rm -rf /var/lib/apt/lists/*

# Copy Sui CLI binary from build context
COPY sui /usr/local/bin/sui
RUN chmod +x /usr/local/bin/sui

# Install Python deps
RUN pip install --no-cache-dir fastapi uvicorn[standard] httpx

# Copy app
COPY *.py .
COPY start.sh .
RUN chmod +x start.sh

# Sui config directory
RUN mkdir -p /root/.sui/sui_config

EXPOSE 8080

CMD ["./start.sh"]
