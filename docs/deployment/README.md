# Deployment Guide

This guide covers production deployment of the EVE-NG MCP Server in various environments.

## 🎯 Deployment Options

- [Docker Deployment](#docker-deployment)
- [Kubernetes Deployment](#kubernetes-deployment)
- [Systemd Service](#systemd-service)
- [Reverse Proxy Setup](#reverse-proxy-setup)
- [Cloud Deployment](#cloud-deployment)

## 🐳 Docker Deployment

### Basic Docker Setup

1. **Create Dockerfile** (if not exists):

```dockerfile
FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Install UV
RUN pip install uv

# Copy project files
COPY . .

# Install dependencies
RUN uv sync --frozen

# Create non-root user
RUN useradd -m -u 1000 eveng && chown -R eveng:eveng /app
USER eveng

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

# Expose port
EXPOSE 8000

# Start server
CMD ["uv", "run", "eveng-mcp-server", "run", "--transport", "sse", "--host", "0.0.0.0", "--port", "8000"]
```

2. **Build and Run**:

```bash
# Build image
docker build -t eveng-mcp-server:latest .

# Run container
docker run -d \
  --name eveng-mcp-server \
  -p 8000:8000 \
  -e EVENG_HOST=your-eve-server \
  -e EVENG_USERNAME=admin \
  -e EVENG_PASSWORD=eve \
  eveng-mcp-server:latest
```

### Docker Compose

Create `docker-compose.yml`:

```yaml
version: '3.8'

services:
  eveng-mcp-server:
    build: .
    container_name: eveng-mcp-server
    restart: unless-stopped
    ports:
      - "8000:8000"
    environment:
      - EVENG_HOST=eve.local
      - EVENG_USERNAME=admin
      - EVENG_PASSWORD=eve
      - EVENG_PORT=80
      - EVENG_PROTOCOL=http
      - MCP_TRANSPORT=sse
      - MCP_HOST=0.0.0.0
      - MCP_PORT=8000
      - MCP_LOG_LEVEL=INFO
    volumes:
      - ./logs:/app/logs
      - ./config:/app/config
    networks:
      - eveng-network
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8000/health"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 40s

  nginx:
    image: nginx:alpine
    container_name: eveng-mcp-nginx
    restart: unless-stopped
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf
      - ./ssl:/etc/nginx/ssl
    depends_on:
      - eveng-mcp-server
    networks:
      - eveng-network

networks:
  eveng-network:
    driver: bridge
```

## ☸️ Kubernetes Deployment

### Namespace and ConfigMap

```yaml
# namespace.yaml
apiVersion: v1
kind: Namespace
metadata:
  name: eveng-mcp

---
# configmap.yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: eveng-mcp-config
  namespace: eveng-mcp
data:
  EVENG_HOST: "eve.local"
  EVENG_PORT: "80"
  EVENG_PROTOCOL: "http"
  MCP_TRANSPORT: "sse"
  MCP_HOST: "0.0.0.0"
  MCP_PORT: "8000"
  MCP_LOG_LEVEL: "INFO"
```

### Secret for Credentials

```yaml
# secret.yaml
apiVersion: v1
kind: Secret
metadata:
  name: eveng-mcp-secret
  namespace: eveng-mcp
type: Opaque
data:
  EVENG_USERNAME: YWRtaW4=  # base64 encoded 'admin'
  EVENG_PASSWORD: ZXZl      # base64 encoded 'eve'
```

### Deployment

```yaml
# deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: eveng-mcp-server
  namespace: eveng-mcp
  labels:
    app: eveng-mcp-server
spec:
  replicas: 2
  selector:
    matchLabels:
      app: eveng-mcp-server
  template:
    metadata:
      labels:
        app: eveng-mcp-server
    spec:
      containers:
      - name: eveng-mcp-server
        image: eveng-mcp-server:latest
        ports:
        - containerPort: 8000
        envFrom:
        - configMapRef:
            name: eveng-mcp-config
        - secretRef:
            name: eveng-mcp-secret
        livenessProbe:
          httpGet:
            path: /health
            port: 8000
          initialDelaySeconds: 30
          periodSeconds: 10
        readinessProbe:
          httpGet:
            path: /ready
            port: 8000
          initialDelaySeconds: 5
          periodSeconds: 5
        resources:
          requests:
            memory: "256Mi"
            cpu: "250m"
          limits:
            memory: "512Mi"
            cpu: "500m"
```

### Service and Ingress

```yaml
# service.yaml
apiVersion: v1
kind: Service
metadata:
  name: eveng-mcp-service
  namespace: eveng-mcp
spec:
  selector:
    app: eveng-mcp-server
  ports:
  - protocol: TCP
    port: 80
    targetPort: 8000
  type: ClusterIP

---
# ingress.yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: eveng-mcp-ingress
  namespace: eveng-mcp
  annotations:
    nginx.ingress.kubernetes.io/rewrite-target: /
    cert-manager.io/cluster-issuer: "letsencrypt-prod"
spec:
  tls:
  - hosts:
    - eveng-mcp.yourdomain.com
    secretName: eveng-mcp-tls
  rules:
  - host: eveng-mcp.yourdomain.com
    http:
      paths:
      - path: /
        pathType: Prefix
        backend:
          service:
            name: eveng-mcp-service
            port:
              number: 80
```

## 🔧 Systemd Service

### Service File

Create `/etc/systemd/system/eveng-mcp-server.service`:

```ini
[Unit]
Description=EVE-NG MCP Server
After=network.target
Wants=network.target

[Service]
Type=exec
User=eveng-mcp
Group=eveng-mcp
WorkingDirectory=/opt/eveng-mcp-server
Environment=PATH=/opt/eveng-mcp-server/.venv/bin
ExecStart=/opt/eveng-mcp-server/.venv/bin/python -m eveng_mcp_server.cli run --transport sse --host 0.0.0.0 --port 8000
ExecReload=/bin/kill -HUP $MAINPID
Restart=always
RestartSec=10
StandardOutput=journal
StandardError=journal
SyslogIdentifier=eveng-mcp-server

# Security settings
NoNewPrivileges=true
PrivateTmp=true
ProtectSystem=strict
ProtectHome=true
ReadWritePaths=/opt/eveng-mcp-server/logs

[Install]
WantedBy=multi-user.target
```

### Installation Steps

```bash
# Create user
sudo useradd -r -s /bin/false eveng-mcp

# Create directories
sudo mkdir -p /opt/eveng-mcp-server
sudo mkdir -p /opt/eveng-mcp-server/logs
sudo chown -R eveng-mcp:eveng-mcp /opt/eveng-mcp-server

# Install application
sudo -u eveng-mcp git clone https://github.com/your-org/eveng-mcp-server.git /opt/eveng-mcp-server
cd /opt/eveng-mcp-server
sudo -u eveng-mcp python -m venv .venv
sudo -u eveng-mcp .venv/bin/pip install -e .

# Create configuration
sudo -u eveng-mcp cp config.example.json /opt/eveng-mcp-server/config.json

# Install and start service
sudo systemctl daemon-reload
sudo systemctl enable eveng-mcp-server
sudo systemctl start eveng-mcp-server

# Check status
sudo systemctl status eveng-mcp-server
```

## 🔒 Reverse Proxy Setup

### Nginx Configuration

Create `/etc/nginx/sites-available/eveng-mcp`:

```nginx
upstream eveng_mcp_backend {
    server 127.0.0.1:8000;
    keepalive 32;
}

server {
    listen 80;
    server_name eveng-mcp.yourdomain.com;
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl http2;
    server_name eveng-mcp.yourdomain.com;

    # SSL Configuration
    ssl_certificate /etc/ssl/certs/eveng-mcp.crt;
    ssl_certificate_key /etc/ssl/private/eveng-mcp.key;
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers ECDHE-RSA-AES256-GCM-SHA512:DHE-RSA-AES256-GCM-SHA512:ECDHE-RSA-AES256-GCM-SHA384:DHE-RSA-AES256-GCM-SHA384;
    ssl_prefer_server_ciphers off;
    ssl_session_cache shared:SSL:10m;

    # Security Headers
    add_header X-Frame-Options DENY;
    add_header X-Content-Type-Options nosniff;
    add_header X-XSS-Protection "1; mode=block";
    add_header Strict-Transport-Security "max-age=63072000; includeSubDomains; preload";

    # Logging
    access_log /var/log/nginx/eveng-mcp.access.log;
    error_log /var/log/nginx/eveng-mcp.error.log;

    # Rate Limiting
    limit_req_zone $binary_remote_addr zone=api:10m rate=10r/s;
    limit_req zone=api burst=20 nodelay;

    location / {
        proxy_pass http://eveng_mcp_backend;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_cache_bypass $http_upgrade;
        proxy_read_timeout 86400;
    }

    # Health check endpoint
    location /health {
        proxy_pass http://eveng_mcp_backend/health;
        access_log off;
    }
}
```

### Apache Configuration

```apache
<VirtualHost *:80>
    ServerName eveng-mcp.yourdomain.com
    Redirect permanent / https://eveng-mcp.yourdomain.com/
</VirtualHost>

<VirtualHost *:443>
    ServerName eveng-mcp.yourdomain.com
    
    # SSL Configuration
    SSLEngine on
    SSLCertificateFile /etc/ssl/certs/eveng-mcp.crt
    SSLCertificateKeyFile /etc/ssl/private/eveng-mcp.key
    
    # Security Headers
    Header always set X-Frame-Options DENY
    Header always set X-Content-Type-Options nosniff
    Header always set X-XSS-Protection "1; mode=block"
    Header always set Strict-Transport-Security "max-age=63072000; includeSubDomains; preload"
    
    # Proxy Configuration
    ProxyPreserveHost On
    ProxyPass / http://127.0.0.1:8000/
    ProxyPassReverse / http://127.0.0.1:8000/
    
    # WebSocket Support
    RewriteEngine on
    RewriteCond %{HTTP:Upgrade} websocket [NC]
    RewriteCond %{HTTP:Connection} upgrade [NC]
    RewriteRule ^/?(.*) "ws://127.0.0.1:8000/$1" [P,L]
    
    # Logging
    CustomLog /var/log/apache2/eveng-mcp.access.log combined
    ErrorLog /var/log/apache2/eveng-mcp.error.log
</VirtualHost>
```

## ☁️ Cloud Deployment

### AWS ECS

```yaml
# task-definition.json
{
  "family": "eveng-mcp-server",
  "networkMode": "awsvpc",
  "requiresCompatibilities": ["FARGATE"],
  "cpu": "256",
  "memory": "512",
  "executionRoleArn": "arn:aws:iam::account:role/ecsTaskExecutionRole",
  "containerDefinitions": [
    {
      "name": "eveng-mcp-server",
      "image": "your-account.dkr.ecr.region.amazonaws.com/eveng-mcp-server:latest",
      "portMappings": [
        {
          "containerPort": 8000,
          "protocol": "tcp"
        }
      ],
      "environment": [
        {"name": "EVENG_HOST", "value": "eve.local"},
        {"name": "MCP_TRANSPORT", "value": "sse"},
        {"name": "MCP_HOST", "value": "0.0.0.0"},
        {"name": "MCP_PORT", "value": "8000"}
      ],
      "secrets": [
        {"name": "EVENG_USERNAME", "valueFrom": "arn:aws:secretsmanager:region:account:secret:eveng-credentials:username"},
        {"name": "EVENG_PASSWORD", "valueFrom": "arn:aws:secretsmanager:region:account:secret:eveng-credentials:password"}
      ],
      "logConfiguration": {
        "logDriver": "awslogs",
        "options": {
          "awslogs-group": "/ecs/eveng-mcp-server",
          "awslogs-region": "us-west-2",
          "awslogs-stream-prefix": "ecs"
        }
      },
      "healthCheck": {
        "command": ["CMD-SHELL", "curl -f http://localhost:8000/health || exit 1"],
        "interval": 30,
        "timeout": 5,
        "retries": 3,
        "startPeriod": 60
      }
    }
  ]
}
```

### Google Cloud Run

```yaml
# cloudrun.yaml
apiVersion: serving.knative.dev/v1
kind: Service
metadata:
  name: eveng-mcp-server
  annotations:
    run.googleapis.com/ingress: all
spec:
  template:
    metadata:
      annotations:
        autoscaling.knative.dev/maxScale: "10"
        run.googleapis.com/cpu-throttling: "false"
    spec:
      containerConcurrency: 80
      timeoutSeconds: 300
      containers:
      - image: gcr.io/your-project/eveng-mcp-server:latest
        ports:
        - containerPort: 8000
        env:
        - name: EVENG_HOST
          value: "eve.local"
        - name: MCP_TRANSPORT
          value: "sse"
        - name: MCP_HOST
          value: "0.0.0.0"
        - name: MCP_PORT
          value: "8000"
        - name: EVENG_USERNAME
          valueFrom:
            secretKeyRef:
              name: eveng-credentials
              key: username
        - name: EVENG_PASSWORD
          valueFrom:
            secretKeyRef:
              name: eveng-credentials
              key: password
        resources:
          limits:
            cpu: 1000m
            memory: 512Mi
        livenessProbe:
          httpGet:
            path: /health
            port: 8000
          initialDelaySeconds: 30
          periodSeconds: 10
```

## 📊 Monitoring and Health Checks

### Health Check Endpoints

Add to your server implementation:

```python
@app.get("/health")
async def health_check():
    return {"status": "healthy", "timestamp": datetime.utcnow().isoformat()}

@app.get("/ready")
async def readiness_check():
    # Check EVE-NG connectivity
    try:
        await eveng_client.test_connection()
        return {"status": "ready", "eveng": "connected"}
    except Exception:
        return {"status": "not ready", "eveng": "disconnected"}, 503
```

### Prometheus Metrics

```python
from prometheus_client import Counter, Histogram, Gauge

# Metrics
REQUEST_COUNT = Counter('eveng_mcp_requests_total', 'Total requests', ['method', 'endpoint'])
REQUEST_DURATION = Histogram('eveng_mcp_request_duration_seconds', 'Request duration')
ACTIVE_CONNECTIONS = Gauge('eveng_mcp_active_connections', 'Active connections')
```

## 🔐 Security Configuration

### Environment Variables

```bash
# Production security settings
export SECURITY_DISABLE_SSL_WARNINGS=false
export SECURITY_MAX_CONCURRENT_CONNECTIONS=50
export SECURITY_SESSION_TIMEOUT=1800
export MCP_LOG_LEVEL=WARNING
```

### Firewall Rules

```bash
# Allow only necessary ports
sudo ufw allow 22/tcp    # SSH
sudo ufw allow 80/tcp    # HTTP
sudo ufw allow 443/tcp   # HTTPS
sudo ufw deny 8000/tcp   # Block direct access to MCP server
sudo ufw enable
```

## 📝 Configuration Management

### Production Configuration

```json
{
  "eveng": {
    "host": "production-eve-server.company.com",
    "port": 443,
    "protocol": "https",
    "ssl_verify": true,
    "timeout": 60,
    "max_retries": 5
  },
  "mcp": {
    "transport": "sse",
    "host": "0.0.0.0",
    "port": 8000,
    "log_level": "WARNING",
    "log_format": "json"
  },
  "security": {
    "disable_ssl_warnings": false,
    "max_concurrent_connections": 100,
    "session_timeout": 1800
  }
}
```

## 🚀 Deployment Checklist

- [ ] Environment variables configured
- [ ] SSL certificates installed
- [ ] Firewall rules configured
- [ ] Health checks implemented
- [ ] Monitoring setup
- [ ] Logging configured
- [ ] Backup strategy defined
- [ ] Security hardening applied
- [ ] Load testing completed
- [ ] Documentation updated
