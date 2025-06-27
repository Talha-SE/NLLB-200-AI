# Use official Python base image
FROM python:3.10-slim

# Set working directory inside container
WORKDIR /app

# Install system dependencies for sentencepiece, torch
RUN apt-get update && apt-get install -y \
    libstdc++6 \
    git \
    wget \
    curl \
    libgomp1 \
    && rm -rf /var/lib/apt/lists/*

# Copy dependency file and install Python packages
COPY requirements.txt .

# Force pip to install only prebuilt wheels where possible
RUN pip install --upgrade pip && \
    pip install --no-cache-dir --prefer-binary -r requirements.txt

# Copy source code
COPY app.py .

# Expose default port for Render
EXPOSE 8080

# Start Flask app
CMD ["python", "app.py"]
