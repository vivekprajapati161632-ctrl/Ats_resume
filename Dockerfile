# --- Stage 1: Build & Dependency Downloader ---
FROM python:3.11-slim AS builder

WORKDIR /build

# System level packages install karein build tools ke liye
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Requirements file copy karein
COPY requirements.txt .

# Wheel compilation aur global build caching ko bypass karke direct install karein
RUN pip install --no-cache-dir --user -r requirements.txt

# --- Stage 2: Final Production Stage (Lightweight Runtime) ---
FROM python:3.11-slim AS runner

WORKDIR /app

# Non-root user create karein secure runtime execution ke liye
RUN useradd -u 8888 appuser && chown -R appuser:appuser /app

# Stage 1 se built packages ko copy karein
COPY --from=builder /root/.local /home/appuser/.local
COPY --from=builder /usr/lib /usr/lib

# Application source files ko copy karein
COPY --chown=appuser:appuser app.py resume_parser.py resume_optimizer.py utils.py ./
COPY --chown=appuser:appuser templates/ ./templates/

# Environment Variables path setting aur Python logs synchronization
ENV PATH=/home/appuser/.local/bin:$PATH
ENV PYTHONUNBUFFERED=1

USER appuser

# Streamlit operational port map
EXPOSE 8501

# Production flags setup configurations
ENTRYPOINT ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0", "--server.enableCORS=false", "--server.enableXsrfProtection=false"]
