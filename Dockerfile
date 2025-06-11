# Multi-stage build for EVE-NG MCP Server
FROM python:3.11-slim as builder

# Set build arguments
ARG BUILD_DATE
ARG VERSION
ARG VCS_REF

# Set labels
LABEL maintainer="EVE-NG MCP Server Team" \
      org.label-schema.build-date=$BUILD_DATE \
      org.label-schema.name="eveng-mcp-server" \
      org.label-schema.description="EVE-NG Model Context Protocol Server" \
      org.label-schema.version=$VERSION \
      org.label-schema.vcs-ref=$VCS_REF \
      org.label-schema.vcs-url="https://github.com/your-org/eveng-mcp-server" \
      org.label-schema.schema-version="1.0"

# Install system dependencies
RUN apt-get update && apt-get install -y \
    curl \
    git \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Install UV package manager
RUN pip install uv

# Set working directory
WORKDIR /app

# Copy dependency files
COPY pyproject.toml uv.lock ./

# Install dependencies
RUN uv sync --frozen --no-dev

# Production stage
FROM python:3.11-slim as production

# Install runtime dependencies
RUN apt-get update && apt-get install -y \
    curl \
    ca-certificates \
    && rm -rf /var/lib/apt/lists/* \
    && apt-get clean

# Create non-root user
RUN groupadd -r eveng && useradd -r -g eveng -u 1000 eveng

# Set working directory
WORKDIR /app

# Copy virtual environment from builder
COPY --from=builder /app/.venv /app/.venv

# Copy application code
COPY --chown=eveng:eveng . .

# Create necessary directories
RUN mkdir -p /app/logs /app/data /app/config \
    && chown -R eveng:eveng /app

# Switch to non-root user
USER eveng

# Set environment variables
ENV PATH="/app/.venv/bin:$PATH" \
    PYTHONPATH="/app" \
    PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    UV_SYSTEM_PYTHON=1

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

# Expose port
EXPOSE 8000

# Default command
CMD ["python", "-m", "eveng_mcp_server.cli", "run", "--transport", "sse", "--host", "0.0.0.0", "--port", "8000"]

# Development stage
FROM production as development

# Switch back to root for development tools
USER root

# Install development dependencies
RUN apt-get update && apt-get install -y \
    vim \
    less \
    htop \
    net-tools \
    && rm -rf /var/lib/apt/lists/*

# Install development Python packages
COPY --from=builder /app/.venv /app/.venv
RUN /app/.venv/bin/uv sync --frozen

# Switch back to eveng user
USER eveng

# Override command for development
CMD ["python", "-m", "eveng_mcp_server.cli", "run", "--transport", "sse", "--host", "0.0.0.0", "--port", "8000", "--debug"]
