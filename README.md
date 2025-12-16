# nife-llmlite

**Production-ready LiteLLM API service** - Simple, fast, multi-provider LLM API wrapper.

## 🚀 Features

- ✅ **REST API** - Clean HTTP endpoints
- ✅ **Multi-Provider** - OpenAI, Anthropic, Google, Mistral, Cohere, Together AI, DeepSeek
- ✅ **Auto-Detection** - Automatic provider routing
- ✅ **Production-Ready** - Gunicorn, health checks, logging
- ✅ **Docker** - Fully containerized
- ✅ **Fast** - Efficient async processing

---

## ⚡ Quick Start

### Using Docker Compose (Recommended)

```bash
# Start the API
docker-compose up -d

# Check status
docker-compose ps

# View logs
docker-compose logs -f

# Stop
docker-compose down
```

API available at: **http://localhost:8080**

### Using Docker

```bash
# Build
docker build -t nife-llmlite .

# Run
docker run -d -p 8080:8080 --name nife-llmlite nife-llmlite

# Logs
docker logs -f nife-llmlite

# Stop
docker stop nife-llmlite && docker rm nife-llmlite
```

### Local Development

```bash
# Install dependencies
pip install -r requirements.txt

# Run
python app.py

# Or with gunicorn
gunicorn --bind 0.0.0.0:8080 --workers 4 app:app
```

---

## 📡 API Endpoints

### 1. Health Check

```bash
curl http://localhost:8080/health
```

**Response:**
```json
{
  "status": "healthy",
  "timestamp": "2024-12-16T10:30:00.000000"
}
```

### 2. Root Info

```bash
curl http://localhost:8080/
```

**Response:**
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

### 3. Completion

**Single Prompt:**
```bash
curl -X POST http://localhost:8080/api/completion \
  -H "Content-Type: application/json" \
  -d '{
    "model_id": "gpt-4",
    "api_key": "sk-...",
    "prompts": ["What is artificial intelligence?"]
  }'
```

**Multiple Prompts:**
```bash
curl -X POST http://localhost:8080/api/completion \
  -H "Content-Type: application/json" \
  -d '{
    "model_id": "claude-3-sonnet",
    "api_key": "sk-ant-...",
    "prompts": [
      "Explain quantum computing",
      "What is machine learning?"
    ],
    "temperature": 0.7,
    "max_tokens": 500
  }'
```

**Response:**
```json
{
  "timestamp": "2024-12-16T10:30:00.000000",
  "model": "gpt-4",
  "normalized_model": "gpt-4",
  "provider": "openai",
  "responses": [
    {
      "prompt_id": 1,
      "prompt": "What is artificial intelligence?",
      "response": "Artificial Intelligence (AI) is...",
      "status": "success"
    }
  ],
  "summary": {
    "total": 1,
    "successful": 1,
    "failed": 0
  }
}
```

### 4. List Models

```bash
curl http://localhost:8080/api/models
```

**Response:**
```json
{
  "providers": {
    "openai": {
      "models": ["gpt-4", "gpt-4-turbo", "gpt-3.5-turbo"],
      "api_key_env": "OPENAI_API_KEY"
    },
    "anthropic": {
      "models": ["claude-3-opus", "claude-3-sonnet"],
      "api_key_env": "ANTHROPIC_API_KEY"
    }
  }
}
```

---

## 🔑 Supported Providers

| Provider | Example Model | API Key Format |
|----------|--------------|----------------|
| **OpenAI** | `gpt-4`, `gpt-4-turbo`, `gpt-3.5-turbo` | `sk-...` |
| **Anthropic** | `claude-3-sonnet`, `claude-3-opus` | `sk-ant-...` |
| **Google** | `gemini-pro`, `gemini-1.5-pro` | `AIza...` |
| **Mistral** | `mistral-large`, `mistral-medium` | `...` |
| **Cohere** | `command`, `command-r` | `...` |
| **Together AI** | `meta-llama/Llama-3-70b-chat-hf` | `...` |
| **DeepSeek** | `deepseek-chat`, `deepseek-coder` | `...` |

---

## 📝 API Request Schema

### POST /api/completion

**Request Body:**
```json
{
  "model_id": "string (required)",      // Model identifier
  "api_key": "string (required)",       // Provider API key
  "prompts": "string|array (required)", // Single or multiple prompts
  "temperature": 0.7,                   // Optional, default: 0.7
  "max_tokens": 1000                    // Optional, default: 1000
}
```

**Response Codes:**
- `200` - All prompts successful
- `207` - Partial success (some failed)
- `400` - Bad request
- `500` - Internal server error

---

## 🔧 Configuration

### Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `PORT` | `8080` | API port |
| `HOST` | `0.0.0.0` | Bind address |
| `VERBOSE` | `false` | LiteLLM verbose logging |
| `DEBUG` | `false` | Flask debug mode |

### Docker Compose Override

Create `docker-compose.override.yml`:
```yaml
version: '3.8'
services:
  nife-llmlite:
    environment:
      - VERBOSE=true
      - DEBUG=true
    ports:
      - "9000:8080"  # Custom port
```

---

## 🧪 Testing

### Quick Test

```bash
# Health check
curl http://localhost:8080/health

# Test completion (replace with your API key)
curl -X POST http://localhost:8080/api/completion \
  -H "Content-Type: application/json" \
  -d '{
    "model_id": "gpt-3.5-turbo",
    "api_key": "YOUR_OPENAI_API_KEY",
    "prompts": ["Hello, world!"]
  }'
```

### Test Script

Save as `test_api.sh`:
```bash
#!/bin/bash

API_URL="http://localhost:8080"

echo "Testing health endpoint..."
curl -s $API_URL/health | jq

echo -e "\nTesting completion endpoint..."
curl -s -X POST $API_URL/api/completion \
  -H "Content-Type: application/json" \
  -d '{
    "model_id": "gpt-3.5-turbo",
    "api_key": "'"$OPENAI_API_KEY"'",
    "prompts": ["What is 2+2?"]
  }' | jq

echo -e "\nTesting models endpoint..."
curl -s $API_URL/api/models | jq
```

```bash
chmod +x test_api.sh
./test_api.sh
```

---

## 📊 Performance

### Benchmarks (Single Instance)

- **Latency**: ~1-3s (depends on LLM provider)
- **Throughput**: ~10-30 req/s
- **Memory**: ~200-500MB
- **CPU**: ~0.5-1.0 core under load

### Scaling

Scale horizontally using Docker Compose:

```bash
# Start 3 instances behind a load balancer
docker-compose up -d --scale nife-llmlite=3
```

---

## 🛡️ Security

### Best Practices

1. **Never commit API keys** - Use environment variables
2. **Use HTTPS in production** - Add SSL/TLS termination
3. **Enable rate limiting** - Use nginx or API gateway
4. **Monitor logs** - Track usage and errors
5. **Update regularly** - Keep dependencies current

### Production Checklist

- [ ] Use HTTPS
- [ ] Add rate limiting
- [ ] Configure CORS properly
- [ ] Set up monitoring
- [ ] Enable log aggregation
- [ ] Use secrets management
- [ ] Add authentication layer

---

## 🐛 Troubleshooting

### Container won't start
```bash
docker-compose logs nife-llmlite
docker-compose ps
```

### API not responding
```bash
# Check if container is running
docker ps

# Check health
curl http://localhost:8080/health

# View logs
docker-compose logs -f
```

### Memory issues
```bash
# Check container stats
docker stats

# Restart with memory limit
docker-compose down
docker-compose up -d
```

### Connection timeout
Increase timeout in production:
```python
# In app.py
gunicorn --timeout 300 app:app
```

---

## 📁 Project Structure

```
nife-llmlite/
├── app.py                 # Main API application
├── requirements.txt       # Python dependencies
├── Dockerfile            # Production container
├── docker-compose.yml    # Container orchestration
├── .gitignore           # Git ignore rules
└── README.md            # This file
```

---

## 🔄 Deployment

### Production Deployment

1. **Build the image:**
```bash
docker build -t nife-llmlite:latest .
```

2. **Tag for registry:**
```bash
docker tag nife-llmlite:latest your-registry/nife-llmlite:latest
```

3. **Push to registry:**
```bash
docker push your-registry/nife-llmlite:latest
```

4. **Deploy:**
```bash
docker pull your-registry/nife-llmlite:latest
docker-compose up -d
```

### Kubernetes Deployment

Create `deployment.yaml`:
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: nife-llmlite
spec:
  replicas: 3
  selector:
    matchLabels:
      app: nife-llmlite
  template:
    metadata:
      labels:
        app: nife-llmlite
    spec:
      containers:
      - name: nife-llmlite
        image: your-registry/nife-llmlite:latest
        ports:
        - containerPort: 8080
        env:
        - name: PORT
          value: "8080"
        livenessProbe:
          httpGet:
            path: /health
            port: 8080
          initialDelaySeconds: 10
          periodSeconds: 30
```

---

## 📄 License

MIT License - Free for commercial and personal use

---

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

---

## 📚 Resources

- [LiteLLM Documentation](https://docs.litellm.ai/)
- [Flask Documentation](https://flask.palletsprojects.com/)
- [Docker Documentation](https://docs.docker.com/)

---

**Made with ❤️ for the LLM community**
