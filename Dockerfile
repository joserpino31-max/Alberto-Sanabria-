# Use official lightweight Python slim image
FROM python:3.11-slim

# Set environment variables to optimize Python for containerized production
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PORT=5000

# Set working directory inside container
WORKDIR /app

# Install dependencies in a separate layer for efficient Docker cache utilization
COPY requirements.txt /app/
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

# Copy application source code
COPY . /app/

# Create a non-privileged user and grant ownership of the working directory
RUN groupadd -r appuser && useradd -r -g appuser -d /app -s /sbin/nologin appuser \
    && chown -R appuser:appuser /app

# Switch to non-root user for security best practices
USER appuser

# Expose application port
EXPOSE 5000

# Health check to ensure the container is responsive
HEALTHCHECK --interval=30s --timeout=5s --start-period=5s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://127.0.0.1:5000/').read()" || exit 1

# Launch the application using Gunicorn production WSGI server
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--workers", "2", "--threads", "2", "--timeout", "120", "--access-logfile", "-", "--error-logfile", "-", "app:app"]
