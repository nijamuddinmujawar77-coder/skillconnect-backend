# ============================================
# SkillConnect Backend - Docker Configuration
# For DigitalOcean App Platform / Droplets
# ============================================

FROM python:3.12-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PORT=8000

# Build-time SECRET_KEY (only for collectstatic, not used in production)
ENV SECRET_KEY="build-time-secret-key-not-for-production"

# Set work directory
WORKDIR /app

# Install system dependencies (PostgreSQL only)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy project files
COPY . .

# Collect static files (using build-time SECRET_KEY)
RUN python manage.py collectstatic --no-input

# Create non-root user for security
RUN adduser --disabled-password --gecos '' appuser && chown -R appuser /app

# Make entrypoint executable
RUN chmod +x /app/entrypoint.sh

USER appuser

# Expose port
EXPOSE 8000

# Start command with migrations
CMD ["/app/entrypoint.sh"]
