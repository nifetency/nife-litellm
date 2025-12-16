# 🧪 API Testing & Usage Guide

**Complete guide to testing and using nife-llmlite API**

---

## 🚀 Quick Test

After deployment, verify the API is working:

```bash
curl http://localhost:8080/health
```

**Expected Response:**
```json
{
  "status": "healthy",
  "timestamp": "2024-12-16T10:30:00.000000"
}
```

✅ If you see this, your API is ready!

---

## 📡 Available Endpoints

| Method | Endpoint | Purpose |
|--------|----------|---------|
| GET | `/` | API information |
| GET | `/health` | Health check |
| GET | `/api/models` | List supported providers |
| POST | `/api/completion` | Generate completions |

---

## 1️⃣ Test Health Endpoint

### Request

```bash
curl http://localhost:8080/health
```

### Response

```json
{
  "status": "healthy",
  "timestamp": "2024-12-16T10:30:00.000000"
}
```

**Status Code:** `200 OK`

---

## 2️⃣ Test API Info Endpoint

### Request

```bash
curl http://localhost:8080/
```

### Response

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

**Status Code:** `200 OK`

---

## 3️⃣ Test Models Endpoint

### Request

```bash
curl http://localhost:8080/api/models
```

### Response

```json
{
  "providers": {
    "openai": {
      "models": ["gpt-4", "gpt-4-turbo", "gpt-3.5-turbo", "gpt-4o"],
      "api_key_env": "OPENAI_API_KEY"
    },
    "anthropic": {
      "models": ["claude-3-opus", "claude-3-sonnet", "claude-3-haiku"],
      "api_key_env": "ANTHROPIC_API_KEY"
    },
    "google": {
      "models": ["gemini-pro", "gemini-1.5-pro", "gemini-1.5-flash"],
      "api_key_env": "GEMINI_API_KEY"
    },
    "mistral": {
      "models": ["mistral-large", "mistral-medium", "mistral-small"],
      "api_key_env": "MISTRAL_API_KEY"
    },
    "cohere": {
      "models": ["command", "command-light", "command-r"],
      "api_key_env": "COHERE_API_KEY"
    },
    "together": {
      "models": ["meta-llama/Llama-3-70b-chat-hf"],
      "api_key_env": "TOGETHERAI_API_KEY"
    },
    "deepseek": {
      "models": ["deepseek-chat", "deepseek-coder"],
      "api_key_env": "DEEPSEEK_API_KEY"
    }
  },
  "note": "This is a sample list. Check provider documentation for complete model catalog."
}
```

**Status Code:** `200 OK`

---

## 4️⃣ Test Completion Endpoint

### Basic Request (Single Prompt)

```bash
curl -X POST http://localhost:8080/api/completion \
  -H "Content-Type: application/json" \
  -d '{
    "model_id": "gpt-3.5-turbo",
    "api_key": "sk-YOUR_OPENAI_API_KEY",
    "prompts": ["What is artificial intelligence?"]
  }'
```

### Response (Success)

```json
{
  "timestamp": "2024-12-16T10:35:00.123456",
  "model": "gpt-3.5-turbo",
  "normalized_model": "gpt-3.5-turbo",
  "provider": "openai",
  "responses": [
    {
      "prompt_id": 1,
      "prompt": "What is artificial intelligence?",
      "response": "Artificial Intelligence (AI) is the simulation of human intelligence processes by machines, especially computer systems. These processes include learning, reasoning, and self-correction. AI applications include expert systems, natural language processing, speech recognition, and machine vision.",
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

**Status Code:** `200 OK`

---

## 📋 Request Schema

### Required Fields

```json
{
  "model_id": "string",    // Model identifier (e.g., "gpt-4")
  "api_key": "string",     // Provider API key
  "prompts": "string|array" // Single prompt or array of prompts
}
```

### Optional Fields

```json
{
  "temperature": 0.7,      // 0.0 to 1.0, default: 0.7
  "max_tokens": 1000       // Max response tokens, default: 1000
}
```

---

## 🎯 Complete Examples

### Example 1: OpenAI GPT-4

```bash
curl -X POST http://localhost:8080/api/completion \
  -H "Content-Type: application/json" \
  -d '{
    "model_id": "gpt-4",
    "api_key": "sk-YOUR_KEY",
    "prompts": ["Explain quantum computing in simple terms"]
  }'
