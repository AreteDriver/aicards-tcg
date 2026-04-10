FROM python:3.12-slim

WORKDIR /app

# Install system deps + Node.js (for Metaplex minting helper)
RUN apt-get update && apt-get install -y --no-install-recommends \
    ca-certificates curl && \
    curl -fsSL https://deb.nodesource.com/setup_20.x | bash - && \
    apt-get install -y nodejs && \
    rm -rf /var/lib/apt/lists/*

# Install Python deps
RUN pip install --no-cache-dir fastapi uvicorn[standard] httpx

# Install Node deps for Metaplex minting
COPY package.json .
RUN npm install --production

# Copy app
COPY *.py .
COPY *.js .
COPY start.sh .
RUN chmod +x start.sh

EXPOSE 8080

CMD ["./start.sh"]
