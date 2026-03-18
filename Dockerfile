# ============================================
# Smart Student Manager - Dockerfile for MySQL
# Multi-stage optimized Docker image
# ============================================

# Stage 1: Base image with Python
FROM python:3.11-slim as base

# Set environment variables
# PYTHONUNBUFFERED ensures logs are printed immediately (no buffering)
# PYTHONDONTWRITEBYTECODE prevents Python from writing .pyc files (saves space)
# PIP_NO_CACHE_DIR reduces image size by not caching pip packages
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1
ENV PIP_NO_CACHE_DIR=1

# Set working directory in container
WORKDIR /app

# Stage 2: Builder - Install dependencies
FROM base as builder

# Copy requirements file
COPY requirements.txt .

# Create virtual environment and install dependencies
# This installs packages to /opt/venv directory
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Upgrade pip and install Python packages
RUN pip install --upgrade pip setuptools wheel && \
    pip install -r requirements.txt

# Stage 3: Runtime - Final image
FROM base as runtime

# Set path to use the virtual environment from builder
ENV PATH="/opt/venv/bin:$PATH"

# Copy virtual environment from builder stage
COPY --from=builder /opt/venv /opt/venv

# Copy application code
COPY . .

# Create a non-root user for security (best practice)
# This prevents container from running as root
RUN useradd -m -u 1000 appuser && \
    chown -R appuser:appuser /app

# Switch to non-root user
USER appuser

# Expose port 5000 (Flask default port)
EXPOSE 5000

# Health check (optional but recommended)
# Checks if the application is responding to requests
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:5000/').read()"

# Run the Flask application
# This command will be executed when the container starts
CMD ["python", "app.py"]

