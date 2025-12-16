# 🐳 Docker Deployment Guide

**Simple, clean deployment instructions for nife-llmlite API**

---

## 📋 Prerequisites

- Docker installed ([Get Docker](https://docs.docker.com/get-docker/))
- Docker Compose installed (included with Docker Desktop)
- Terminal/Command Line access

---

## 🚀 Deployment Steps

### Step 1: Navigate to Project

```bash
cd /path/to/nife-litellm
```

### Step 2: Build the Docker Image

```bash
docker-compose build
```

**What happens:**
- Downloads Python 3.11 base image
- Installs dependencies (Flask, LiteLLM, Gunicorn)
- Copies application code
- Creates optimized container

**Expected output:**
```
[+] Building 45.2s (12/12) FINISHED
=> [internal] load build definition
=> [internal] load .dockerignore
=> [internal] load metadata
=> CACHED [1/6] FROM python:3.11-slim
=> [2/6] WORKDIR /app
=> [3/6] COPY requirements.txt .
=> [4/6] RUN pip install -r requirements.txt
=> [5/6] COPY app.py .
=> [6/6] RUN useradd -m -u 1000 appuser
=> exporting to image
=> => writing image sha256:abc123...
=> => naming to docker.io/library/nife-litellm
```

### Step 3: Start the API

```bash
docker-compose up -d
```

**What happens:**
- Starts container in detached mode (background)
- Exposes port 8080
- Runs health checks
- Auto-restarts on failure

**Expected output:**
```
[+] Running 2/2
✔ Network nife-litellm_llmlite-network  Created
✔ Container nife-llmlite-api            Started
```

### Step 4: Verify Running

```bash
docker-compose ps
```

**Expected output:**
```
NAME                 STATUS                    PORTS
nife-llmlite-api    Up (healthy)              0.0.0.0:8080->8080/tcp
```

---

## 🔍 Verify Deployment

### Check API Health

```bash
curl http://localhost:8080/health
```

**Expected response:**
```json
{
  "status": "healthy",
  "timestamp": "2024-12-16T10:30:00.000000"
}
```

### Check API Info

```bash
curl http://localhost:8080/
```

**Expected response:**
```json
{
  "service": "nife-llmlite",
  "version": "1.0.0",
  "status": "operational",
  "endpoints": {
    "health": "/health",
    "completion": "/api/completion",
    "models": "/api/models"
  }
}
```

---

## 📊 View Logs

### Real-time logs

```bash
docker-compose logs -f
```

### Last 50 lines

```bash
docker-compose logs --tail=50
```

### Filter by service

```bash
docker-compose logs nife-llmlite
```

**Expected log output:**
```
nife-llmlite-api | ============================================================
nife-llmlite-api | 🚀 nife-llmlite API starting
nife-llmlite-api | 📍 Address: 0.0.0.0:8080
nife-llmlite-api | 🐛 Debug: False
nife-llmlite-api | ============================================================
nife-llmlite-api | [2024-12-16 10:30:00] [INFO] Starting gunicorn 21.2.0
nife-llmlite-api | [2024-12-16 10:30:00] [INFO] Listening at: http://0.0.0.0:8080
nife-llmlite-api | [2024-12-16 10:30:00] [INFO] Using worker: sync
nife-llmlite-api | [2024-12-16 10:30:00] [INFO] Booting worker with pid: 8
```

---

## 🛠️ Common Commands

### Stop API

```bash
docker-compose down
```

### Restart API

```bash
docker-compose restart
```

### Stop and remove everything

```bash
docker-compose down -v
```

### Rebuild from scratch

```bash
docker-compose build --no-cache
docker-compose up -d
```

### Scale to multiple instances

```bash
docker-compose up -d --scale nife-llmlite=3
```

---

## 🔧 Configuration

### Change Port

Edit `docker-compose.yml`:

```yaml
services:
  nife-llmlite:
    ports:
      - "9000:8080"  # Change 9000 to your desired port
```

Then restart:
```bash
docker-compose down
docker-compose up -d
```

### Enable Verbose Logging

Edit `docker-compose.yml`:

```yaml
services:
  nife-llmlite:
    environment:
      - VERBOSE=true  # Enable detailed LiteLLM logs
```

### Enable Debug Mode (Development Only)

Edit `docker-compose.yml`:

```yaml
services:
  nife-llmlite:
    environment:
      - DEBUG=true  # Enable Flask debug mode
```

---

## 🐛 Troubleshooting

### Container won't start

```bash
# Check logs
docker-compose logs

# Check container status
docker-compose ps
```

### Port already in use

```bash
# Check what's using port 8080
lsof -i :8080  # Mac/Linux
netstat -ano | findstr :8080  # Windows

# Kill the process or change port in docker-compose.yml
```

### API not responding

```bash
# Check if container is running
docker-compose ps

# Check logs for errors
docker-compose logs --tail=100

# Restart container
docker-compose restart
```

### Out of memory

```bash
# Check resource usage
docker stats

# Increase memory in Docker Desktop settings
# Or reduce worker count in Dockerfile
```

### Build fails

```bash
# Clean Docker cache
docker system prune -a

# Rebuild from scratch
docker-compose build --no-cache
```

---

## 📦 Production Deployment

### Using Docker Registry

```bash
# 1. Build image
docker build -t your-registry/nife-llmlite:latest .

# 2. Push to registry
docker push your-registry/nife-llmlite:latest

# 3. On production server
docker pull your-registry/nife-llmlite:latest
docker-compose up -d
```

### Environment Variables

Create `.env` file (optional):

```bash
PORT=8080
HOST=0.0.0.0
VERBOSE=false
DEBUG=false
```

Update `docker-compose.yml`:

```yaml
services:
  nife-llmlite:
    env_file:
      - .env
```

---

## 🔒 Security Checklist

- [ ] Container runs as non-root user ✅ (built-in)
- [ ] Use HTTPS in production (add reverse proxy)
- [ ] Configure CORS for your domain
- [ ] Add rate limiting (Nginx/API Gateway)
- [ ] Don't expose on public internet without authentication
- [ ] Keep Docker and dependencies updated

---

## 📈 Monitoring

### Check Container Health

```bash
docker inspect nife-llmlite-api | grep -A 10 Health
```

### Monitor Resources

```bash
docker stats nife-llmlite-api
```

### Check Container Logs

```bash
docker logs -f nife-llmlite-api
```

---

## ✅ Deployment Complete

Your API is now running at:
- **Local:** http://localhost:8080
- **Network:** http://YOUR_SERVER_IP:8080

**Next:** See [API_USAGE.md](./API_USAGE.md) for testing and usage examples.

---

## 🆘 Quick Reference

```bash
# Start
docker-compose up -d

# Stop
docker-compose down

# Logs
docker-compose logs -f

# Status
docker-compose ps

# Restart
docker-compose restart

# Rebuild
docker-compose build --no-cache
```

---

**Deployment Status: 🟢 Ready**
