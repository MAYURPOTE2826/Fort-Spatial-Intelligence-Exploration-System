# --- Build Stage ---
FROM python:3.11-slim as builder

WORKDIR /app

# Install system dependencies for GDAL/Rasterio/GeoPandas and building wheels
RUN apt-get update && apt-get install -y \
    gdal-bin \
    libgdal-dev \
    gcc \
    g++ \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

ENV CPLUS_INCLUDE_PATH=/usr/include/gdal
ENV C_INCLUDE_PATH=/usr/include/gdal

# Create virtual environment and install dependencies
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip wheel --no-cache-dir --no-deps --wheel-dir /app/wheels -r requirements.txt

# --- Runtime Stage ---
FROM python:3.11-slim as runtime

WORKDIR /app

# Install only runtime system dependencies
RUN apt-get update && apt-get install -y \
    gdal-bin \
    libgdal-dev \
    libpq5 \
    && rm -rf /var/lib/apt/lists/*

ENV CPLUS_INCLUDE_PATH=/usr/include/gdal
ENV C_INCLUDE_PATH=/usr/include/gdal

COPY --from=builder /app/wheels /wheels
COPY --from=builder /opt/venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Install wheels without index
RUN pip install --no-cache-dir /wheels/*

# Add non-root user for security
RUN groupadd -r appuser && useradd -r -g appuser appuser
RUN chown -R appuser:appuser /app

COPY . /app/
RUN chown -R appuser:appuser /app

USER appuser

# Run via Gunicorn
CMD ["gunicorn", "-c", "gunicorn_conf.py", "app.main:app"]