```

**Response:**
```json
{
  "timestamp": "2024-12-16T10:40:00.000000",
  "model": "gpt-4",
  "normalized_model": "gpt-4",
  "provider": "openai",
  "responses": [
    {
      "prompt_id": 1,
      "prompt": "Explain quantum computing in simple terms",
      "response": "Quantum computing uses the principles of quantum mechanics to process information. Unlike classical computers that use bits (0 or 1), quantum computers use quantum bits or 'qubits' that can exist in multiple states simultaneously through superposition...",
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

### Example 2: Anthropic Claude

```bash
curl -X POST http://localhost:8080/api/completion \
  -H "Content-Type: application/json" \
  -d '{
    "model_id": "claude-3-sonnet",
    "api_key": "sk-ant-YOUR_KEY",
    "prompts": ["Write a haiku about programming"],
    "temperature": 0.9
  }'
```

**Response:**
```json
{
  "timestamp": "2024-12-16T10:45:00.000000",
  "model": "claude-3-sonnet",
  "normalized_model": "claude-3-sonnet",
  "provider": "anthropic",
  "responses": [
    {
      "prompt_id": 1,
      "prompt": "Write a haiku about programming",
      "response": "Code flows like water\nBugs hide in silent shadows\nDebug brings the light",
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

### Example 3: Google Gemini

```bash
curl -X POST http://localhost:8080/api/completion \
  -H "Content-Type: application/json" \
  -d '{
    "model_id": "gemini-pro",
    "api_key": "AIzaYOUR_KEY",
    "prompts": ["List 3 benefits of cloud computing"],
    "max_tokens": 500
  }'
```

**Response:**
```json
{
  "timestamp": "2024-12-16T10:50:00.000000",
  "model": "gemini-pro",
  "normalized_model": "gemini/gemini-pro",
  "provider": "google",
  "responses": [
    {
      "prompt_id": 1,
      "prompt": "List 3 benefits of cloud computing",
      "response": "Here are 3 key benefits of cloud computing:\n\n1. Cost Efficiency: Reduces capital expenses by eliminating the need for physical hardware and infrastructure...\n\n2. Scalability: Resources can be easily scaled up or down based on demand...\n\n3. Accessibility: Access your data and applications from anywhere with internet connection...",
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

### Example 4: Multiple Prompts (Batch)

```bash
curl -X POST http://localhost:8080/api/completion \
  -H "Content-Type: application/json" \
  -d '{
    "model_id": "gpt-3.5-turbo",
    "api_key": "sk-YOUR_KEY",
    "prompts": [
      "What is Python?",
      "What is JavaScript?",
      "What is Docker?"
    ],
    "temperature": 0.7,
    "max_tokens": 200
  }'
```

**Response:**
```json
{
  "timestamp": "2024-12-16T10:55:00.000000",
  "model": "gpt-3.5-turbo",
  "normalized_model": "gpt-3.5-turbo",
  "provider": "openai",
  "responses": [
    {
      "prompt_id": 1,
      "prompt": "What is Python?",
      "response": "Python is a high-level, interpreted programming language known for its simplicity and readability...",
      "status": "success"
    },
    {
      "prompt_id": 2,
      "prompt": "What is JavaScript?",
      "response": "JavaScript is a versatile programming language primarily used for web development...",
      "status": "success"
    },
    {
      "prompt_id": 3,
      "prompt": "What is Docker?",
      "response": "Docker is a platform for developing, shipping, and running applications in containers...",
      "status": "success"
    }
  ],
  "summary": {
    "total": 3,
    "successful": 3,
    "failed": 0
  }
}
```

---

## ⚠️ Error Responses

### 400 Bad Request (Missing Required Field)

**Request:**
```bash
curl -X POST http://localhost:8080/api/completion \
  -H "Content-Type: application/json" \
  -d '{
    "model_id": "gpt-4"
  }'
```

**Response:**
```json
{
  "error": "api_key is required"
}
```

### 400 Bad Request (Invalid JSON)

**Request:**
```bash
curl -X POST http://localhost:8080/api/completion \
  -H "Content-Type: application/json" \
  -d 'invalid json'
```

**Response:**
```json
{
  "error": "No JSON data provided"
}
```

### 500 Internal Server Error (Invalid API Key)

**Response:**
```json
{
  "error": "Internal server error",
  "message": "AuthenticationError: Invalid API key provided",
  "timestamp": "2024-12-16T11:00:00.000000"
}
```

### 207 Multi-Status (Partial Success)

**Request:** Multiple prompts with one failing

**Response:**
```json
{
  "timestamp": "2024-12-16T11:05:00.000000",
  "model": "gpt-3.5-turbo",
  "normalized_model": "gpt-3.5-turbo",
  "provider": "openai",
  "responses": [
    {
      "prompt_id": 1,
      "prompt": "Valid prompt",
      "response": "This is the response...",
      "status": "success"
    },
    {
      "prompt_id": 2,
      "prompt": "Invalid prompt that causes error",
      "response": null,
      "status": "error",
      "error": "RateLimitError: Rate limit exceeded"
    }
  ],
  "summary": {
    "total": 2,
    "successful": 1,
    "failed": 1
  }
}
```

**Status Code:** `207 Multi-Status`

---

## 🔑 Provider-Specific Examples

### OpenAI

```bash
# GPT-4
curl -X POST http://localhost:8080/api/completion \
  -d '{"model_id": "gpt-4", "api_key": "sk-...", "prompts": ["Hello"]}'

# GPT-3.5 Turbo
curl -X POST http://localhost:8080/api/completion \
  -d '{"model_id": "gpt-3.5-turbo", "api_key": "sk-...", "prompts": ["Hello"]}'
```

### Anthropic

```bash
# Claude 3 Opus
curl -X POST http://localhost:8080/api/completion \
  -d '{"model_id": "claude-3-opus", "api_key": "sk-ant-...", "prompts": ["Hello"]}'

# Claude 3 Sonnet
curl -X POST http://localhost:8080/api/completion \
  -d '{"model_id": "claude-3-sonnet", "api_key": "sk-ant-...", "prompts": ["Hello"]}'
```

### Google

```bash
# Gemini Pro
curl -X POST http://localhost:8080/api/completion \
  -d '{"model_id": "gemini-pro", "api_key": "AIza...", "prompts": ["Hello"]}'

# Gemini 1.5 Pro
curl -X POST http://localhost:8080/api/completion \
  -d '{"model_id": "gemini-1.5-pro", "api_key": "AIza...", "prompts": ["Hello"]}'
```

### Mistral

```bash
curl -X POST http://localhost:8080/api/completion \
  -d '{"model_id": "mistral-large", "api_key": "YOUR_KEY", "prompts": ["Hello"]}'
```

### Cohere

```bash
curl -X POST http://localhost:8080/api/completion \
  -d '{"model_id": "command", "api_key": "YOUR_KEY", "prompts": ["Hello"]}'
```

### Together AI (Llama)

```bash
curl -X POST http://localhost:8080/api/completion \
  -d '{"model_id": "meta-llama/Llama-3-70b-chat-hf", "api_key": "YOUR_KEY", "prompts": ["Hello"]}'
```

### DeepSeek

```bash
curl -X POST http://localhost:8080/api/completion \
  -d '{"model_id": "deepseek-chat", "api_key": "YOUR_KEY", "prompts": ["Hello"]}'
```

---

## 🧪 Test Script

Save this as `test_api.sh`:

```bash
#!/bin/bash

API_URL="http://localhost:8080"

echo "Testing nife-llmlite API"
echo "========================"

# Test 1: Health
echo -e "\n1. Health Check:"
curl -s $API_URL/health | jq

# Test 2: Info
echo -e "\n2. API Info:"
curl -s $API_URL/ | jq

# Test 3: Models
echo -e "\n3. Supported Models:"
curl -s $API_URL/api/models | jq '.providers | keys'

# Test 4: Completion (if API key provided)
if [ -n "$OPENAI_API_KEY" ]; then
    echo -e "\n4. Completion Test:"
    curl -s -X POST $API_URL/api/completion \
      -H "Content-Type: application/json" \
      -d '{
        "model_id": "gpt-3.5-turbo",
        "api_key": "'"$OPENAI_API_KEY"'",
        "prompts": ["Say hello in 5 words"],
        "max_tokens": 50
      }' | jq '.responses[0].response'
else
    echo -e "\n4. Completion Test: Skipped (Set OPENAI_API_KEY to test)"
fi

echo -e "\n========================"
echo "Tests Complete!"
```

**Run:**
```bash
chmod +x test_api.sh
export OPENAI_API_KEY="sk-your-key"
./test_api.sh
```

---

## 📊 Response Status Codes

| Code | Meaning | When |
|------|---------|------|
| `200` | OK | All prompts successful |
| `207` | Multi-Status | Some prompts failed |
| `400` | Bad Request | Missing/invalid parameters |
| `404` | Not Found | Invalid endpoint |
| `500` | Server Error | API/LLM provider error |

---

## 💡 Tips & Best Practices

### 1. Temperature Settings

- **0.0 - 0.3:** Factual, deterministic responses
- **0.4 - 0.7:** Balanced creativity
- **0.8 - 1.0:** More creative, varied responses

### 2. Token Limits

- Start with `max_tokens: 500` for testing
- Adjust based on response length needs
- Higher tokens = longer generation time

### 3. Batch Processing

- Process multiple prompts in one request
- More efficient than multiple requests
- All prompts use same model/settings

### 4. Error Handling

- Always check `summary.failed` count
- Review individual `response.status`
- Implement retry logic for failures

---

## 🔍 Testing Checklist

After deployment, verify:

- [ ] Health endpoint returns 200
- [ ] Info endpoint shows correct version
- [ ] Models endpoint lists providers
- [ ] Completion works with your API key
- [ ] Multiple prompts work correctly
- [ ] Error handling works properly
- [ ] Response times are acceptable
- [ ] Logs show no errors

---

## 📝 Common Use Cases

### Use Case 1: Question Answering

```bash
curl -X POST http://localhost:8080/api/completion \
  -H "Content-Type: application/json" \
  -d '{
    "model_id": "gpt-4",
    "api_key": "YOUR_KEY",
    "prompts": ["What causes rainbows?"]
  }'
```

### Use Case 2: Content Generation

```bash
curl -X POST http://localhost:8080/api/completion \
  -H "Content-Type: application/json" \
  -d '{
    "model_id": "claude-3-opus",
    "api_key": "YOUR_KEY",
    "prompts": ["Write a product description for wireless headphones"],
    "temperature": 0.8
  }'
```

### Use Case 3: Code Assistance

```bash
curl -X POST http://localhost:8080/api/completion \
  -H "Content-Type: application/json" \
  -d '{
    "model_id": "gpt-4",
    "api_key": "YOUR_KEY",
    "prompts": ["Write a Python function to calculate fibonacci numbers"]
  }'
```

### Use Case 4: Batch Analysis

```bash
curl -X POST http://localhost:8080/api/completion \
  -H "Content-Type: application/json" \
  -d '{
    "model_id": "gpt-3.5-turbo",
    "api_key": "YOUR_KEY",
    "prompts": [
      "Summarize: Article text 1...",
      "Summarize: Article text 2...",
      "Summarize: Article text 3..."
    ],
    "max_tokens": 100
  }'
```

---

## ✅ Success Checklist

Your API is working correctly when:

- [x] Health check returns `"status": "healthy"`
- [x] Completion endpoint returns responses
- [x] Provider detection works correctly
- [x] Error messages are clear
- [x] Logs show successful requests
- [x] Response times are reasonable

---

**API Ready for Use! 🎉**

For deployment instructions, see [DOCKER_DEPLOY.md](./DOCKER_DEPLOY.md)
