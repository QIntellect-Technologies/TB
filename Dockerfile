# Use Python 3.11 as the base image
FROM python:3.11-slim

# Install system dependencies including Node.js for frontend build
RUN apt-get update && apt-get install -y \
    curl \
    build-essential \
    && curl -fsSL https://deb.nodesource.com/setup_20.x | bash - \
    && apt-get install -y nodejs \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy backend requirements first for caching
COPY backend/requirements.txt ./backend/
RUN pip install --no-cache-dir -r backend/requirements.txt

# Copy frontend package files and install dependencies
COPY frontend/package*.json ./frontend/
RUN cd frontend && npm install

# Copy the entire project
COPY . .

# Build the frontend
RUN cd frontend && npm run build

# Ensure the backend static directory exists and copy the built frontend
RUN mkdir -p backend/static/dist && cp -r frontend/dist/* backend/static/dist/

# Set working directory to backend for the start command
WORKDIR /app/backend

# Use the PORT environment variable provided by Railway
CMD ["sh", "-c", "uvicorn main:app --host 0.0.0.0 --port ${PORT:-8000}"]
